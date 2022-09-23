import csv
from typing import Any
from collections.abc import Generator
from faker import Faker
from flask import Flask
from pathlib import Path
import requests

# json file url (it's outside the function for faster work)
request = requests.get("http://api.open-notify.org/astros.json")
# path to requirements file
requirements = Path(
    "/home/oleh/PycharmProjects/homework__medvedenko_oleh__main/requirements.txt"
)
# website's background
background = (
    "<style>body{background-image: "
    "url(https://preview.redd.it/w4xyk5k6xpt51.jpg?auto=webp&s=bc3d47295b9272b46deda85d53381ffb21c7b2db);"
    "background-attachment: fixed;background-size: auto 100%; background-repeat: no-repeat;"
    "background-position: 40% 50%;}</style>"
)

fake = Faker()
app = Flask(__name__)


# Main page with hyperlinks
@app.route("/")
def main_page() -> str:
    return (
        f"{background}"
        "<h3><li><a href='/requirements/'>requirements</a></li></h3>"
        "<h3><li><a href='/generate-users/'>generate-users</a></li></h3>"
        "<h3><li><a href='/space/'>space</a></li></h3>"
        "<h3><li><a href='/mean/'>mean</a></li></h3>"
    )


# Requirements reader
@app.route("/requirements/")
def requirements_text() -> str:
    return f"{background}" "".join(
        f"<p>{i}</p>" for i in requirements.read_text().splitlines()
    )


# fake names and emails for Users generator
def generate_info() -> str:
    name = fake.first_name()
    email = f"{name}@{fake.domain_name()}"
    return f"{name} | {email}"


# Users generator
@app.route("/generate-users/")
@app.route("/generate-users/<int:amount>")
def generate_users(amount: int = 100) -> Generator[str, Any, None]:
    for index in range(amount):
        yield f"<p>{index + 1}. {generate_info()}</p>" f"{background}"


# Json reader
@app.route("/space/")
def space() -> str:
    text = request.json()
    return f"<p>Number of astronauts: {text['number']}</p> {background}"


# Mean calculator
@app.route("/mean/")
def mean() -> str:
    total_height = 0
    total_weight = 0
    total_index = 0
    cvs_url = "https://drive.google.com/uc?export=download&id=1yM0a4CSf0iuAGOGEljdb7qcWyz82RBxl"
    with requests.Session() as s:
        download = s.get(cvs_url)
    decoded_content = download.content.decode("utf-8")
    reader = csv.DictReader(decoded_content.splitlines())
    for row in reader:
        total_height += float(list(row.values())[1]) * 2.54
        total_weight += float(list(row.values())[2]) * 0.45
        total_index += 1
    average_height = total_height / total_index
    average_weight = total_weight / total_index
    return (
        f"<p>Average height: {round(average_height, 2)} cm.</p>"
        f"<p>Average weigh: {round(average_weight, 2)} kg.</p>"
        f"<p>Number of participants: {total_index}."
        f"{background}"
    )


if __name__ == "__main__":
    app.run(debug=True)
