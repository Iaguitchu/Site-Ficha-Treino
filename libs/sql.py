from datetime import datetime
from decimal import Decimal
import json
import mysql.connector

mySQLConnection = None

def configMySql(prm):
    global mySQLConnection
    if isinstance(prm, str):
        MYSQL_CONNECTION = prm
    else:
        MYSQL_CONNECTION = prm.config["MYSQL_CONNECTION"]

    mySQLConnection = json.loads(MYSQL_CONNECTION)


def connect():
    global mySQLConnection
    return mysql.connector.connect(**mySQLConnection)

def sqlSelectDict(sql: str, args=()):
    cnx = connect()
    try:
        cursor = cnx.cursor()
        cursor.execute(sql, args)
        headers = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        data = []
        for row in rows:

            item = {}
            for col, name in enumerate(headers):
                valor = row[col]
                if isinstance(valor, Decimal):
                    item[name] = float(valor)
                elif isinstance(valor, datetime):
                    item[name] = valor.isoformat()
                else:
                    item[name] = valor

            data.append(item)
        cursor.close()
    finally:
        if cnx is not None:
            cnx.close()
    return data


def sqlExecute(sql: str, args=()):
    cnx = connect()
    try:
        cursor = cnx.cursor()
        cursor.execute(sql, args)
        count = cursor.rowcount
        newid = cursor.lastrowid
        cnx.commit()
    except Exception as ex:
        raise ex
    finally:
        if cnx is not None:
            cnx.close()
    return count, newid


def sqlSelect(sql: str, args=()):
    cnx = connect()
    try:
        cursor = cnx.cursor()
        cursor.execute(sql, args)
        result = cursor.fetchall()
        cursor.close()
    finally:
        if cnx is not None:
            cnx.close()

    return result

