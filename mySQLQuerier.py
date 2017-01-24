import mysql.connector, json
from datetime import datetime

config = json.load(open("config.json"))
mysql_pw = config['mysql_pw']

connection = mysql.connector.connect(user='loganyg', password=mysql_pw, host='127.0.01', database='changeorg_data')
cursor = connection.cursor()

def insert(json_body, table, fields, field_keys=[]):
    command = ("INSERT INTO " + table + " "
               "(" + ','.join(fields) + ")"
               "VALUES (" + ','.join(['%s']*len(fields)) + ")"
        )
    if field_keys:
        data = tuple(map(lambda x: json_body[x], field_keys))
    else:
        data = tuple(map(lambda x: json_body[x], fields))
    cursor.execute(command, data)
    connection.commit()

def add_petition(json_body):
    add_petition = ("INSERT INTO petitions "
                    "(petition_id, url, title, goal, creator_name, creator_url, organization_name, organization_url, overview, created_at, category)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
    petition_data = (json_body['petition_id'], json_body['petition_url'], json_body['title'], json_body['goal'], json_body['creator_name'], json_body['creator_url'],
                     json_body['organization_name'], json_body['organization_url'], json_body['overview'], datetime.strptime(json_body['created_at'], "%Y-%m-%dT%H:%M:%SZ"),
                     json_body['category'])
    cursor.execute(add_petition, petition_data)
    connection.commit()

def add_user(json_body):
    add_user = ("INSERT INTO users "
                "(user_id, url, name, location)"
                "VALUES (%s, %s, %s, %s)"
        )
    user_data = (json_body['user_id'], json_body['user_url'], json_body['name'], json_body['location'])
    cursor.execute(add_user, user_data)
    connection.commit()

def add_target(json_body):
    columns = ['name', 'title', 'type', 'target_area']
    for col in columns:
       if col not in json_body.keys():
             json_body[col] = None
    add_target = ("INSERT INTO targets "
                  "(" + ",".join(columns) + ")"
                  "VALUES (%s, %s, %s, %s)"
        )
    target_data = tuple(map(lambda x: json_body[x], columns))
    cursor.execute(add_target, target_data)
    connection.commit()

def close():
    connection.close()
