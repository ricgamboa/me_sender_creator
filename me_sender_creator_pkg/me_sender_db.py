# Module to include the option to save users in database
# Only for testing purpose. The database include most secret information,
# this module mst be replaced with very secure connection and secure database

import sqlite3
import json
from pathlib import Path

from .me_components import Sender


class SenderDB(Sender):
    # Add method to save the sender information in the database
    def save_info(self):
        icons_json = json.dumps(self.icons)

        # Open database path
        config_file_path = Path.cwd().joinpath("me_sender_creator_pkg", "config_file")
        with open(config_file_path, "r") as config:
            config_info = json.load(config)
        database_path = Path(config_info["USER_DATABASE_PATH"])
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        # Verify tables exists or create
        cursor.executescript("CREATE TABLE IF NOT EXISTS user("
                                 "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,"
                                 "global_user_id INTEGER UNIQUE,"
                                 "user_name TEXT,"
                                 "user_icons TEXT,"
                                 "user_cell INTEGER);")
        # Save values to database
        cursor.execute("INSERT OR IGNORE INTO user (global_user_id,user_name,user_icons,user_cell) VALUES (?, ?, ?, ?)",
                       (self.id, self.name, icons_json, self.cell))

        connection.commit()
        cursor.close()

