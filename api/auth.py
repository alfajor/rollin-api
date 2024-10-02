from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyQuery
from db.db import check_api_key

api_key_query = APIKeyQuery(name="api_key", auto_error=False)

def api_key_auth(api_key_query: str = Security(api_key_query)):
    user_api_key = check_api_key(api_key_query)

    if user_api_key:
        return user_api_key
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")