# Import necessary  modules
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Import custom JWT handler (assuming it's in a module called "auth.jwt_handler")
from auth.jwt_handler import decode_jwt


def verify_jwt(jwtoken: str) -> bool:
    """
    Verifies the validity of a JWT (JSON Web Token).

    Args:
        jwtoken (str): The JWT to verify.

    Returns:
        bool: True if the token is valid, False otherwise.
    """
    isTokenValid: bool = False
    # Decode the JWT payload
    payload = decode_jwt(jwtoken)  
    # Printing the decoded payload for debugging purposes.
    print(payload)  
    if payload:
        isTokenValid = True
    return isTokenValid



class JWTBearer(HTTPBearer):
    """
    Custom FastAPI dependency for JWT (JSON Web Token) authentication.

    Args:
        auto_error (bool, optional): Whether to raise an HTTPException if authentication fails. Defaults to True.
    """

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """
        Validates the JWT from the request.

        Args:
            request (Request): The incoming request.

        Returns:
            str: The valid JWT token.
        """
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        print("Credentials:", credentials)  # Printing the decoded payload for debugging purposes.
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication token")

            if not verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token")

            return credentials.credentials

