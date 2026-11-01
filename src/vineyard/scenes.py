"""Lectura de la verdad (ground truth) de las escenas Smart Spaces de NVIDIA."""
import json
import sys
from collections import Counter
from pathlib import Path

Frames = dict[int, list[dict]]


def load_ground_truth(path: str | Path) -> Frames:
    """Carga ground_truth.json y convierte las claves de fotograma a enteros."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return {int(frame): objects for frame, objects in raw.items()}


def object_types(gt: Frames) -> dict[int, str]:
    """Clase de cada objeto distinto (identificado por su id)."""
    return {o["object id"]: o["object type"] for objs in gt.values() for o in objs}


def appearances_by_class(gt: Frames) -> Counter:
    """Cuántas veces aparece cada clase, sumando todos los fotogramas."""
    return Counter(o["object type"] for objs in gt.values() for o in objs)


def cameras(gt: Frames) -> set[str]:
    """Cámaras en las que se ve algún objeto."""
    return {cam for objs in gt.values() for o in objs for cam in o["2d bounding box visible"]}


def main(path: str) -> None:
    gt = load_ground_truth(path)
    unique = Counter(object_types(gt).values())
    empty = sum(1 for objs in gt.values() if not objs)
    print(f"fotogramas: {len(gt)} (vacíos: {empty})")
    print(f"cámaras con objetos: {len(cameras(gt))}")
    print("objetos distintos por clase:", dict(unique))
    print("apariciones por clase:", dict(appearances_by_class(gt)))


if __name__ == "__main__":
    main(*sys.argv[1:])