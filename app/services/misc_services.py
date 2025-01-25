import base64
def encode_img(data):
    try:
        with open(data, "rb") as image_file:
            profile_picture_encoded = base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Warning: Profile picture file {data} not found.")
    except Exception as e:
        print(f"Error processing profile picture: {e}")
    return profile_picture_encoded
