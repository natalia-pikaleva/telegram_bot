import requests
from typing import Dict


def _make_response(method: str, url: str, headers: Dict, timeout: int, success=200):
    response = requests.request(method, url, headers=headers, timeout=timeout)

    status_code = response.status_code
    if status_code == success:
        return response

    return status_code


def _get_movie(
    method: str,
    url: str,
    headers: Dict,
    movie_name: str,
    timeout: int,
    func=_make_response,
):

    response = func(method, url=url, headers=headers, timeout=timeout)
    return response


class SiteApiInterface:

    @staticmethod
    def get_movie():
        return _get_movie


if __name__ == "__main__":
    _make_response()
    _get_movie()

    SiteApiInterface()
