from pathlib import Path

# FIXME: Implement merge for pyproject.toml?


def delete_myself():
    Path(__file__).unlink()


if __name__ == "__main__":
    delete_myself()

    print("Project successfully generated!")
    print("Run `poetry run doit list` to show the available actions.")
