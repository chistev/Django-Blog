This is a blog built with the Django Framework. 

in the settings.py, add

    'account',
    'article',
    'rest_framework'

    to installed apps.

Also, add

    STATIC_URL = 'static/'

    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'assets'),)

    MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')
    MEDIA_URL = '/images/'
