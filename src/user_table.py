class UserTable:
    def __init__(self, db_file):
        self.db_file = db_file

    def add_user(self, name, email, password_hashed, salt, registration_date):
        db = self.db_file
        with db._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO user (user_name, user_email, password_hashed, salt, registration_date)
                VALUES (?, ?, ?, ?, ?)
                """,
                (name, email, password_hashed, salt, registration_date),
            )

    def delete_user(self, name, email) -> bool:
        db = self.db_file
        with db._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT user_id, user_name, user_email 
                FROM user
                WHERE user_name = ? AND user_email = ?
                """,
                (name, email),
            )
            result = cur.fetchall()
            if len(result) == 1:
                user_id = result[0][0]
                user_id = 1
                cur.execute(
                    """
                    DELETE 
                    FROM user
                    WHERE user_id = ?
                    """,
                    [user_id],
                )
                return True
            elif len(result) == 0:  # TODO: CHANGE THIS AFTER IMPLEMNT LOG MODULE
                print(f"No user found named {name} with {email}")
                return False
            else:
                print(f"Multiple users found named {name} with email({email}).")
                return False

    def select_user(self, user_info: dict) -> list | None:
        db = self.db_file
        with db._connect() as conn:
            cur = conn.cursor()

            where_clause = " AND ".join(f"{col} = ?" for col in user_info.keys())
            values = list(user_info.values())

            cur.execute(
                f"SELECT user_id, user_name, user_email FROM user WHERE {where_clause}",
                values,
            )
            result = cur.fetchall()

            return result if result else None
