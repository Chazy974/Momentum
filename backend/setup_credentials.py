import keyring

print("🔐 Configuration des identifiants PostgreSQL pour Momentum")

service = "MomentumDB"

admin_user = input("Nom d'utilisateur admin PostgreSQL (ex: postgres) : ")
admin_password = input("Mot de passe admin PostgreSQL : ")
user = input("Nom du nouvel utilisateur pour Momentum (ex: momentum_user) : ")
user_password = input("Mot de passe de ce nouvel utilisateur : ")
db_name = input("Nom de la base de données à créer (ex: momentum) : ")

keyring.set_password(service, "admin_user", admin_user)
keyring.set_password(service, "admin_password", admin_password)
keyring.set_password(service, "user", user)
keyring.set_password(service, "user_password", user_password)
keyring.set_password(service, "db_name", db_name)

print("✅ Identifiants enregistrés avec succès dans le keyring.")