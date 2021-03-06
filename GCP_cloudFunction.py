import base64
import sqlalchemy
from sqlalchemy import update


def hello_pubsub(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    
    db_user = 'root' #  os.environ.get("DB_USER")
    db_pass = 'root' #  os.environ.get("DB_PASS")
    db_name = 'hack' #  os.environ.get("DB_NAME")
    cloud_sql_connection_name = 'hack-iot-264109:asia-southeast1:hack-iot' #  os.environ.get("CLOUD_SQL_CONNECTION_NAME")
    
    db = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername='mysql+pymysql',
            username=db_user,
            password=db_pass,
            database=db_name,
            query={
                'unix_socket': '/cloudsql/{}'.format(cloud_sql_connection_name)
            },
        ),
    )
    
    stmt = sqlalchemy.text('INSERT INTO log(meter_reding) VALUES (:data)')
    try:
        with db.connect() as conn:
            conn.execute(stmt, data=pubsub_message)
        message.ack()
    except Exception as e:
        print(e)
