from utilities.models import BoardPost
import psycopg2
import time
import random


def getConnection():
    return psycopg2.connect(
            database="postgres",
            user="postgres",
            password="revature",
            host="database-project0.c3f2ribjt3t3.us-east-1.rds.amazonaws.com",
            port="5432"
    )


def checkToken(token):
    connection = getConnection()
    cursor = connection.cursor()
    flag = False

    qry = f"SELECT * FROM users WHERE authtoken='{token}';"

    try:
        cursor.execute(qry)

        if len(list(cursor.fetchall())) == 1:
            flag = True

    except psycopg2.DatabaseError:
        pass

    connection.close()
    return flag


def authenticate(username, password):
    connection = getConnection()
    cursor = connection.cursor()
    output = None

    qry = f"SELECT * FROM users WHERE username='{username}' AND password='{password}';"

    try:
        cursor.execute(qry)

        hashstring = str(hash(float(time.time())+random.random()))
        if len(list(cursor.fetchall())) == 1:
            output = hashstring
            qry2 = f"UPDATE users SET authtoken='{hashstring}' WHERE username='{username}';"
            cursor.execute(qry2)

    except psycopg2.DatabaseError:
        pass

    connection.close()
    return output


def register(username, password):
    connection = getConnection()
    cursor = connection.cursor()
    output = False

    qry = f"SELECT * FROM users WHERE username='{username}' AND password='{password}';"

    try:
        cursor.execute(qry)

        if len(list(cursor.fetchall())) == 0:
            qry2 = f"INSERT INTO users (username, password) VALUES ('{username}','{password}');"
            cursor.execute(qry2)
            output = True

    except psycopg2.DatabaseError:
        pass

    connection.close()
    return output


def getPosts():
    connection = getConnection()
    cursor = connection.cursor()
    output = []

    qry = f"SELECT * FROM boardposts;"

    try:
        cursor.execute(qry)

        results = list(cursor.fetchall())
        if len(results) > 0:
            for each in results:
                output.append(BoardPost(each[0], each[1]))

    except psycopg2.DatabaseError:
        pass

    connection.close()
    return output


def makePost(token, message):
    connection = getConnection()
    cursor = connection.cursor()
    flag = False

    qry = f"SELECT username FROM users WHERE authtoken='{token}';"

    try:
        cursor.execute(qry)

        result1 = cursor.fetchone()
        if result1 is not None:

            username = str(result1[0])

            posts = getPosts();
            if len(posts) == 0:
                id = str(0)
                qry2 = f"INSERT INTO boardposts (post_id,author,message) VALUES ('{id}','{username}','{message}');"
                cursor.execute(qry2)
            else:
                qry2 = f"SELECT MAX(post_id) FROM boardposts;"
                cursor.execute(qry2)

                nextid = str(int(cursor.fetchone()[0])+1)

                qry3 = f"INSERT INTO boardposts (post_id,author,message) VALUES ('{nextid}','{username}','{message}');"

                cursor.execute(qry3)

            flag = True

    except psycopg2.DatabaseError:
        pass

    connection.close()
    return flag
