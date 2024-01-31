import mysql.connector

def connect_to_database():
    """
    连接到 MySQL 数据库并返回一个连接对象。
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="qzt",
        port=3306
    )
    return connection

def close_connection(connection):
    """
    关闭 MySQL 数据库连接。
    """
    connection.close()
