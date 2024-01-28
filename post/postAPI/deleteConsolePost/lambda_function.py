import logging
import pymysql
from http import HTTPStatus

DB_HOST="db-team8-consolation.c8fut6pj2ay8.ap-northeast-2.rds.amazonaws.com"
DB_USER="root"
DB_PASSWORD="1tkddydwkdql"
DB_NAME="helpmeDB"

def connectSQL():
    return pymysql.connect(
        host=DB_HOST, 
        user=DB_USER, 
        password=DB_PASSWORD, 
        db=DB_NAME)


def deletePostSQL(sql, sqlData):
    connection=connectSQL()
    connection.cursor().execute(sql,sqlData) 
    connection.commit()


def lambda_handler(event, context):
    try:
        params=event['queryStringParameters']
        consolePostId=params["consolePostId"]
        sqlData = {
            'consolePostId' : consolePostId
        }
        sql = "DELETE FROM console WHERE consoleId=%(consolePostId)s"
        deletePostSQL(sql, sqlData)
        
        result={'statusCode':HTTPStatus.OK,'headers': {
                'Access-Control-Allow-Origin': '*',
            }
        }
        return result
    except Exception:
        logging.exception(Exception)