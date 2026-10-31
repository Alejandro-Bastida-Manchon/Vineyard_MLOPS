import hashlib
import io
from PIL import Image, UnidentifiedImageError

MIN_SIDE = 128
ALLOWED_FORMATS = {"JPEG", "PNG"}

def image_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def validate_image(data: bytes) -> tuple[bool, str]:
    """Devuelve (es_valida, motivo)."""
    try:
        Image.open(io.BytesIO(data)).verify()
        img = Image.open(io.BytesIO(data))  # verify() deja el objeto inservible
    except (UnidentifiedImageError, OSError, SyntaxError):
        return False, "corrupt"
    if img.format not in ALLOWED_FORMATS:
        return False, f"format_{img.format}"
    if min(img.size) < MIN_SIDE:
        return False, "too_small"
    return True, "ok"