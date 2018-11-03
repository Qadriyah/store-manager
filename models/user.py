"""
User data access layer
"""

from models.connection import Connection


class UserModels:
    def __init__(self):
        __conn = Connection()
        self.cursor = __conn.connect()

    def add_user(self, user):
        """Inserts a user to the database"""
        result = {}
        try:
            query = """
            INSERT INTO users(fullname, username, password, roles) \
            VALUES('{}', '{}', '{}', '{}') 
            RETURNING *
            """.format(
                user.fullname,
                user.username,
                user.password,
                user.roles
            )
            self.cursor.execute(query)
            result.update({"user": self.cursor.fetchone()})
            result.update({"msg": "Success"})
        except Exception:
            result.update({"msg": "Some fields were missing"})

        return result

    def get_user(self, column, value):
        """
        Checks if user already exists

        Args:
            column(str): table column to be checked
            value(str, int): the value to be checked

        Returns:
            user(User): User if found, None otherwise
        """
        result = {}
        try:
            query = """
            SELECT id, fullname, username, password, roles, created_at \
            FROM users WHERE {} = '{}'
            """.format(column, value)
            self.cursor.execute(query)
            res = self.cursor.fetchone()
            result.update({"user": res})
            if not res:
                result.update({"msg": "User not found"})
            else:
                result.update({"msg": "Found"})
        except Exception:
            result.update({"msg": "Unknown column {}".format(column)})

        return result

    def get_all_users(self):
        """Retrieves all users from the database"""
        result = {}
        try:
            query = """
            SELECT id, fullname, username, password, roles, created_at \
            FROM users 
            """
            self.cursor.execute(query)
            res = self.cursor.fetchone()
            result.update({"users": res})
            if not res:
                result.update({"msg": "Users not found"})
            else:
                result.update({"msg": "Found"})
        except Exception:
            result.update({"msg": "Database error"})

        return result

    def edit_user(self):
        """
        Modifies user details
        """
        pass

    def delete_user(self):
        """
        Deletes a user from the database
        """
        pass
