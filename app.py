import csv
from typing import Any
from collections.abc import Generator
from faker import Faker
from flask import Flask, Response
from pathlib import Path
import requests
from webargs import fields
from webargs.flaskparser import use_args

from application.services.create_table import create_table
from application.services.db_connection import DBConnection


# json file url (it's outside the function for faster work)
request = requests.get("http://api.open-notify.org/astros.json")
# path to requirements file
requirements = Path("./requirements.txt/")
# website's background
background = (
    "<head><meta charset='UTF-8'><title>FlaskTasks</title></head>"
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
        # "<style>h1 {color: RebeccaPurple;text-shadow: 2px 2px 2px Plum;}</style>"
        "<body><h1>Hello, you are on a main page!</h1>"
        "<ul><h3><li><a href='/requirements/'>requirements</a></li></h3>"
        "<h3><li><a href='/generate-users/'>generate-users</a></li></h3>"
        "<h3><li><a href='/space/'>space</a></li></h3>"
        "<h3><li><a href='/mean/'>mean</a></li></h3>"
        "<h3><li><a href='/phones/read-all'>show the base</a></li></h3></ul></body>"
    )


# Requirements reader
@app.route("/requirements/")
def requirements_text() -> str:
    return f"{background}" "".join(
        f"<p><tt>{i}</tt></p>" for i in requirements.read_text().splitlines()
    )


# fake names and emails for phones generator
def generate_info() -> str:
    name = fake.first_name()
    email = f"{name}@{fake.domain_name()}"
    return f"{name} | {email}"


# users generator
@app.route("/generate-users/")
@app.route("/generate-users/<int:amount>")
def generate_users(amount: int = 100) -> Generator[str, Any, None]:
    for index in range(amount):
        yield f"<p>{index + 1}. {generate_info()}</p>{background}"


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
        f"<p>Average height: {round(average_height, 2)} cm</p>"
        f"<p>Average weigh: {round(average_weight, 2)} kg</p>"
        f"<p>Number of participants: {total_index}"
        f"{background}"
    )


@app.route("/phones/create")
@use_args(
    {
        "contact_name": fields.Str(required=True),
        "phone_value": fields.Int(required=True),
    },
    location="query",
)
def phones__create(args):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "INSERT INTO phones (contact_name, phone_value) VALUES (:contact_name, :phone_value);",
                {
                    "contact_name": args["contact_name"],
                    "phone_value": args["phone_value"],
                },
            )

    return "Ok"


@app.route("/phones/read-all")
def phones__read_all():
    with DBConnection() as connection:
        phones = connection.execute("SELECT * FROM phones;").fetchall()

    return "<br>".join(
        [
            f"{background}"
            f'{phone["id"]}: {phone["contact_name"]} - {phone["phone_value"]}'
            for phone in phones
        ]
    )


@app.route("/phones/read/<int:id>")
def phones__read(id: int):
    with DBConnection() as connection:
        phone = connection.execute(
            "SELECT * " "FROM phones " "WHERE (id=:id);",
            {
                "id": id,
            },
        ).fetchone()

    return f'{phone["id"]}: {phone["contact_name"]} - {phone["phone_value"]}'


@app.route("/phones/update/<int:id>")
@use_args({"phone_value": fields.Str(), "contact_name": fields.Str()}, location="query")
def phones__update(
    args,
    id: int,
):
    with DBConnection() as connection:
        with connection:
            contact_name = args.get("contact_name")
            phone_value = args.get("phone_value")
            if contact_name is None and phone_value is None:
                return Response(
                    "Need to provide at least one argument",
                    status=400,
                )

            args_for_request = []
            if contact_name is not None:
                args_for_request.append("contact_name=:contact_name")
            if phone_value is not None:
                args_for_request.append("phone_value=:phone_value")

            args_2 = ", ".join(args_for_request)

            connection.execute(
                "UPDATE phones " f"SET {args_2} " "WHERE id=:id;",
                {
                    "id": id,
                    "phone_value": phone_value,
                    "contact_name": contact_name,
                },
            )

    return f"ID: {id} updated"


@app.route("/phones/delete/<int:id>")
def phones__delete(id):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "DELETE " "FROM phones " "WHERE (id=:id);",
                {
                    "id": id,
                },
            )

    return f"ID: {id} deleted"


create_table()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
