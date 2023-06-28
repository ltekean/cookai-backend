from django.apps import AppConfig
from django.conf import settings


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from . import operator

            operator.delete_dormant_user_start()
            operator.update_ingredient_links_start()
            operator.delete_old_job_executions_start()

    # 한번 불려야 하는데 두번 불림.
    # 두번 불리는 이유: https://stackoverflow.com/questions/33814615/how-to-avoid-appconfig-ready-method-running-twice-in-django
    #  Reload와 main 두가지 프로세스가 뜬다고 함.
    #  또는 python manage.py runserver --noreload  로 실행하면 됨.
