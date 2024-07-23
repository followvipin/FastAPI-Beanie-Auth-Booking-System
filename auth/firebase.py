"""this module provides the bearer function for the google authentication if you want to use 
this you need give it a proper wroking firebase key."""

# from firebase_admin import credentials, auth, initialize_app
# from fastapi import HTTPException, Header

# cred = credentials.Certificate("path/to/key.json")
# initialize_app(cred)

# async def get_current_user(authorization: str = Header(...)) -> str:
#     """
#     Retrieves the current user based on the session token in the authorization header.

#     Args:
#         authorization (str): The authorization header containing the session token.

#     Returns:
#         dict: A dictionary containing the user ID and decoded claims.
#     """
#     if authorization is None or not authorization.startswith("Bearer "):
#         return {"error": "invalid authorization header"}
#     session_token = authorization[7:]
#     if not session_token:
#         raise HTTPException(status_code=401, detail="Not authenticated")
#     try:
#         decoded_claims = auth.verify_id_token(session_token)
#         user_id = decoded_claims.get("user_id")

#         if not user_id:
#             raise HTTPException(status_code=401, detail="Invalid session cookie")
#         return {"user_id": user_id, "decoded_claims": decoded_claims}
#     except auth.InvalidSessionCookieError:
#         raise HTTPException(status_code=401, detail="Invalid session cookie")
