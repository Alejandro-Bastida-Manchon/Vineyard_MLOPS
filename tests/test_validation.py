import io

from PIL import Image

from vineyard.validation import image_hash, validate_image


def make_image(size=(256, 256), fmt="JPEG") -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", size, "green").save(buf, format=fmt)
    return buf.getvalue()


def test_valid_jpeg_is_accepted():
    # Este test habría detectado el fallo de io.BytesIO sin (data)
    assert validate_image(make_image()) == (True, "ok")


def test_valid_png_is_accepted():
    assert validate_image(make_image(fmt="PNG")) == (True, "ok")


def test_too_small_is_rejected():
    assert validate_image(make_image((32, 32))) == (False, "too_small")


def test_garbage_bytes_are_corrupt():
    assert validate_image(b"no soy una imagen") == (False, "corrupt")


def test_unsupported_format_is_rejected():
    ok, reason = validate_image(make_image(fmt="BMP"))
    assert ok is False
    assert reason == "format_BMP"


def test_same_content_gives_same_hash():
    assert image_hash(make_image()) == image_hash(make_image())


def test_different_content_gives_different_hash():
    assert image_hash(make_image((256, 256))) != image_hash(make_image((300, 300)))