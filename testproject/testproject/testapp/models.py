from django.conf import settings
from django.db import models
from django.dispatch import receiver

from wiretap.models import Message
from wiretap.signals import post_save_message_response

class UserMessage(Message):
    """
    Example of `Message` subclass populated with app-specific data.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

@receiver(post_save_message_response)
def did_save_message_response(request, response, message, **kwargs):
    if request.user.is_anonymous():
        message.delete()
    else:
        user_message = UserMessage(
            message_ptr=message,
            user=request.user
        )
        user_message.__dict__.update(message.__dict__)
        user_message.save()
