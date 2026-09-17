import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv(".envi")

DATABASE_URL = os.getenv("DATABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")
SUPABASE_PUBLIC_KEY = os.getenv("SUPABASE_PUBLIC_KEY")


if not DATABASE_URL or not SUPABASE_SECRET_KEY or not SUPABASE_PUBLIC_KEY:
    raise ValueError("Supabase environment variables are missing.")

# Admin privilged client - For Server only operations
admin_supabase : Client = create_client(

    DATABASE_URL,
    SUPABASE_SECRET_KEY
)

def create_user_client(access_token: str) -> Client:
    client = create_client(
        DATABASE_URL,
        SUPABASE_PUBLIC_KEY
    )

    client.postgrest.auth(access_token)

    return client

