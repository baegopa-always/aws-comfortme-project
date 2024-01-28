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


def  conductSqlQuery(sql, sqlData):
    print("--------------------------------")
    print("conductSqlQuery function init")
    conn=getMysqlConn()
    curs = conn.cursor()
    curs.execute(sql, sqlData) 
    conn.commit()
    print("conductSqlQuery function done")
    print("--------------------------------")


def lambda_handler(event, context):
    
    try:
        print("--------------------------------")
        print("deleteConsole lambda_handler function init")
        
        params=event['queryStringParameters']
        consoleBotId=params["consoleBotId"]
        
        sql = "DELETE FROM console WHERE consoleId=%s"
        conductSqlQuery(sql, consoleBotId)
        
        result={
            'statusCode':HTTPStatus.OK,
            'headers': {
            'Access-Control-Allow-Origin': '*',
            }
        }
        print("deleteConsole lambda_handler function done")
        print("--------------------------------")
        return result
    except Exception:
        logging.exception(Exception)