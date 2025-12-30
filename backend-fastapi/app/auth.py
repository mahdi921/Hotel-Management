from fastapi import Request, HTTPException, Depends, Security
from sqlalchemy.orm import Session
from .database import get_db
from .models import DjangoSession, User
import json
import base64
from datetime import datetime

# Logic to decode Django session
# Django default session serializer is JSON (since 1.6+) but might be signed. 
# However, for shared DB, we just need to match session_key and check expiry.
# Getting user_id from session_data requires decoding. 
# Django's default session cookies are signed, but the DB stores base64 encoded string usually (if using standard serializer).
# Let's assume standard django.contrib.sessions.serializers.JSONSerializer logic for simplicity here 
# or use a simplified approach: we just check if key exists and is valid. 
# To get the USER ID, we need to decode.
# For this MVP, we will rely on a simpler 'get' from the decoded session data if possible,
# or we can use a helper library, but standard base64 decoding usually works for the _auth_user_id.

def get_user_from_session(session_key: str, db: Session):
    session = db.query(DjangoSession).filter(DjangoSession.session_key == session_key).first()
    if not session:
        return None
    
    if session.expire_date < datetime.now():
        return None

    # Decode session data
    # Format is usually: hash:base64encoded_json
    try:
        data = session.session_data
        encoded_data = data.split(":", 1)[1]
        decoded_json = base64.b64decode(encoded_data).decode("utf-8")
        session_dict = json.loads(decoded_json)
        user_id = session_dict.get("_auth_user_id")
        return user_id
    except Exception as e:
        print(f"Error decoding session: {e}")
        return None

async def get_current_user(request: Request, db: Session = Depends(get_db)):
    sessionid = request.cookies.get("sessionid")
    if not sessionid:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user_id = get_user_from_session(sessionid, db)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
         raise HTTPException(status_code=401, detail="User not found")
         
    return user
