import json

from vineyard.scenes import (
    appearances_by_class,
    cameras,
    load_ground_truth,
    object_types,
)


def obj(oid, kind, **boxes):
    return {"object type": kind, "object id": oid, "2d bounding box visible": boxes}


def write(tmp_path, data):
    path = tmp_path / "ground_truth.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_keys_become_integers(tmp_path):
    gt = load_ground_truth(write(tmp_path, {"0": [], "1": []}))
    assert list(gt) == [0, 1]


def test_object_types_are_unique_per_id(tmp_path):
    data = {
        "0": [obj(1, "Person", Camera_0001=[0, 0, 5, 5])],
        "1": [obj(1, "Person", Camera_0001=[1, 0, 6, 5]), obj(2, "Forklift")],
    }
    assert object_types(load_ground_truth(write(tmp_path, data))) == {1: "Person", 2: "Forklift"}


def test_appearances_count_every_frame(tmp_path):
    data = {"0": [obj(1, "Person")], "1": [obj(1, "Person"), obj(2, "Forklift")]}
    counts = appearances_by_class(load_ground_truth(write(tmp_path, data)))
    assert counts == {"Person": 2, "Forklift": 1}


def test_cameras_are_collected(tmp_path):
    data = {"0": [obj(1, "Person", Camera_0003=[0, 0, 1, 1], Camera_0015=[0, 0, 1, 1])]}
    assert cameras(load_ground_truth(write(tmp_path, data))) == {"Camera_0003", "Camera_0015"}