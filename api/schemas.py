from pydantic import BaseModel

class Company(BaseModel):
    company_name: str
    ebitda_source: str
    cif_source: str
    cif: str
    ebitda_2023: float

    class Config:
        orm_mode = True