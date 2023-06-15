from users.models import User


def delete_dormant_user():
    dormant_user = User.objects.filter(is_active=False)
    dormant_user.delete()
    print("operating")
