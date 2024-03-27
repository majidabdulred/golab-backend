import base64
import io

from PIL import Image


def set_height_and_width(aspect_ratio):
    if aspect_ratio == "1:1":
        return 512, 512
    elif aspect_ratio == "4:3":
        return 512, 640
    elif aspect_ratio == "16:9":
        return 896, 512
    elif aspect_ratio == "2:3":
        return 512, 768
    elif aspect_ratio == "3:2":
        return 768, 512
    elif aspect_ratio == "9:16":
        return 512, 896
    else:
        return 512, 512


def base64_to_image(base64_string):
    return Image.open(io.BytesIO(base64.b64decode(base64_string.split(",", 1)[0])))


def image_to_base64(image):
    image_string = io.BytesIO()
    image.save(image_string, format="PNG")
    return base64.b64encode(image_string.getvalue()).decode("utf-8")
