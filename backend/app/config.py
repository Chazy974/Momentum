import keyring
import urllib.parse

def get_secret(service, key):
    value = keyring.get_password(service, key)
    if not value:
        raise ValueError(f"Missing {key} in keyring for service '{service}'")
    return value

# Configuration dynamique depuis keyring
db_user = get_secret("MomentumDB", "user").lower()
db_password = get_secret("MomentumDB", "user_password")
db_name = get_secret("MomentumDB", "db_name")
host = "localhost"
port = "5432"

# Encodage sécurisé du mot de passe
encoded_password = urllib.parse.quote_plus(db_password)

# URL SQLAlchemy au format PostgreSQL
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{db_user}:{encoded_password}@{host}:{port}/{db_name}"

# Structure classique pour être utilisée dans Alembic (env.py)
class Settings:
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL

settings = Settings()
