import pandas as pd
import pymysql
import logging
import sshtunnel
from sshtunnel import SSHTunnelForwarder


ssh_host = 'ssh_host'
ssh_username = 'ssh_username'
ssh_password = 'ssh_password'
database_username = 'database_username'
database_password = 'database_password'
database_name = 'database_name'
localhost = 'localhost'


def open_ssh_tunnel(verbose=True):
    """Open an SSH tunnel and connect using a username and password.

    :param verbose: Set to True to show logging
    :return tunnel: Global SSH tunnel connection
    """

    if verbose:
        sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG

    global tunnel
    tunnel = SSHTunnelForwarder(
        (ssh_host, 22),
        ssh_username = ssh_username,
        ssh_password = ssh_password,
        remote_bind_address = ('127.0.0.1', 3306)
    )

    tunnel.start()


def mysql_connect():
    """Connect to a MySQL server using the SSH tunnel connection

    :return connection: Global MySQL database connection
    """

    global connection

    connection = pymysql.connect(
        host=localhost,
        user=database_username,
        passwd=database_password,
        db=database_name,
        port=tunnel.local_bind_port
    )


def run_query(sql):
    """Runs a given SQL query via the global database connection.

    :param sql: MySQL query
    :return: Pandas dataframe containing results
    """

    return pd.read_sql_query(sql, connection)


open_ssh_tunnel()
mysql_connect()
df = run_query('SELECT * FROM deals LIMIT 100')
df.head()