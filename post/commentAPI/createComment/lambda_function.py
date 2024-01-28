import json
import sys
import logging
import pymysql
from http import HTTPStatus
import requests

DB_HOST="db-team8-consolation.c8fut6pj2ay8.ap-northeast-2.rds.amazonaws.com"
DB_USER="root"
DB_PASSWORD="1tkddydwkdql"
DB_NAME="comfortmeDB"

def connectSQL():
    return pymysql.connect(
        host=DB_HOST, 
        user=DB_USER, 
        password=DB_PASSWORD, 
        db=DB_NAME)

def createCommentSQL(sql,sqlData):
    connection=connectSQL()
    connection.cursor().execute(sql,sqlData) 
    connection.commit()

def lambda_handler(event, context):
    try:
        data=json.loads(event['body'])
        
        contents=data['contents']
        consolePostId=data['consolePostId']
        email=data['email']
        anonymous=data['anonymous']
        print(f"contents : {contents}  consolePostId : {consolePostId}   email : {email}  anonymous : {anonymous}")
        
        sqlData={
            'contents':contents,
            'consolePostId':consolePostId,
            'email':email,
            'anonymous':anonymous
        }
        sql = "INSERT INTO Comment(contents,consolePostId,email,anonymous) VALUES(%(contents)s,%(consolePostId)s,%(email)s,%(anonymous)s)"
        createCommentSQL(sql,sqlData)
        
        result={
            'statusCode':HTTPStatus.OK,
            'headers': {
            'Access-Control-Allow-Origin': '*',
            },
        }
        return result
    except Exception:
        logging.exception(Exception)
