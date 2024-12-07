import os

current_dir = os.path.abspath(os.path.dirname(__file__))
keycloak_dir = os.path.join(current_dir, "keycloak")
opentdf_dir = os.path.join(current_dir, "opentdf")

# Most common options to change
BRAND_NAME = "yourbrand"
TLD = ".org"
LOCAL_SERVER_mDNS = "localhost"
SERVICES_TO_RUN = ["keycloak", "org", "opentdf", "AICouncil", "nginx-proxy"]
VITE_GOOGLE_CLIENT_ID = "<YOUR GOOGLE OAUTH CLIENT ID>"
VITE_GITHUB_CLIENT_ID = "<YOUR GITHUB OAUTH CLIENT ID>"
VITE_KAS_ENDPOINT = "https://opentdf/kas"
PEM_FILE = "<YOUR SECRET HERE>"
SERVER_USER = "<YOUR SECRET HERE>"
SERVER_HOST = "<YOUR SECRET HERE>"
REMOTE_FOLDER = "<YOUR SECRET HERE>"
ZIP_FILE = "<YOUR SECRET HERE>"
LOCAL_DESTINATION = "<YOUR SECRET HERE>"
EXTRACT_FOLDER = "<YOUR SECRET HERE>"  # Name of the folder after extraction

# More public options
COMPOSE_PROJECT_NAME = BRAND_NAME

# Google OAuth Config
VITE_GOOGLE_SCOPES = "openid profile email"
VITE_GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
VITE_GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"

# GitHub OAuth Config
VITE_GITHUB_SCOPES = "openid profile email"
VITE_GITHUB_AUTH_ENDPOINT = "https://github.com/login/oauth/authorize"
VITE_GITHUB_TOKEN_ENDPOINT = "https://github.com/login/oauth/access_token"

# Keycloak Config
KEYCLOAK_REALM = "opentdf"
KEYCLOAK_HOST = "https://localhost:8888"
KEYCLOAK_SERVER_URL = KEYCLOAK_HOST
VITE_KEYCLOAK_AUTH_ENDPOINT = (
    f"{KEYCLOAK_HOST}/auth/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth"
)
VITE_KEYCLOAK_TOKEN_ENDPOINT = (
    f"{KEYCLOAK_HOST}/auth/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
)
VITE_KEYCLOAK_USERINFO_ENDPOINT = (
    f"{KEYCLOAK_HOST}/auth/realms/{KEYCLOAK_REALM}/protocol/openid-connect/userinfo"
)
VITE_KEYCLOAK_SERVER_URL = KEYCLOAK_HOST + "/auth"
VITE_KEYCLOAK_CLIENT_ID = BRAND_NAME
VITE_KEYCLOAK_REALM = "opentdf"

# Admin Config
ADMIN_CLIENT = "admin-cli"
KEYCLOAK_ADMIN = "admin"

# Git Branch Port Config
# BRANCH="$(git rev-parse --abbrev-ref HEAD)"
VITE_PUBLIC_URL = BRAND_NAME + TLD
VITE_LOCAL_PORT = ":3001"

# EC2 Metadata Check
VITE_PUBLIC_URL_ON_EC2 = "localhost"

# Server URLs
VITE_FRONTEND_SERVER_URL = f"https://{VITE_PUBLIC_URL}{VITE_LOCAL_PORT}"

# Redirects
VITE_GOOGLE_REDIRECT_URI = f"https://{VITE_PUBLIC_URL}{VITE_LOCAL_PORT}"
VITE_GITHUB_REDIRECT_URI = f"https://{VITE_PUBLIC_URL}{VITE_LOCAL_PORT}"
VITE_KEYCLOAK_REDIRECT_URI = f"https://{VITE_PUBLIC_URL}{VITE_LOCAL_PORT}"
KEYCLOAK_REDIRECT_URI = f"{VITE_KEYCLOAK_REDIRECT_URI}"
VITE_ORG_BACKEND_URL = "https://org-backend:8085"

# Opentdf config
opentdfdb = dict(
    image='postgres:15-alpine',
    detach=True,
    name="opentdfdb",
    network=BRAND_NAME,
    restart_policy={"Name": "always"},
    user="postgres",
    environment={
        "POSTGRES_PASSWORD": "changeme",
        "POSTGRES_USER": "postgres",
        "POSTGRES_DB": "keycloak",
    },
    volumes={
        "POSTGRES_DATA_VOLUME": {"bind": "/var/lib/postgresql/data", "mode": "rw"}
    },
    healthcheck={
        "test": ["CMD-SHELL", "pg_isready"],
        "interval": 5000000000,  # 5s in nanoseconds
        "timeout": 5000000000,  # 5s in nanoseconds
        "retries": 10,
    }
)

opentdf = dict(
    image="julianfl0w/opentdf:1.0",
    detach=True,
    command="start",
    name="opentdf",
    network=BRAND_NAME,
    restart_policy={"Name": "always"},
    ports={"8080/tcp": 8080},
    environment={"KEYCLOAK_BASE_URL": KEYCLOAK_SERVER_URL},
    volumes={
        f"{opentdf_dir}/opentdf.yaml": {"bind": "/app/opentdf.yaml", "mode": "ro"},
        f"{opentdf_dir}": {"bind": "/keys", "mode": "ro"},
        f"{opentdf_dir}/kas-cert.pem": {"bind": "/app/kas-cert.pem", "mode": "ro"},
        f"{opentdf_dir}/kas-ec-cert.pem": {"bind": "/app/kas-ec-cert.pem", "mode": "ro"},
        f"{opentdf_dir}/kas-private.pem": {"bind": "/app/kas-private.pem", "mode": "ro"},
        f"{opentdf_dir}/kas-ec-private.pem": {"bind": "/app/kas-ec-private.pem", "mode": "ro"},
    },
    healthcheck={
        "test": ["CMD-SHELL", f"curl -sf {KEYCLOAK_SERVER_URL} || exit 1"],
        "interval": 10000000000,  # 10s in nanoseconds
        "timeout": 5000000000,  # 5s in nanoseconds
        "retries": 5,
    }
)

# Keycloak config
keycloakdb = opentdfdb.copy()
keycloakdb["name"] = "keycloakdb"

keycloak = {
    "name": "keycloak",
    "image": "cgr.dev/chainguard/keycloak@sha256:37895558d2e0e93ffff75da5900f9ae7e79ec6d1c390b18b2ecea6cee45ec26f",
    "entrypoint": "/opt/keycloak/keycloak-startup.sh",
    "detach":True,
    "volumes": {
        os.path.join(keycloak_dir, "keys/localhost.crt"): {
            "bind": "/etc/x509/tls/localhost.crt",
            "mode": "ro",  # Read-only
        },
        os.path.join(keycloak_dir, "keys/localhost.key"): {
            "bind": "/etc/x509/tls/localhost.key",
            "mode": "ro",  # Read-only
        },
        os.path.join(keycloak_dir, "keys/ca.jks"): {
            "bind": "/truststore/truststore.jks",
            "mode": "ro",  # Read-only
        },
        os.path.join(keycloak_dir, "realms"): {
            "bind": "/opt/keycloak/realms",
            "mode": "ro",  # Read-only
        },
        os.path.join(keycloak_dir, "oauth_certs"): {
            "bind": "/opt/keycloak/oauth_certs",
            "mode": "ro",  # Read-only
        },
        os.path.join(keycloak_dir, "keycloak-startup.sh"): {
            "bind": "/opt/keycloak/keycloak-startup.sh",
            "mode": "ro",  # Read-only
        },
    },
    "environment": {
        "KC_PROXY": "edge",
        "KC_HTTP_RELATIVE_PATH": "/auth",
        "KC_DB_VENDOR": "postgres",
        "KC_DB_URL_HOST": "keycloakdb",
        "KC_DB_URL_PORT": "5432",
        "KC_DB_URL_DATABASE": "keycloak",
        "KC_DB_USERNAME": "keycloak",
        "KC_DB_PASSWORD": "changeme",
        "KC_HOSTNAME_STRICT": "false",
        "KC_HOSTNAME_STRICT_BACKCHANNEL": "false",
        "KC_HOSTNAME_STRICT_HTTPS": "false",
        "KC_HTTP_ENABLED": "true",
        "KC_HTTP_PORT": "8888",
        "KC_HTTPS_PORT": "8443",
        "KEYCLOAK_ADMIN": "admin",
        "KEYCLOAK_ADMIN_PASSWORD": "changeme",
        "KEYCLOAK_FRONTEND_URL": "https://$KEYCLOAK_FRONTEND_URL/auth",
        "KC_HOSTNAME_URL": "https://$KEYCLOAK_FRONTEND_URL/auth",
        "KC_FEATURES": "preview,token-exchange",
        "KC_HEALTH_ENABLED": "true",
        "KC_HTTPS_KEY_STORE_PASSWORD": "password",
        "KC_HTTPS_KEY_STORE_FILE": "/truststore/truststore.jks",
        "KC_HTTPS_CERTIFICATE_FILE": "/etc/x509/tls/localhost.crt",
        "KC_HTTPS_CERTIFICATE_KEY_FILE": "/etc/x509/tls/localhost.key",
        "KC_HTTPS_CLIENT_AUTH": "request",
    },
}


# Secrets
GOOGLE_CLIENT_SECRET = "<YOUR SECRET HERE>"
GITHUB_CLIENT_SECRET = "<YOUR SECRET HERE>"
KEYCLOAK_ADMIN_PASSWORD = "changeme"