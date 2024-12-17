from user import User
from ..toolbox import get_logger, get_psycopg_conn


logger = get_logger()


class Analyst(User):
    def __init__(self, username, password, dob = None):
        super().__init__(username, password, dob)
    
    def create_account(self) -> bool:
        conn = get_psycopg_conn()
        if not conn:
            logger.warning("Не удалоось установить сединение с базой данных")
            return False
        if not self._username_check():
            logger.warning("Аналитик с таким именем уже существует")
            return False

        cursor = conn.cursor()

        query = """
            INSERT INTO users (username, password_hash, user_class, birth_date)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """

        cursor.execute(query, (self._username, self._password, "Аналитик", self._dob))
        result = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        if result:
            user_id = result
            self._id = user_id
            logger.info("Новый пользователь успешно создан")
            return True
        return False
    
    def create_review(self, title: str, content: str):
        if not self._id:
            raise Exception("Невозможно добавить отчёт для неавторизованного аналитика")
        
        conn = get_psycopg_conn()
        if not conn:
            logger.warning("Не удалоось установить сединение с базой данных")
            return False

        cursor = conn.cursor()
        query = """
            INSERT INTO analyst_reports (title, content, user_id)
            VALUES (%s, %s, %s)
            RETURNING id;
        """
        cursor.execute(query, (title, content, self._id))
        conn.commit()
        logger.info("Новый отзыв добавлен")

    def get_all_reviews(self) -> list[dict]:
        if not self._id:
            raise Exception("Невозможно получить отчёты для неавторизованного аналитика")
        
        conn = get_psycopg_conn()
        if not conn:
            logger.warning("Не удалоось установить сединение с базой данных")
            return False

        cursor = conn.cursor()
        query = """
            SELECT title, content
            FROM analyst_reports
            WHERE user_id = %s;
        """
        cursor.execute(query, (self._id,))
        reviews = cursor.fetchall()
        reviews_list = [
            {"title": review[0], "content": review[1]}
            for review in reviews
        ]
        cursor.close()
        conn.close()

        return reviews_list