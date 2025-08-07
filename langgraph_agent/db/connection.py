import mysql.connector


def sync_query(query: str):
    mydb = mysql.connector.connect(host="localhost", user="root", password="", database="bc")
    cursor = mydb.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    mydb.close()
    return result
