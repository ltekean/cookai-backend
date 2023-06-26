import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from .coupang import update_ingredient_links

logger = logging.getLogger(__name__)


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_update_ingredient_links_executions(max_age=60 * 60 * 24 * 7):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class CoupangCommand(BaseCommand):
    help = "하루에 한번 쿠팡 링크를 업데이트합니다."

    def coupang_start(self, *args, **options):
        scheduler = BackgroundScheduler(
            timezone=settings.TIME_ZONE
        )  # BlockingScheduler를 사용할 수도 있습니다.
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            update_ingredient_links,
            # trigger=CronTrigger(day_of_week="0-7", hour="04", minute="00"),
            trigger=CronTrigger(minute="*/2"),
            id="update_ingredient_links",  # id는 고유해야합니다.
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'update_ingredient_links'.")

        scheduler.add_job(
            delete_old_update_ingredient_links_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="05", minute="00"
            ),  # 실행 시간입니다. 여기선 매주 월요일 3시에 실행합니다.
            id="delete_old_update_ingredient_links_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_update_ingredient_links_executions'."
        )

        try:
            logger.info("Starting Coupang scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping Coupang scheduler...")
            scheduler.shutdown()
            logger.info("Coupang Scheduler shut down successfully!")
