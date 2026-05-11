import json

from reader import ApiReader
from strategies import create_strategy


def load_config(path="config.json"):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def prompt_output_type(default_type):
    options = {
        "1": "console",
        "2": "kafka",
        "3": "redis",
        "4": "file",
    }

    print("Choose output destination:")
    print("1) Console")
    print("2) Kafka")
    print("3) Redis")
    print("4) File")

    prompt = "Enter 1-4"
    if default_type:
        prompt += f" (default: {default_type})"
    prompt += ": "

    while True:
        choice = input(prompt).strip()
        if not choice and default_type:
            return default_type
        if choice in options:
            return options[choice]
        print("Invalid choice. Please enter a number from 1 to 4.")


def main():
    config = load_config()
    api_config = config.get("api") or {}
    output_config = config.get("output") or {}

    url = api_config.get("url")
    if not url:
        raise ValueError("Config field 'api.url' is required.")

    reader = ApiReader(url, api_config.get("timeout_seconds", 20))
    items = reader.read()

    output_type = prompt_output_type(output_config.get("type"))
    output_config["type"] = output_type
    strategy = create_strategy(output_config)
    strategy.write(items)


if __name__ == "__main__":
    main()
