import datetime
from chatbot import settings
from slack import WebClient
from slack.errors import SlackApiError
from django_slack_oauth.models import SlackOAuthRequest
from botuser.models import Send_Message, Schedule_Message
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


@receiver(post_save, sender=Send_Message)
def handle_Send_Message(sender, instance,created, **kwargs):
    if created == True:
        token = str(SlackOAuthRequest.objects.last())
        user = instance.is_user
        if user == True:
            client = WebClient(token=token)
        else:
            client = WebClient(
                token=settings.BOT_USER_ACCESS_TOKEN)
        try:
            if token == settings.OAUTH_ACCESS_TOKEN:
                response = client.chat_postMessage(
                    channel=instance.channel,
                    text=instance.text,
                    as_user=True,
                )
            elif user == True:
                response = client.chat_postMessage(
                    channel=instance.channel,
                    text=instance.text,
                    as_user=False,
                )
            else:
                response = client.chat_postMessage(
                    channel=instance.channel,
                    text=instance.text,
                )
        except:
            pass

@receiver(post_save, sender=Schedule_Message)
def handle_Schedule_Message(sender, instance, **kwargs):
    token = str(SlackOAuthRequest.objects.last())
    user = instance.is_user
    send_at = instance.post_at
    year = send_at.year
    month = send_at.month
    date = send_at.day
    hour = send_at.hour
    minute = send_at.minute
    epoch_time = datetime.datetime(
        year, month, date, hour, minute).timestamp()
    if user == True:
        client = WebClient(token=token)
    else:
        client = WebClient(
            token=settings.BOT_USER_ACCESS_TOKEN)
    if token == settings.OAUTH_ACCESS_TOKEN:
        response = client.chat_scheduleMessage(
            channel=instance.channel,
            text=instance.text,
            post_at=epoch_time,
            as_user=True,
        )
    elif user == True:
        response = client.chat_scheduleMessage(
            channel=instance.channel,
            text=instance.text,
            post_at=epoch_time,
            as_user=False,
        )
    else:
        response = client.chat_scheduleMessage(
            channel=instance.channel,
            text=instance.text,
            post_at=epoch_time,
        )