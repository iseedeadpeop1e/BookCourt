from datetime import datetime, timedelta

from fastapi import HTTPException, Depends
from fastapi import status
from fastapi.security import OAuth2PasswordBearer

from jose import (
    JWTError,
    jwt,
)
from passlib.hash import bcrypt
from pydantic import ValidationError

from .. import tables
from ..database import get_session, Session
from ..models.auth import Company, CompanyCreate
from ..models.auth import Token
from ..settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sing-in")


def get_current_user(token: str = Depends(oauth2_scheme)) -> Company:
    return AuthService.validate_token(token)


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def validate_token(cls, token: str) -> Company:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm]
            )
        except JWTError:
            raise exception from None

        company_data = payload.get("company")

        try:
            company = Company.parse_obj(company_data)
        except ValidationError:
            raise exception from None

        return company

    @classmethod
    def create_token(cls, company: tables.Company) -> Token:
        company_data = Company.from_orm(company)

        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expiration),
            'sub': str(company_data.id),
            'company': company_data.dict(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )

        return Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_company(self, company_data: CompanyCreate) -> Token:
        company = tables.Company(
            email=company_data.email,
            company_name=company_data.company_name,
            password_hash=self.hash_password(company_data.password),
            phone_number=company_data.phone_number,
            address=company_data.address,
            created_at=company_data.created_at,
        )

        self.session.add(company)
        self.session.commit()

        return self.create_token(company)

    def authenticate_company(self, email: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )
        company = (
            self.session
            .query(tables.Company)
            .filter(tables.Company.email == email)
            .first()
        )

        if not company:
            raise exception

        if not self.verify_password(password, company.password_hash):
            raise exception

        return self.create_token(company)
