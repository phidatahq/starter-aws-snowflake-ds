import os

from airflow.configuration import conf
from airflow.www.fab_security.manager import AUTH_DB, AUTH_OAUTH

basedir = os.path.abspath(os.path.dirname(__file__))

# Enable Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True
CSRF_ENABLED = True

# The SQLAlchemy connection string
SQLALCHEMY_DATABASE_URI = conf.get("database", "SQL_ALCHEMY_CONN")

# ----------------------------------------------------
# AUTHENTICATION CONFIG
# ----------------------------------------------------
# For details on how to set up each of the following authentication, see
# http://flask-appbuilder.readthedocs.io/en/latest/security.html#authentication-methods
# for details.

# The authentication types
# AUTH_OID : Is for OpenID
# AUTH_DB : Is for database
# AUTH_LDAP : Is for LDAP
# AUTH_REMOTE_USER : Is for using REMOTE_USER from web server
# AUTH_OAUTH : Is for OAuth

# Use OAUTH i.e. Google, Facebook, GitHub authentication
AUTH_TYPE = AUTH_OAUTH
# Allow user self registration
AUTH_USER_REGISTRATION = True
# The default user self registration role
AUTH_USER_REGISTRATION_ROLE = "Admin"
# If we should replace ALL the user's roles each login, or only on registration
AUTH_ROLES_SYNC_AT_LOGIN = True

# Enable Google OAuth
OAUTH_PROVIDERS = [
    {
        "name": "google",
        "icon": "fa-google",
        "token_key": "access_token",
        "remote_app": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "api_base_url": "https://www.googleapis.com/oauth2/v2/",
            "client_kwargs": {"scope": "email profile"},
            "request_token_url": None,
            "access_token_url": "https://accounts.google.com/o/oauth2/token",
            "authorize_url": "https://accounts.google.com/o/oauth2/auth",
            "jwks_uri": "https://www.googleapis.com/oauth2/v3/certs",
        },
        "whitelist": ["@{}".format(os.getenv("GOOGLE_DOMAIN"))],
    }
]

# ----------------------------------------------------
# Theme CONFIG
# ----------------------------------------------------
# Flask App Builder comes up with a number of predefined themes
# that you can use for Apache Airflow.
# http://flask-appbuilder.readthedocs.io/en/latest/customizing.html#changing-themes
# Please make sure to remove "navbar_color" configuration from airflow.cfg
# in order to fully utilize the theme. (or use that property in conjunction with theme)
# APP_THEME = "bootstrap-theme.css"  # default bootstrap
# APP_THEME = "amelia.css"
# APP_THEME = "cerulean.css"
# APP_THEME = "cosmo.css"
# APP_THEME = "cyborg.css"
# APP_THEME = "darkly.css"
# APP_THEME = "flatly.css"
# APP_THEME = "journal.css"
# APP_THEME = "lumen.css"
# APP_THEME = "paper.css"
# APP_THEME = "readable.css"
# APP_THEME = "sandstone.css"
# APP_THEME = "simplex.css"
# APP_THEME = "slate.css"
# APP_THEME = "solar.css"
# APP_THEME = "spacelab.css"
# APP_THEME = "superhero.css"
# APP_THEME = "united.css"
# APP_THEME = "yeti.css"
