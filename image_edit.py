from PIL import Image, ImageEnhance
from io import BytesIO
import requests


def battle_screen(index1, index2=None, effect=None):
    b = BytesIO()
    path1 = f'C:\\Users\\ADMIN\\PycharmProjects\\Emojimon\\Emojis\\Emoji{index1}.png'
    stadium = Image.open('poke_stadium.jpg')
    img1 = Image.open(path1)
    img1 = img1.resize((400, 400))
    background = stadium.copy()
    background.paste(img1, (300, 300), img1)

    try:
        path2 = f'C:\\Users\\ADMIN\\PycharmProjects\\Emojimon\\Emojis\\Emoji{index2}.png'
        img2 = Image.open(path2)
        img2 = img2.resize((400, 400))
        background.paste(img2, (1250, 300), img2)
    except FileNotFoundError:
        pass

    background.save(b, format='jpeg')
    b.seek(0)
    return b


def guess_poke(url: str):
    b = BytesIO()
    response = requests.get(url)

    img = Image.open(BytesIO(response.content))
    img = img.resize((500, 500))

    img_guess = Image.open('guess the pokemon.png')
    img_backup = img_guess.copy()

    enhancer = ImageEnhance.Brightness(img)
    img_dark = enhancer.enhance(0)
    layer = img_dark
    img_backup.paste(layer, (350, 300), mask=layer)
    img_backup.save(b, format='jpeg')
    b.seek(0)
    return b


if __name__ == "__main__":
    battle_screen(0, 0)