import logging

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError

from user import models

from user import schemas
from user.password import hash_password

from core_exceptions import NotFoundException, BadRequestsException


class UserNotFound(NotFoundException):
    detail = 'User not found'


class UserAlreadyExists(BadRequestsException):
    pass


async def create(session: AsyncSession, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    session.add(db_user)
    try:
        await session.commit()
    except IntegrityError as exc:
        logging.warning('Handled IntegrityError', exc_info=exc)
        raise UserAlreadyExists(detail=f'User with email: {user.email}, already exists')
    await session.refresh(db_user)
    return db_user


async def reads(session: AsyncSession, skip, limit) -> [models.User]:
    expression = select(models.User).offset(skip).limit(limit)
    users = await session.exec(expression)
    return users.all()


async def read_by_id(session: AsyncSession, user_id) -> models.User | NotFoundException:
    expression = select(models.User).where(models.User.pk == user_id)
    user = (await session.exec(expression)).first()
    if not user:
        raise UserNotFound()
    return user


async def read_by_email(session: AsyncSession, user_email) -> models.User | NotFoundException:
    expression = select(models.User).where(models.User.email == user_email)
    user = (await session.exec(expression)).first()
    if not user:
        raise UserNotFound()
    return user


async def update_by_id(session: AsyncSession, user_id, user_data: dict) -> models.User | NotFoundException:
    user = await read_by_id(session, user_id)

    for key, value in user_data.items():
        setattr(user, key, value)
    await session.commit()
    await session.refresh(user)
    return user


async def delete_by_id(session: AsyncSession, user_id: int) -> bool | NotFoundException:
    user = await read_by_id(session, user_id)
    await session.delete(user)
    await session.commit()
    return True

