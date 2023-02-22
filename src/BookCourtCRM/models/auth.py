from pydantic import BaseModel


class CompanyBase(BaseModel):
    company_name: str
    email: str
    phone_number: str
    address: str
    created_at: int


class CompanyCreate(CompanyBase):
    password: str


class Company(CompanyBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
