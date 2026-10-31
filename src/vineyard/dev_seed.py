"""Sube imágenes de prueba a raw/. Solo para desarrollo."""
import io

from PIL import Image

from vineyard.storage import BUCKET, get_s3


def make_image(size, fmt="JPEG"):
    buf = io.BytesIO()
    Image.new("RGB", size, "green").save(buf, format=fmt)
    return buf.getvalue()


def main():
    good = make_image((256, 256))
    files = {
        "raw/hoja_1_ok.jpg": good,
        "raw/hoja_2_duplicada.jpg": good,
        "raw/hoja_3_pequena.jpg": make_image((32, 32)),
        "raw/hoja_4_rota.jpg": b"no soy una imagen",
        "raw/hoja_5_bmp.jpg": make_image((256, 256), fmt="BMP"),
    }
    s3 = get_s3()
    for key, data in files.items():
        s3.put_object(Bucket=BUCKET, Key=key, Body=data)
        print("subida:", key)


if __name__ == "__main__":
    main()