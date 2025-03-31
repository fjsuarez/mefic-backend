import logging
from fastapi import HTTPException
from firebase_admin import auth

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify_firebase_token(token: str) -> str:
    """
    Verify Firebase JWT token and return the user ID
    """
    try:
        logger.info(f"Attempting to verify token: {token[:10]}...")
        
        # Verify the token
        decoded_token = auth.verify_id_token(token)
        
        # Get user ID from token
        user_id = decoded_token['uid']
        logger.info(f"Successfully verified token for user: {user_id}")
        
        return user_id
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        # Log more details about the token
        if token:
            logger.error(f"Token prefix: {token[:15]}..., Length: {len(token)}")
        else:
            logger.error("Token is empty or None")
            
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication credentials: {str(e)}"
        )