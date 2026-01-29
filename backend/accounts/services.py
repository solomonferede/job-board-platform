from .models import User


def deactivate_user(user: User):
    user.is_active = False
    user.save(update_fields=["is_active"])
