from datetime import timedelta, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db.models.user import User, RefreshToken
from src.services.auth import AuthUtilitiesService


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int):
        stmt = await self.session.execute(select(User).where(User.id == user_id))
        user = stmt.scalar_one_or_none()
        return user

    async def get_user_by_name(self, username: str):
        stmt = await self.session.execute(select(User).where(User.username == username))
        user = stmt.scalar_one_or_none()
        return user

    async def get_current_user(self, payload):
        try:
            user_id = payload.get("sub")
            stmt = await self.session.execute(select(User).where(User.id == int(user_id)))
            user = stmt.scalar_one_or_none()
            return user
        except AttributeError:
            return None

    async def create_refresh_token(self, user_id: int) -> RefreshToken:
        refresh_token = RefreshToken(
            token=AuthUtilitiesService.generate_refresh_token(),
            user_id=user_id,
            expires_at=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        self.session.add(refresh_token)
        await self.session.commit()
        await self.session.refresh(refresh_token)
        return refresh_token

    async def user_register(self, user: User) -> User:
        hashed_password = AuthUtilitiesService.get_password_hash(user.password)
        new_user = User(username=user.username, password=hashed_password)
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def user_refresh_token(self, user_id: int):
        existing_token = await self.session.execute(
            select(RefreshToken).where(RefreshToken.user_id == user_id)
        )
        existing_token = existing_token.scalar_one_or_none()

        if existing_token:
            await self.session.delete(existing_token)
            await self.session.commit()
        new_token = RefreshToken(
            token=AuthUtilitiesService.generate_refresh_token(),
            user_id=user_id,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        self.session.add(new_token)
        await self.session.commit()
        await self.session.refresh(new_token)

    async def auth_user(self, username: str):
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def check_and_get_refresh_token(self, refresh_token: str):
        stmt = await self.session.execute(
            select(RefreshToken).where(RefreshToken.token == refresh_token)
        )
        existing_token = stmt.scalar_one_or_none()
        return existing_token

    async def get_user_by_refresh_token(self, refresh_token: str):
        user_stmt = await self.session.execute(
            select(User).where(User.id == refresh_token.user_id)
        )
        user = user_stmt.scalar_one_or_none()
        return user