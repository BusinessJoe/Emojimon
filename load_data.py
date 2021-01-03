import pickle
import json
from emojimon import Emoji


class move:
    moveName = ""
    moveType = ""
    movePower = 0
    moveAccuracy = 0
    moveEffect = ""
    moveHitType = ""


def move_load(string: str):
    with open("move_data.json", "r") as f:
        data_dict = json.load(f)
    return data_dict[string]


def pickle_2_json():
    with open("CompleteEmojiDex.dat", "rb") as f:
        data_dict = pickle.load(f)

    print(type(data_dict))
    print(data_dict[0].name)

if __name__ == "__main__":
    pickle_2_json()
