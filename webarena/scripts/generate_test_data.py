"""Replace the website placeholders with website domains from env_config
Generate the test data"""
import json
import os


"""Store the website URLs as follows"""
GITLAB = "http://localhost:8023/"
REDDIT = ""
SHOPPING = ""
SHOPPING_ADMIN = ""
WIKIPEDIA = ""
MAP = ""
HOMEPAGE = ""

"""Use these accounts for the evaluation purpose only as they are specifically created for the evaluation purpose"""
ACCOUNTS = {
    "reddit": {"username": "MarvelsGrantMan136", "password": "test1234"},
    "gitlab": {"username": "byteblaze", "password": "hello1234"},
    "shopping": {
        "username": "emma.lopez@gmail.com",
        "password": "Password.123",
    },
    "shopping_admin": {"username": "admin", "password": "admin1234"},
    "shopping_site_admin": {"username": "admin", "password": "admin1234"},
}

URL_MAPPINGS = {
    REDDIT: "http://reddit.com",
    SHOPPING: "http://onestopmarket.com",
    SHOPPING_ADMIN: "http://luma.com/admin",
    GITLAB: "http://gitlab.com",
    WIKIPEDIA: "http://wikipedia.org",
    MAP: "http://openstreetmap.org",
    HOMEPAGE: "http://homepage.com",
}


def main() -> None:
    """Paste the correct address to the test.raw.json and test.json files"""
    with open("./test.raw.json", "r") as f:
        raw = f.read()
    raw = raw.replace("__GITLAB__", GITLAB)
    raw = raw.replace("__REDDIT__", REDDIT)
    raw = raw.replace("__SHOPPING__", SHOPPING)
    raw = raw.replace("__SHOPPING_ADMIN__", SHOPPING_ADMIN)
    raw = raw.replace("__WIKIPEDIA__", WIKIPEDIA)
    raw = raw.replace("__MAP__", MAP)
    with open("./test.json", "w") as f:
        f.write(raw)
    # split to multiple files
    data = json.loads(raw)
    for idx, item in enumerate(data):
        """Using gitlab here will generate the test files that corresponding to gitlab only similarly using shopping_admin or shopping will generate respective test files"""
        if item['sites'] == ['gitlab']:
            """Paste the correct location of the config files folder where you will get all the test files for that particular site"""
            with open(f"./WebArena/webarena/config_files/{idx}.json", "w") as f:
                json.dump(item, f, indent=2)


if __name__ == "__main__":
    main()


"""Check the configs_files folder where you will get the test cases for the desired website"""