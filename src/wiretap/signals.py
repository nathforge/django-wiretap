import django.dispatch

post_save_message_request = django.dispatch.Signal(
    providing_args=['request', 'message']
)

post_save_message_response = django.dispatch.Signal(
    providing_args=['request', 'response', 'message']
)
