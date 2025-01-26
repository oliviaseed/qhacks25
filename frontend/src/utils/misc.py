from datetime import datetime
import base64
from flask import send_file
import io

def calculate_age(birthday):
    birth_date = datetime.strptime(birthday, "%Y-%m-%d")
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def encode_img(data):
    try:
        with open(data, "rb") as image_file:
            img = base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Warning: Picture file {data} not found.")
    except Exception as e:
        print(f"Error processing profile picture: {e}")
    return img

def decode_img(data):
    try:
        img = base64.b64decode(data)
    except Exception as e:
        print(f"Error decoding picture: {e}")
    return send_file(io.BytesIO(img), mimetype='image/jpeg')
