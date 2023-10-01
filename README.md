This is a blog built with the Django Framework. 

for the markdown you need to install cdeditor. You can do this by going to your project root directory and then in the terminal -

> pip install django-ckeditor

in the settings.py, add
    
    'article',
    'account',
    'rest_framework'
    'ckeditor'

    to installed apps.

Also, add in your settings.py

    STATIC_URL = 'static/'

    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'assets'),)

    MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')
    MEDIA_URL = '/images/'
