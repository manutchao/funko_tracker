from pydantic import BaseModel
from typing import Optional

class FunkoCreate(BaseModel):
    name: str
    barcode: str
    license: Optional[str] = None
    number: Optional[str] = None
