import json

def get_color_list():
    with open("JSONS/colors.json", "r") as file:
        data = json.load(file)
        color_tuples = {key: tuple(value) for key, value in data["colors"].items()}
        return color_tuples