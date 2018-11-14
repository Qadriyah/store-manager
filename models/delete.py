class Delete:
    def __init__(self, connection):
        self.cursor = connection.cursor

    def delete_record(self, table, record_id):
        """
        Deletes a record from the table
        """
        response = {}
        try:
            query = """
            UPDATE {} SET status = '{}' WHERE id = {}
            """.format(table, "Deleted", record_id)
            self.cursor.execute(query)
            response.update({"msg": "Success"})
        except Exception:
            response.update({"msg": "Failure"})

        return response

    def delete_from_table(self, table, record_id):
        response = {}
        try:
            query = """
            DELETE FROM {} WHERE id = {}
            """.format(table, record_id)
            self.cursor.execute(query)
            response.update({"msg": "Success"})
        except Exception:
            response.update({"msg": "Failure"})

        return response

    def delete_expired_tokens(self):
        """Deletes expired tokens from the databse"""
        response = {}
        try:
            query = """
            DELETE FROM blacklists WHERE expires < '{}'::TIMESTAMP
            """.format("NOW()")
            self.cursor.execute(query)
            response.update({"msg": "Success"})
        except Exception:
            response.update({"msg": "Failure"})

        return response
