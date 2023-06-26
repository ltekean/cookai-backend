import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from .models import User

logger = logging.getLogger(__name__)


def delete_dormant_user():
    # 실행시킬 Job
    # 여기서 정의하지 않고, import 해도 됨
    dormant_user = User.objects.filter(is_active=False)
    dormant_user.delete()
    print("operating")


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=2419_200):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class UserCommand(BaseCommand):
    help = "Runs delete_dormant_user."

    def start(self, *args, **options):
        scheduler = BackgroundScheduler(
            timezone=settings.TIME_ZONE
        )  # BlockingScheduler를 사용할 수도 있습니다.
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            delete_dormant_user,
            trigger=CronTrigger(minute="*/3"),
            id="delete_dormant_user",  # id는 고유해야합니다.
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'delete_dormant_user'.")

        scheduler.add_job(
            delete_old_job_executions,
            # trigger=CronTrigger(
            #     day_of_week="mon", hour="03", minute="00"
            # ),  # 실행 시간입니다. 여기선 매주 월요일 3시에 실행합니다.
            trigger=CronTrigger(minute="*/5"),
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
