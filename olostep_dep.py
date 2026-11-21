from fastapi import Request
from olostep import AsyncOlostep


def get_olostep(request: Request) -> AsyncOlostep:
    return request.app.state.olostep
