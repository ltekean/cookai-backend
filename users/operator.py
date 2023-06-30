import logging
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from articles.coupang import update_ingredient_links
from .models import User

logger = logging.getLogger(__name__)


def delete_dormant_user():
    dormant_users = User.objects.filter(is_active=False)
    for user in dormant_users:
        last_updated_date = (user.updated_at + datetime.timedelta(hours=9)).date()
        now_date = datetime.date.today()
        dormant_seconds = int((now_date - last_updated_date).total_seconds())
        if dormant_seconds > 604800:
            user.delete()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs delete_dormant_user."

    def start(self, *args, **options):
        scheduler = BackgroundScheduler(
            timezone=settings.TIME_ZONE
        )  # BlockingScheduler를 사용할 수도 있습니다.
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            delete_dormant_user,
            trigger=CronTrigger(day_of_week="0-6", hour="03", minute="00"),
            id="delete_dormant_user",  # id는 고유해야합니다.
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'delete_dormant_user'.")

        scheduler.add_job(
            update_ingredient_links,
            trigger=CronTrigger(day_of_week="0-6", hour="04", minute="00"),
            id="update_ingredient_links",  # id는 고유해야합니다.
            max_instances=1,
            replace_existing=True,
        )

        logger.info("Added job 'update_ingredient_links'.")
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="05", minute="00"
            ),  # 실행 시간입니다. 여기선 매주 월요일 3시에 실행합니다.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
