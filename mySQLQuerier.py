import mysql.connector, json
from datetime import datetime

config = json.load(open("config.json"))
mysql_pw = config['mysql_pw']

connection = mysql.connector.connect(user='loganyg', password=mysql_pw, host='127.0.01', database='changeorg_data')
cursor = connection.cursor()

def add_petition(p_json):
    add_petition = ("INSERT INTO petitions "
                    "(petition_id, url, title, goal, creator_name, creator_url, organization_name, organization_url, overview, created_at, category)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
    petition_data = (p_json['petition_id'], p_json['url'], p_json['title'], p_json['goal'], p_json['creator_name'], p_json['creator_url'],
                     p_json['organization_name'], p_json['organization_url'], p_json['overview'], datetime.strptime(p_json['created_at'], "%Y-%m-%dT%H:%M:%SZ"),
                     p_json['category'])
    cursor.execute(add_petition, petition_data)
    connection.commit()
def close():
    connection.close()