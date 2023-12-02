import psycopg2
import uuid

conn = psycopg2.connect(
    database="moscow",
    user="postgres",
    password="verySecret",
    host="localhost",
    port="5432"
)

def init_task_table():
    with conn.cursor() as cur:
        print('CREATE TABLE request_tasks')

        cur.execute(f"""
        CREATE TABLE request_tasks (
            id UUID NOT NULL PRIMARY KEY,
            latitude DOUBLE PRECISION NOT NULL,
            longitude DOUBLE PRECISION NOT NULL,
            filepath VARCHAR(255) NOT NULL
        );
        """)

def _insert_task(task):
    with conn.cursor() as cur:
        cur.execute(f"""
        INSERT INTO request_tasks (id, latitude, longitude, filepath)
        VALUES ('{task.id}', {task.latitude}, {task.longitude}, '{task.filepath}');
        """)

def create_task(latitude, longitude, filepath):
    id = str(uuid.uuid4())
    task = Task(id, latitude, longitude, filepath)

    _insert_task(task)

    return task

def task_by_id(id):
    with conn.cursor() as cur:
        cur.execute(f"""
        SELECT * FROM request_tasks WHERE id = '{id}';
        """)

        result = cur.fetchall()

        if len(result) > 0:
            return Task(result[0][0], result[0][1], result[0][2], result[0][3])
        else:
            return None

class Task:
    def __init__(self, id, latitude, longitude, filepath):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.filepath = filepath
