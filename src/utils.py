from hashlib import sha256

from PIL import Image


def get_hash_from_image(content: Image) -> str:
    return sha256(content.tobytes()).hexdigest()