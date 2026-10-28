from flask import json


def load_sample(name):
    try:
        with open(f"cache/sample_{name}.json") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None