"""
The following settings are meant to be used for a faked github.com OAuth
instance.  You should rename this file to 'local_settings.py' in order to use
it for the instance it resides in.

The are 2 main reasons for using local_settings.py when running locally:
    1. Disable CSRF protection (just not necessary when running on localhost)
    2. Disable file-based caching (who cares if things are slower when coding!)
        - Feel free to run with caching enabled locally, but it can cause
          headaches when developing because models, etc. are always changing so
          it doesn't serve a lot of purpose.
"""

def get_setting(setting):
    """
    Get a setting from settings.py
    """
    import settings
    return getattr(settings, setting)


# Development debug mode
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# You can get this token from github.com by doing the following:
#   - Login to your account
#   - Click 'Account Settings' at top
#   - Click 'Account Admin' on left (middle of page
#   - Copy/paste token under 'API Token' section below

# Replace with your own github API token to run locally and have faked OAuth
# instance always authorize as you
#GITHUB_API_TOKEN = ''

# Overrides for middleware to avoid having the CSRF protection when running
# locally
MIDDLEWARE_CLASSES = get_setting('MIDDLEWARE_CLASSES')
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# Disable caching
CACHES = get_setting('CACHES')
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
