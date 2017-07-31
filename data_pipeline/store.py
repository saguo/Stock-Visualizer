from __future__ import absolute_import

from cassandra.cluster import Cluster

KEYSPACE = 'stock'
TABLE = 'stock'

class DataStore(object):

    def __init__(self, contact_points):
        cassandra_cluster = Cluster(contact_points=contact_points)
        self.session = cassandra_cluster.connect()
        self.session.execute(
            """
            CREATE KEYSPACE IF NOT EXISTS %s
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '3'}
            AND durable_writes = 'true'
            """ % KEYSPACE)
        self.session.set_keyspace(KEYSPACE)
        self.session.execute(
            """
            CREATE TABLE IF NOT EXISTS %s (
                stock_symbol text,
                trade_time timestamp,
                trade_price float,
                PRIMARY KEY (stock_symbol,trade_time))
            """ % TABLE)

    def get(self, key):
        pass

    def put(self, symbol, tradetime, price):
        self.session.execute(
            """
            INSERT INTO %s (stock_symbol, trade_time, trade_price)
            VALUES ('%s', '%s', %f)
            """ % (TABLE, symbol, tradetime, price)
            
        )

    def shut_down(self):
        self.session.shutdown()