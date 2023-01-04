import os
import logging
from typing import Any, List, Union

from airflow.configuration import conf
from airflow.www.fab_security.manager import AUTH_DB, AUTH_OAUTH
from airflow.www.security import AirflowSecurityManager

log = logging.getLogger(__name__)
log.setLevel(os.getenv("AIRFLOW__LOGGING__FAB_LOGGING_LEVEL", "INFO"))
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
AUTH_USER_REGISTRATION_ROLE = "Viewer"
# If we should replace ALL the user's roles each login, or only on registration
AUTH_ROLES_SYNC_AT_LOGIN = True
FAB_SECURITY_MANAGER_CLASS = "webserver_config.OauthAuthorizer"
AUTH_ROLES_MAPPING = {
    "User": ["User"],
    "Admin": ["Admin"],
}

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
        # "whitelist": ["@{}".format(os.getenv("GOOGLE_DOMAIN"))],
    },
    {
        "name": "github",
        "icon": "fa-github",
        "token_key": "access_token",
        "remote_app": {
            "client_id": os.getenv("GITHUB_CLIENT_ID"),
            "client_secret": os.getenv("GITHUB_CLIENT_SECRET"),
            "api_base_url": "https://api.github.com",
            "client_kwargs": {"scope": "read:user, read:org"},
            "access_token_url": "https://github.com/login/oauth/access_token",
            "authorize_url": "https://github.com/login/oauth/authorize",
            "request_token_url": None,
        },
    },
]


def email_to_role_keys(email: str) -> List[str]:
    """Maps an email to role_keys"""
    ADMIN_EMAILS = ["ashpreet@phidata.com"]
    if email in ADMIN_EMAILS:
        log.info(f"User {email} is an Admin")
        return ["Admin"]
    else:
        return ["User"]


def github_team_parser(team_payload):
    # Parse the team payload from GitHub
    log.info(f"Team payload: {team_payload}")
    return [team["id"] for team in team_payload]


def github_map_roles(team_list):
    # Associate the team IDs with Roles here.
    # The expected output is a list of roles that FAB will use to Authorize the user.

    team_role_map = {
        "data-platform-admins": "Admin",
        "data-platform-users": "User",
    }
    return list(set(team_role_map.get(team, "Viewer") for team in team_list))


class OauthAuthorizer(AirflowSecurityManager):

    # For other providers:
    # https://github.com/dpgaspar/Flask-AppBuilder/blob/master/flask_appbuilder/security/manager.py#L550
    def get_oauth_user_info(
        self, provider: str, resp: Any
    ) -> dict[str, Union[str, list[str]]]:

        log.info(f"Getting user info from {provider}")
        # log.info(f"Response: {resp}")

        if provider == "google":
            me = self.appbuilder.sm.oauth_remotes[provider].get("userinfo")
            user_data = me.json()
            # log.info(f"User info from Google: {user_data}")
            return {
                "username": "google_" + user_data.get("id", ""),
                "first_name": user_data.get("given_name", ""),
                "last_name": user_data.get("family_name", ""),
                "email": user_data.get("email", ""),
                "role_keys": email_to_role_keys(user_data.get("email", "")),
            }
        elif provider == "github":
            remote_app = self.appbuilder.sm.oauth_remotes[provider]
            me = remote_app.get("user")
            user_data = me.json()
            team_data = remote_app.get("user/teams")
            teams = github_team_parser(team_data.json())
            roles = github_map_roles(teams)
            log.debug(
                f"User info from Github: {user_data}\nTeam info from Github: {teams}"
            )
            return {"username": "github_" + user_data.get("login"), "role_keys": roles}
        else:
            return {}


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
