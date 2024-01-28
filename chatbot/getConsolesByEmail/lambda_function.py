import json
import sys
import logging
import pymysql
import datetime
from http import HTTPStatus

def getMysqlConn():
    return pymysql.connect(
            host=DB_HOST, 
            user=DB_USER, 
            password=DB_PASSWORD, 
            db=DB_NAME)

def  conductSqlQuery(sql,sqlData):
    print("--------------------------------")
    print("conductSqlQuery function init")
    conn=getMysqlConn()
    curs = conn.cursor()
    with conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
                cur.execute(sql,sqlData)
                result = json.dumps(cur.fetchall(),default=json_default,ensure_ascii = False)
    print("conductSqlQuery function done")
    print("--------------------------------")
    return result

def json_default(value): 
    if isinstance(value, datetime.date): 
        return value.strftime('%Y-%m-%d %H:%M:%S') 
    raise TypeError('not JSON serializable')

def lambda_handler(event, context):
    try:
        print("--------------------------------")
        print("getConsolesByEmail lambda_handler function init")
        print("event : ",event)
        params=event['queryStringParameters']
        email=params['email']
        print("email : ",email)
        
        sql = "SELECT * FROM ConsoleBot WHERE email= %s ORDER BY createdAt ASC"
        retValue=conductSqlQuery(sql,email)
        
        result={
            'statusCode':HTTPStatus.OK,
            'headers': {
            'Access-Control-Allow-Origin': '*',
            },
            'body':retValue
        }
        print("getConsolesByEmail lambda_handler function done")
        print("--------------------------------")
        return result
    except Exception:
        logging.exception(Exception)