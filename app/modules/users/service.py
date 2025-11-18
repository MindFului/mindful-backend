# app/modules/users/service.py

from app.modules.auth.service import users_db

class UsersService:

    def find_by_id(self, user_id: str):
        return next((u for u in users_db if u["id"] == user_id), None)

    def find_all(self):
        return users_db

    def update(self, user_id: str, data: dict):
        user = self.find_by_id(user_id)
        if user:
            user.update(data)
            return user
        return None


users_service = UsersService()
