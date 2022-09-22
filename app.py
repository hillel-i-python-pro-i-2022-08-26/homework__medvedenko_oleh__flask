import csv
from typing import Any
from collections.abc import Generator
from faker import Faker
from flask import Flask
from pathlib import Path
import requests

fake = Faker()
app = Flask(__name__)


@app.route("/")
def main_page() -> str:
    return "<h1>Hello! You are on a main page!</h1>"


@app.route("/requirements/")
def requirements_text() -> str:
    requirements = Path(
        "/home/oleh/PycharmProjects/homework__medvedenko_oleh__main/requirements.txt"
    ).read_text()
    return f"<p>{requirements}</p>"


@app.route("/generate-users/")
def generate_users() -> Generator[str, Any, None]:
    names = [fake.first_name() for _ in range(100)]
    return (
        f"<p>First name: {name} | Email: {name}@{fake.domain_name()}</p>"
        for name in names
    )


@app.route("/space/")
def space() -> str:
    request = requests.get("http://api.open-notify.org/astros.json")
    text = request.json()
    return f"<p>Number of astronauts: {text['number']}</p>"


@app.route("/mean/")
def mean() -> str:
    sum_of_height = 0
    sum_of_weight = 0
    index = 0
    cvs_url = "https://drive.google.com/uc?export=download&id=1yM0a4CSf0iuAGOGEljdb7qcWyz82RBxl"
    with requests.Session() as s:
        download = s.get(cvs_url)
    decoded_content = download.content.decode("utf-8")
    reader = csv.DictReader(decoded_content.splitlines())
    for row in reader:
        sum_of_height += float(list(row.values())[1]) * 2.54
        sum_of_weight += float(list(row.values())[2]) * 0.45
        index += 1
    average_height = sum_of_height / index
    average_weight = sum_of_weight / index
    return (
        f"<p>Average height: {round(average_height, 2)} cm.</p>"
        f"<p>Average weigh: {round(average_weight, 2)} kg.</p>"
        f"<p>Number of participants: {index}."
    )


if __name__ == "__main__":
    app.run(debug=True)
