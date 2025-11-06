from pathlib import Path

CACHE_FOLDER = Path(__file__).parent.parent / "cache"
OUT_FOLDER = Path(__file__).parent / "output"


all_listings = {}


def main():
    OUT_FOLDER.mkdir(parents=True, exist_ok=True)
    i = 0
    total = 0
    for file in OUT_FOLDER.glob("*.html"):
        with file.open("r", encoding="utf-8") as f:
            data = f.read()
        total += 1
        if 'title="Amazon Music"' in data:
            i += 1
    print(f"{i} / {total}")


if __name__ == "__main__":
    main()
