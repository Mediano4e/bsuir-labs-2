from abc import ABC, abstractmethod
from ..toolbox import get_logger, get_psycopg_conn


logger = get_logger()


class User(ABC):
    def __init__(self, username: str, password: str, dob: str | None = None):
        self._id: int | None = None
        self._username: str = username
        self._password: str = password
        self._dob: str = dob
    
    @abstractmethod
    def create_account(self) -> bool:
        pass
    
    def login(self) -> bool:
        conn = get_psycopg_conn()
        if not conn:
            return False

        cursor = conn.cursor()
        query = """
            SELECT id, birth_date 
            FROM users
            WHERE username = %s AND password_hash = %s
        """
        cursor.execute(query, (self._username, self._password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            user_id, birth_date = user
            self._id = user_id
            self._dob = birth_date
            return True
        else:
            logger.warning("Неверный логин или пароль")
            return False
    
    def _username_check(self) -> bool:
        conn = get_psycopg_conn()
        if not conn:
            return None

        cursor = conn.cursor()
        query = "SELECT id, birth_date FROM users WHERE username = %s;"
        cursor.execute(query, (self._username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return False if result else True
    
    @property
    def user_id(self) -> int | None:
        return self._id
    
    @property
    def username(self) -> str:
        return self._username
    
    @property
    def password(self) -> str:
        return self._password
    
    @property
    def dob(self) -> str | None:
        return self._dob
    