"""Cuenta imágenes por clase. Sirve para revisar los datasets antes de entrenar."""
import sys
from pathlib import Path

EXTS = {".jpg", ".jpeg", ".png"}


def count_images(root: Path) -> dict[str, int]:
    """Cuenta las imágenes de cada subcarpeta (una subcarpeta = una clase)."""
    return {
        d.name: sum(1 for f in d.rglob("*") if f.suffix.lower() in EXTS)
        for d in sorted(root.iterdir())
        if d.is_dir()
    }


def main(base: str = "data") -> None:
    for dataset in sorted(Path(base).iterdir()):
        if not dataset.is_dir():
            continue
        counts = count_images(dataset)
        print(f"\n{dataset.name}  (total: {sum(counts.values())})")
        for cls, n in counts.items():
            print(f"  {cls:<15} {n}")


if __name__ == "__main__":
    main(*sys.argv[1:])