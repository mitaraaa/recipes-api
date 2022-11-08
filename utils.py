import json
from http import HTTPStatus


def message(message: str, code: HTTPStatus) -> tuple[str, HTTPStatus]:
    return json.dumps({"code": code, "message": message}), code
