from typing import Optional
from uuid import UUID
from infra.hash import hash_password, verify_password
from core.models.user_model import User
from core.schemas.user_schema import UserRegister


class UserService:
    @staticmethod
    async def create(data: UserRegister):
        user = User(
            username=data.username,
            email=data.email,
            password=hash_password(data.password),
        )

        return await User.insert(user)

    @staticmethod
    async def get_by_email(email: str) -> Optional[User]:
        return await User.by_email(email)

    @staticmethod
    async def get_by_id(id: UUID) -> Optional[User]:
      return await User.find_one(User.id == id)

    @staticmethod
    async def authenticate(email: str, password: str) -> Optional[User]:
        user = await UserService.get_by_email(email)

        print(user, email)
        if user is None:
            return None


        if not verify_password(hashed_password=user.password, password=password):
            return None

        return user
