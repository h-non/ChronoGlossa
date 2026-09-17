from src.supabase_client import admin_supabase


response = admin_supabase.auth.sign_in_with_password(
    {
        "email": "trythingsig@gmail.com",
        "password" : "yippieewetestin1"

        })

print("Logged in: ",response.user.id)


token1 = response.session.access_token
print(len(token1))
admin_supabase.auth.get_user(token1)

import hashlib

print("TOKEN HASH:", hashlib.sha256(token1.encode()).hexdigest())
print("TOKEN LENGTH:", len(token1))
print(token1)
with open("token.txt", "w") as file:
    file.write(token1)

print("Token saved to token.txt")
admin_supabase.auth.get_user(token1)