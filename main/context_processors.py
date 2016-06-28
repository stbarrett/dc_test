from django.conf import settings # import the settings file

def settings(request):
    from django.conf import settings
    return {
            'AFFILIATE_ID': settings.AFFILIATE_ID,
            'MEDIA_URL': settings.MEDIA_URL,
            'DEBUG': settings.DEBUG
            }
