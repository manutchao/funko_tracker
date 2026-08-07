from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FunkoCreate(BaseModel):
    name: str
    barcode: str
    license: Optional[str] = None
    number: Optional[str] = None

class FunkoOut(FunkoCreate):
    id: str
    created_at: datetime
