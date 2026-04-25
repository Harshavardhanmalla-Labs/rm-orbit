from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import uuid
import datetime
import os
import base64
from cryptography.fernet import Fernet

from app.database import get_db
from app.models import Secret

router = APIRouter()

# For a production wallet component, secrets need to be encrypted before rest.
MASTER_KEY = os.getenv("MASTER_ENCRYPTION_KEY", Fernet.generate_key().decode('utf-8'))
f = Fernet(MASTER_KEY.encode('utf-8'))

class SecretCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    value: str

class SecretOut(BaseModel):
    id: str
    org_id: str
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True

class SecretRevealOut(SecretOut):
    value: str

def get_org_id(x_org_id: Optional[str] = Header(None)) -> str:
    if not x_org_id:
        return "default_org"
    return x_org_id

@router.get("/", response_model=List[SecretOut])
def list_secrets(org_id: str = Depends(get_org_id), db: Session = Depends(get_db)):
    return db.query(Secret).filter(Secret.org_id == org_id).all()

@router.post("/", response_model=SecretOut)
def create_secret(sec: SecretCreate, org_id: str = Depends(get_org_id), db: Session = Depends(get_db)):
    # Encrypt the value
    encrypted = f.encrypt(sec.value.encode('utf-8'))
    
    new_sec = Secret(
        id=str(uuid.uuid4()),
        org_id=org_id,
        name=sec.name,
        description=sec.description,
        encrypted_value=encrypted.decode('utf-8'),
        iv_material="static_fernet" # Using fernet which handles IV natively
    )
    db.add(new_sec)
    db.commit()
    db.refresh(new_sec)
    return new_sec

@router.get("/{secret_id}/reveal", response_model=SecretRevealOut)
def reveal_secret(secret_id: str, org_id: str = Depends(get_org_id), db: Session = Depends(get_db)):
    sec = db.query(Secret).filter(Secret.id == secret_id, Secret.org_id == org_id).first()
    if not sec:
        raise HTTPException(status_code=404, detail="Secret not found")
    
    decrypted = f.decrypt(sec.encrypted_value.encode('utf-8')).decode('utf-8')
    
    return {
        "id": sec.id,
        "org_id": sec.org_id,
        "name": sec.name,
        "description": sec.description,
        "value": decrypted,
        "created_at": sec.created_at,
        "updated_at": sec.updated_at
    }

@router.delete("/{secret_id}")
def delete_secret(secret_id: str, org_id: str = Depends(get_org_id), db: Session = Depends(get_db)):
    sec = db.query(Secret).filter(Secret.id == secret_id, Secret.org_id == org_id).first()
    if not sec:
        raise HTTPException(status_code=404, detail="Secret not found")
    
    db.delete(sec)
    db.commit()
    return {"status": "deleted"}
