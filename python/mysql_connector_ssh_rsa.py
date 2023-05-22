import pymysql
import paramiko
import pandas as pd
import config
from sshtunnel import SSHTunnelForwarder
from os.path import expanduser

C = config.Cred

sql_hostname = C.sql_hostname
sql_username = C.sql_username
sql_password = C.sql_password
sql_main_database = C.sql_main_database
sql_port = C.sql_port
ssh_host = C.ssh_host
ssh_user = C.ssh_user
ssh_port = C.ssh_port
sql_ip = C.sql_ip
rsa_password = C.rsa_password

home = expanduser('~')
pkeyfilepath = '/id_rsa'
mypkey = paramiko.RSAKey.from_private_key_file(home + pkeyfilepath, password=rsa_password)


class Connector:
    def mysql_connect(query):
        with SSHTunnelForwarder(
                (ssh_host, ssh_port),
                ssh_username=ssh_user,
                ssh_pkey=mypkey,
                ssh_password='ssh_password',
                remote_bind_address=(sql_hostname, sql_port)) as tunnel:
            conn = pymysql.connect(host='127.0.0.1', user=sql_username,
                    passwd=sql_password, db=sql_main_database,
                    port=tunnel.local_bind_port)
            data = pd.read_sql_query(query, conn)
            conn.close()
            return data

