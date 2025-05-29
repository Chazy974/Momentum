import keyring

service = "MomentumDB"

print("admin_password =", repr(keyring.get_password(service, "admin_password")))
print("user_password  =", repr(keyring.get_password(service, "user_password")))
