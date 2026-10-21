
import logging
import traceback
from datetime import datetime, timedelta

import phonenumbers
from fastapi import APIRouter, Depends, HTTPException, Response, Cookie, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from ..models.db import get_db, User
from ..schemas import User as UserSchema
from ..config import settings
from ..services.otp import (
    generate_otp,
    send_otp_sms,
    store_otp,
    verify_otp,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])

logger = logging.getLogger(__name__)


# -----------------------------
# Request schemas
# -----------------------------

class SendOTPRequest(BaseModel):
    phone_number: str = Field(min_length=5, max_length=20)


class VerifyOTPRequest(BaseModel):
    phone_number: str = Field(min_length=5, max_length=20)
    otp: str = Field(pattern=r"^\d{6}$")


# -----------------------------
# Phone number normalization
# -----------------------------

def normalize_phone_number(phone_number: str) -> str:
    """
    Accept international numbers such as +919019830973.
    Also accept 10-digit Indian numbers without +91.
    Return the normalized E.164 number.
    """
    phone_number = phone_number.strip()

    try:
        if phone_number.startswith("+"):
            parsed = phonenumbers.parse(phone_number, None)
        else:
            # Support local Indian mobile numbers from the +91 login UI.
            digits = "".join(ch for ch in phone_number if ch.isdigit())

            if len(digits) == 10:
                parsed = phonenumbers.parse(digits, "IN")
            elif len(digits) == 12 and digits.startswith("91"):
                parsed = phonenumbers.parse("+" + digits, None)
            else:
                raise ValueError("Include the country code.")

        if not phonenumbers.is_valid_number(parsed):
            raise ValueError("The phone number is not valid.")

        return phonenumbers.format_number(
            parsed,
            phonenumbers.PhoneNumberFormat.E164,
        )

    except (phonenumbers.NumberParseException, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number. Include a valid country code.",
        ) from exc


# -----------------------------
# JWT authentication
# -----------------------------

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    payload = data.copy()

    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=15)
    )

    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def get_current_user(
    token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        phone_number = payload.get("sub")

        if not phone_number:
            raise credentials_exception

    except JWTError as exc:
        raise credentials_exception from exc

    user = (
        db.query(User)
        .filter(User.phone_number == phone_number)
        .first()
    )

    if user is None:
        raise credentials_exception

    return user


# -----------------------------
# Send OTP
# -----------------------------

@router.post("/send-otp")
def send_otp(req: SendOTPRequest):
    formatted_number = normalize_phone_number(req.phone_number)

    try:
        otp = generate_otp()
        store_otp(formatted_number, otp)
        send_otp_sms(formatted_number, otp)

        logger.info("OTP generated successfully for %s", formatted_number)

        return {"message": "OTP sent successfully"}

    except Exception as exc:
        logger.exception("Failed to process OTP request")

        # Avoid exposing internal exception details to the client.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not process OTP. Check the backend terminal.",
        ) from exc


# -----------------------------
# Verify OTP and log in
# -----------------------------

@router.post("/verify-otp")
def verify_otp_endpoint(
    req: VerifyOTPRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    formatted_number = normalize_phone_number(req.phone_number)

    try:
        is_valid = verify_otp(formatted_number, req.otp)
    except Exception as exc:
        logger.exception("OTP verification failed unexpectedly")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not verify OTP. Check the backend terminal.",
        ) from exc

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired OTP",
        )

    try:
        user = (
            db.query(User)
            .filter(User.phone_number == formatted_number)
            .first()
        )

        if user is None:
            user = User(phone_number=formatted_number)
            db.add(user)
            db.commit()
            db.refresh(user)

        expires_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

        access_token = create_access_token(
            data={"sub": user.phone_number},
            expires_delta=timedelta(minutes=expires_minutes),
        )

        response.set_cookie(
            key="token",
            value=access_token,
            httponly=True,
            max_age=expires_minutes * 60,
            samesite="lax",
            secure=False,  # Local HTTP development only.
            path="/",
        )

        return {"message": "Login successful"}

    except Exception as exc:
        db.rollback()
        logger.exception("Login or user database operation failed")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed. Check the backend terminal.",
        ) from exc


# -----------------------------
# Logout
# -----------------------------

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="token",
        path="/",
        httponly=True,
        samesite="lax",
    )

    return {"message": "Logged out successfully"}


# -----------------------------
# Current user
# -----------------------------

@router.get("/me", response_model=UserSchema)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
