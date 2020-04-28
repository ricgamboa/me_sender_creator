# This module should be replaced by a graphical interface

class UserDisplay:
    def __init__(self):
        self.language = "english"

    def positon_name(self, language):
        spanish_list = ["sala", "comedor", "cocina", "baño", "alcoba"]
        english_list = ["living room", "dinning room", "kitchen", "bathroom", "bedroom"]

        switcher = {
            "spanish":spanish_list,
            "english":english_list
        }
        return switcher.get(language,"invalid language")

    def show_icon_position(self, user_icons):
        print("----------------------------------------")
        print("Your icons are the following: ")
        print("----------------------------------------")
        print(user_icons)
        print("----------------------------------------")
        print("located at the following positions: ")
        print("----------------------------------------")
        for icon, pos in zip(user_icons, self.positon_name(self.language)):
            print("Icon: {0} is located at {1}".format(icon, pos))

    def show_cell(self, user_cell):
        print("----------------------------------------")
        print("Use the position in the cell {}".format(user_cell+1))
        print("----------------------------------------")
