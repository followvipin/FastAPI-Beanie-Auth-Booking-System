# Import the necessary modules
import time
from typing import Dict
import jwt
from config.config import Settings

secret_key = Settings().secret_key


def token_response(token: str) -> Dict[str, str]:
    """
    Generates a response containing an access token.

    Args:
        token (str): The JWT token to include in the response.

    Returns:
        Dict[str, str]: A dictionary with the access token.
    """
    return {"access_token": token}


def sign_jwt(username: str) -> Dict[str, str]:
    """
    Generates a JWT token for the given username.

    Args:
        username (str): The user's identifier.

    Returns:
        Dict[str, str]: A dictionary containing the access token.
    """
    # Set the expiry time for the token.
    payload = {
        "user_id": username,
        "expires": time.time() + 86400,  # Expires in 24 hours
    }
    return token_response(jwt.encode(payload, secret_key, algorithm="HS256"))


def decode_jwt(token: str) -> dict:
    """
    Decodes a JWT token and returns the payload if it's valid.

    Args:
        token (str): The JWT token to decode.

    Returns:
        dict: The decoded payload if the token is valid and not expired, otherwise an empty dictionary.
    """
    decoded_token = jwt.decode(token.encode(), secret_key, algorithms=["HS256"])
    return decoded_token if decoded_token["expires"] >= time.time() else {}


def decode_jwt(token: str) -> dict:
    """
    Decodes a JWT token and returns the payload if it's valid.

    Args:
        token (str): The JWT token to decode.

    Returns:
        dict: The decoded payload if the token is valid and not expired, otherwise an empty dictionary.
    """
    decoded_token = jwt.decode(token.encode(), secret_key, algorithms=["HS256"])
    return decoded_token if decoded_token["expires"] >= time.time() else {}
