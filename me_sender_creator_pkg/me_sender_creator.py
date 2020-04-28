# Main program that create parameter of a new user

import json
from pathlib import Path

from . import me_components, me_sender_db


def me_sender_create(id_number, name):
    # Create and save a new user
    # Input: user ID, user name
    # Output: {"id":user ID, "name":user name, "icons":user's list of icons to memorize, "cell":cell user must look for}

    #Check configuration values
    config_file_path = Path.cwd().joinpath("me_sender_creator_pkg", "config_file")
    with open(config_file_path, "r") as config:
        config_info = json.load(config)
    collection_size = config_info["COLLECTION_SIZE"]
    num_icons_sender = config_info["NUM_ICONS_SENDER"]
    position_list_size = config_info["POSITION_LIST_SIZE"]

    # create user
    sender = me_sender_db.SenderDB(id_number, name)

    # create icons collection and assign random icons to user
    icons = me_components.Icons(collection_size)
    sender.icons = icons.random_choose(num_icons_sender)

    # create the position-list and choose random cell
    position_list = me_components.PositionList(position_list_size, num_icons_sender)
    sender.cell = position_list.random_cell()

    # save to user database
    sender.save_info()

    return {"id":sender.id, "name":sender.name, "icons":sender.icons, "cell":sender.cell}
