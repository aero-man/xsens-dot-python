'''
Handle database interactions.

Read and write discovered Xsens DOTs.
'''

import sqlite3
from app_logger import Logger


logger = Logger(__name__)


class XsensDOTDatabase:
    def __init__(self, name="database.sqlite"):
        logger.logger.info("Connecting to database: {}...".format(name))
        
        self.conn = sqlite3.connect(name)
        self.cursor = self.conn.cursor()
        
        self._create_tables()
        

    def add_device(self, ble_address, local_name, status, signal_strength):
        # Add an Xsens DOT device to the database
        status = "Disconnected"
        self.cursor.execute("INSERT INTO devices VALUES (?,?,?,?,?)",
                            ([None, ble_address, local_name, status, signal_strength]))
        self.conn.commit()
        
    def _create_tables(self):
        if not self._table_exists("devices"):
            logger.logger.debug("`devices` table does not exist. Creating...")
            self._create_device_table()

    def _table_exists(self, name):
        # Check if a table of `name` exists. If SELECT fails, it does not.
        try:
            self.cursor.execute("SELECT * FROM {}".format(name))
        except sqlite3.OperationalError as e:
            logger.logger.error(e)
            return False
        except Error as e:
            logger.logger.error(e)
            return False
        return True
    
    def _create_device_table(self):
        # Create a table to store scanned Bluetooth devices in
        try:
            self.cursor.execute('''CREATE TABLE devices
                                   (device_id INTEGER PRIMARY KEY,
                                   ble_address varchar(17) NOT NULL ,
                                   local_name varchar(20),
                                   status varchar(20),
                                   signal_strength_dbm INTEGER)''')
        except sqlite3.OperationalError as e:
            logger.logger.error(e)

