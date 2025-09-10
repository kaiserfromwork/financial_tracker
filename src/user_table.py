# TODO: REMOVE print() for Log
class UserTable:
    def __init__(self, db_file):
        self.db_file = db_file

    def add_user(self, name, email, password_hashed, salt, registration_date) -> None:
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

    # TODO: Change type annotation, check that user_info is a valid type and not empty
    def select_user(self, user_info: dict) -> list | None:
        if not user_info:
            return None

        db = self.db_file
        with db._connect() as conn:
            cur = conn.cursor()

            where_clause = " AND ".join(f"{col} = ?" for col in user_info.keys())
            values = list(user_info.values())

            cur.execute(
                f"SELECT user_id, user_name, user_email FROM user WHERE {where_clause}",
                values,
            )
            result = (
                cur.fetchall()
            )  # TODO: Change this to fetchone, change update_user afterwards

            return result if result else None

    def update_user(
        self,
        update_info: dict,
        user_info: dict,
    ) -> bool:  # TODO: CURRENTLY RETURN bool, might change it to the updated row.
        if not isinstance(update_info, dict):
            raise TypeError(
                f"update_info expected to be a dictionary, but got: {type(update_info).__name__}"
            )
        if not isinstance(user_info, dict):
            raise TypeError(
                f"user_info expected to be a dictionary, but got: {type(user_info).__name__}"
            )

        db = self.db_file
        with db._connect() as conn:
            cur = conn.cursor()

            if not user_info:
                print("User select information is missing!")
                return False
            else:
                result = self.select_user(user_info)
                if result:
                    user_id, _, _ = result[
                        0
                    ]  # TODO: CHANGE select query to fetchone, change this to result afterwards
                    print("User selected!")
                else:
                    user_id, _, _ = [None, None, None]
                    print("User not found!")

            if not update_info:
                print("User update infomation is missing!")
                return False
            else:
                set_clause = " , ".join(
                    f"{col} = '{value}'" for col, value in update_info.items()
                )

            if set_clause and user_id:
                cur.execute(
                    f"UPDATE user SET {set_clause} WHERE user_id = ?", (user_id,)
                )

            else:
                return False

            return True if cur.rowcount else False
