from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in)
def user_logged_in_receiver(sender, user, request, **kwargs):
    user.update_last_login()

@receiver(request_finished)
def user_last_request(sender, **kwargs):
    loggedIn = LoggedInUser()
    if loggedIn.current_user:
        user = CustomUser.objects.get(username=loggedIn.current_user)
        user.last_request = datetime.datetime.now()
        user.save()