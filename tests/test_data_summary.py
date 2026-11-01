from vineyard.data_summary import count_images


def test_count_images_counts_only_images_per_class(tmp_path):
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "1.jpg").write_bytes(b"x")
    (tmp_path / "a" / "notes.txt").write_text("x")
    (tmp_path / "b").mkdir()

    assert count_images(tmp_path) == {"a": 1, "b": 0}