from fastapi import HTTPException


class RegistarationManager():
    def __init__(self):
        self.users_db = {}

    def create_user(self, login: str, password: str, dob: str, role: str):
        if login in self.users_db:
            raise HTTPException(status_code=400, detail="Пользователь с таким логином уже существует.")
        user = {"login": login, "password": password, "dob": dob, "role": role}
        self.users_db[login] = user
        
    def get_user(self, login: str):
        return self.users_db.get(login)
    