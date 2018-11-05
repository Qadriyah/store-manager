from api import connection


class Delete:
    def __init__(self):
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
