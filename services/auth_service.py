from fastapi import HTTPException
from firebase_admin import auth

async def verify_firebase_token(token: str) -> str:
    """
    Verify Firebase JWT token and return the user ID
    """
    try:
        # Verify the token
        decoded_token = auth.verify_id_token(token)
        
        # Get user ID from token
        user_id = decoded_token['uid']
        
        return user_id
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication credentials: {str(e)}"
        )