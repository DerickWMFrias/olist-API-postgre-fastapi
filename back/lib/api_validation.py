from fastapi import Header, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from dbconfig.conn import get_dbconn
from models.schemas import Keys

def validate_api_key(
    x_api_key: str = Header(..., alias="X-API-Key"),
    dbconn: Session = Depends(get_dbconn),
):
    key = (
        dbconn.query(Keys)
        .filter(Keys.key_text == x_api_key)
        .first()
    )

    if not key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )

    if key.is_revoked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key revoked"
        )

    if key.expires_at_tmzone <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key expired"
        )

    return key 
