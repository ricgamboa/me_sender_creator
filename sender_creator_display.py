# This module should be replaced by a graphical interface

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json


class UserDisplay:
    def __init__(self):
        self.language = "english"
        self.icons_images = []

    def positon_name(self, language):
        spanish_list = ["sala", "comedor", "cocina", "baño", "alcoba"]
        english_list = ["living room", "dinning room", "kitchen", "bathroom", "bedroom"]

        switcher = {
            "spanish": spanish_list,
            "english": english_list
        }
        return switcher.get(language, "invalid language")

    def find_icons(self, icon_index):
        # Return a list with the images from the images/icons folder according to the icon_index set
        names_path = Path.cwd().joinpath("images", "icons", "icons_names")
        name_list = ["n"]*len(icon_index)
        with open(names_path) as names:
            line = 0
            for name in names:
                if line in icon_index:
                    name_list[icon_index.index(line)] = name.strip()
                line += 1
        icons_images = []
        for name in name_list:
            image_path = Path.cwd().joinpath("images", "icons", name)
            icons_images.append(Image.open(image_path))
        return icons_images

    def draw_table(self, corner, backgrnd_img, box_dimension, rows, columns, box_color=(255, 255, 255), line_color=(0, 0, 0)):
        # Draw table and return X positions and Y positions of the cell's centers
        box_corners = (corner[0], corner[1], corner[0]+box_dimension[0], corner[1]+box_dimension[1])
        h_lines_start_points = []
        h_lines_stop_points = []
        v_lines_start_points = []
        v_lines_stop_points = []
        y_point = box_corners[1]
        y_center_cell = [y_point + box_dimension[1]//(2*rows)]
        for h_point in range(rows - 1):
            y_point = y_point + box_dimension[1]//rows
            h_lines_start_points.append((box_corners[0], y_point))
            h_lines_stop_points.append((box_corners[2], y_point))
            y_center_cell.append(y_point + box_dimension[1]//(2 * rows))
        x_point = box_corners[0]
        x_center_cell = [x_point + box_dimension[0]//(2*columns)]
        for v_point in range(columns - 1):
            x_point = x_point + box_dimension[0]//columns
            v_lines_start_points.append((x_point, box_corners[1]))
            v_lines_stop_points.append((x_point, box_corners[3]))
            x_center_cell.append(x_point + box_dimension[0]//(2*columns))
        brush = ImageDraw.Draw(backgrnd_img)
        brush.rectangle(box_corners, fill=box_color, outline=line_color)
        for h_line in range(rows - 1):
            brush.line((h_lines_start_points[h_line], h_lines_stop_points[h_line]), fill=line_color)
        for v_line in range(columns - 1):
            brush.line((v_lines_start_points[v_line], v_lines_stop_points[v_line]), fill=line_color)
        return x_center_cell, y_center_cell

    def show_cell_icon_position(self, user_icons, user_cell):
        # Show icons list
        img_width = 800    # Background of the icon list
        img_height = 400   # Background of the icon list
        max_icon_area_width = 800   # Area to draw icons
        max_icon_area_height = 200  # Area to draw icons
        max_icon_width = (max_icon_area_width-5*len(user_icons))//len(user_icons)
        max_icon_height = max_icon_area_height-5

        self.icons_images = self.find_icons(user_icons)

        # Resize if required
        my_icons_list = []
        for icon_img in self.icons_images:
            org_width = icon_img.size[0]
            org_height = icon_img.size[1]
            icon_add = icon_img
            if org_width > max_icon_width:
                new_width = max_icon_width
                new_height = (max_icon_width*org_height)//org_width
                icon_add = icon_img.resize((new_width, new_height))
            if org_height > max_icon_height:
                new_height = max_icon_height
                new_width = (max_icon_height*org_width)//org_height
                icon_add = icon_img.resize((new_width, new_height))
            my_icons_list.append(icon_add)

        # Show icons in the position
        my_icons_image = Image.new(mode="RGBA", size=(img_width, img_height), color=(255, 255, 255))
        x_position = 5
        y_position = 5
        for image in my_icons_list:
            my_icons_image.paste(image, (x_position, y_position))
            x_position += image.size[0] + 5

        print("----------------------------------------")
        print("Your icons are the following: ")
        print("----------------------------------------")
        print(user_icons)
        print("----------------------------------------")

        #Show icons in the position
        background_path = Path.cwd().joinpath("images", "background.png")
        backgound_info_path = Path.cwd().joinpath("images", "background_info")
        bakcground_image = Image.open(background_path)
        with open(backgound_info_path) as background_info_json:
            background_info = json.load(background_info_json)

        mask = Image.new("L", tuple(background_info["icon_size"]), 0)
        brush1 = ImageDraw.Draw(mask)
        brush1.ellipse((0, 0, background_info["icon_size"][0], background_info["icon_size"][1]), fill=255)

        for icon_img, center_pos in zip(self.icons_images, background_info["positions"]):
            bakcground_image.paste(icon_img.resize(tuple(background_info["icon_size"])),
                                   (center_pos[0]-background_info["icon_size"][0],
                                    center_pos[1]-background_info["icon_size"][1]), mask)
        bakcground_image.show()

        print("located at the following positions: ")
        print("----------------------------------------")
        for icon, pos in zip(user_icons, self.positon_name(self.language)):
            print("Icon: {0} is located at {1}".format(icon, pos))

        # Draw table and the cell of the user
        table_dimension = (200, img_height-max_icon_area_height-50)
        (xcenter, ycenter) = self.draw_table((img_width//2-table_dimension[1], max_icon_area_height+25), my_icons_image,
                                             table_dimension, 2, 1)
        font = ImageFont.truetype("arial.ttf", size=30)
        brush2 = ImageDraw.Draw(my_icons_image)
        brush2.text((xcenter[0]-50, ycenter[0]-15), "location", font=font, fill=(255, 0, 255), align="right")
        brush2.text((xcenter[0]-15, ycenter[1]-15), str(user_cell+1), font=font, fill=(255, 0, 255), align="right")
        my_icons_image.show()

        print("----------------------------------------")
        print("Use the position in the cell {}".format(user_cell+1))
        print("----------------------------------------")
