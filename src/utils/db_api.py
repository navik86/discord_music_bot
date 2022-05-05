from psycopg2 import connect
from config.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


def connection_db():
    global connection
    try:
        connection = connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    except Exception as _ex:
        print("Error while working with PostgreSQL", _ex)
    else:
        print("Database is connected.")


def add_new_track(*args):

    track, creater = args

    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO track_counter (track_name, creater_name, counter) VALUES (%s, %s, %s)",\
                       (track, creater, 1))
        connection.commit()
        print("[INFO] Track was successfully inserted")


def check_track(track):

    with connection.cursor() as cursor:
        cursor.execute("SELECT track_name FROM track_counter WHERE track_name = %s",\
                       (track,))
        select_result = cursor.fetchone()

    if select_result:
        return True
    else:
        return False


def add_counter(track):

    with connection.cursor() as cursor:
        cursor.execute("UPDATE track_counter SET counter = counter + 1 WHERE track_name = %s", \
                       (track,))
        connection.commit()
        print("[INFO] Counter was succefully updated")


def add_track_or_counter_to_db(*args):
    track, creator = args
    if check_track(track):
        add_counter(track)
    else:
        add_new_track(track, creator)


def show_top_5():
    top_list = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT track_name, counter FROM track_counter ORDER BY counter DESC LIMIT 5;")
        for row in cursor:
            top_list.append(row)
    return top_list