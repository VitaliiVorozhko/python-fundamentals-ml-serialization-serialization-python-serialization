import json
import jsonschema
from jsonschema import validate
import csv

student_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "department_id": {"type": "integer"}
        },
        "required": ["name", "department_id"]
    }
}

department_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"}
        },
        "required": ["id", "name"]
    }
}


class InvalidInstanceError(Exception):
    pass


class DepartmentName(Exception):
    pass


def validate_json(data, schema):
    try:
        validate(instance=data, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError:
        return False


def user_with_department(csv_file, user_json, department_json):
    with open(user_json, "r") as f:
        users = json.load(f)

    with open(department_json, "r") as f:
        departments = json.load(f)

    if not validate_json(users, student_schema):
        raise InvalidInstanceError("Users data is not valid")

    if not validate_json(departments, department_schema):
        raise InvalidInstanceError("Departments data is not valid")

    dep_names = {}
    for dep in departments:
        dep_names[dep["id"]] = dep["name"]

    rows = []
    for user in users:
        dep_id = user["department_id"]
        if dep_id not in dep_names:
            raise DepartmentName(f"Department with id {dep_id} does not exist")
        rows.append([user["name"], dep_names[dep_id]])

    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "department"])
        writer.writerows(rows)