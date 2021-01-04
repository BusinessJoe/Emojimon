import pickle
import json
from emojimon import Emoji, move


def move_load(string: str):
    with open("move_data.json", "r") as f:
        data_dict = json.load(f)
    return data_dict[string]


def add_item():
    with open("CompleteMoveList.dat", "rb") as f:
        data_list = pickle.load(f)

    laser = move()
    laser.moveName = "Legendary Laser"
    laser.moveType = "Gamer"
    laser.movePower = 150
    laser.moveAccuracy = 0.98
    laser.moveEffect = "E5"
    laser.moveHitType = "Emotional"

    sword = move()
    sword.moveName = "Legendary Sword"
    sword.moveType = "Sheep"
    sword.movePower = 150
    sword.moveAccuracy = 0.98
    sword.moveEffect = "F5"
    sword.moveHitType = "Physical"

    data_list.append(laser)
    data_list.append(sword)

    with open("CompleteMoveList.dat", "wb") as f:
        pickle.dump(data_list, f)


def check_data():
    with open("CompleteEmojiDex.dat", "rb") as f:
        data_list = pickle.load(f)
    print(data_list[1412].name)


def pickle_2_json():
    with open("CompleteEmojiDex.dat", "rb") as f:
        data_dict = pickle.load(f)

    #with open("emoji_data.json", "w") as f:


if __name__ == '__main__':
    check_data()

