from src.supabase_client import admin_supabase, create_user_client
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    

    try:
        response = admin_supabase.auth.get_user(token)

    except Exception:
        

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    if response.user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid user"
        )

    user_client = create_user_client(token)

    return response.user, user_client