from fastapi import APIRouter
from fastapi import Depends

from fastapi.security import OAuth2PasswordRequestForm

from ..services.auth import AuthService, get_current_user
from ..models.auth import (
    Company,
    CompanyCreate,
    Token
)

router = APIRouter(
    prefix="/auth",
)


@router.post("/sing-up", response_model=Token)
def sing_up(
    company_data: CompanyCreate,
    service: AuthService = Depends(),
):
    return service.register_new_company(company_data)


@router.post("/sing-in", response_model=Token)
def sing_in(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(),
):
    return service.authenticate_company(
        form_data.username,
        form_data.password,
    )


@router.get("/user", response_model=Company)
def get_company(company: Company = Depends(get_current_user)):
    return company

