from PIL import Image, ImageEnhance
from io import BytesIO
import requests


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
    guess_poke(
        'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/microsoft/209/reversed-hand-with-middle-finger-extended_1f595.png')
