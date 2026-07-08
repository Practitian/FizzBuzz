import asyncio
import os

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="FizzBuzz Main Service",
    description="Fizz + Buzz + Concat сервис",
    version="1.0.0",
)

FIZZ_URL = os.getenv("FIZZ_URL", "http://localhost:8001")
BUZZ_URL = os.getenv("BUZZ_URL", "http://localhost:8002")
CONCAT_URL = os.getenv("CONCAT_URL", "http://localhost:8003")

REQUEST_TIMEOUT = 5.0


class FizzBuzzRequest(BaseModel):
    value: int = Field(..., description="Число для проверки")


class FizzBuzzResponse(BaseModel):
    result: str


async def call_fizz(client: httpx.AsyncClient, value: int) -> str:
    resp = await client.get(f"{FIZZ_URL}/fizz", params={"value": value})
    resp.raise_for_status()
    return resp.json().get("result", "")


async def call_buzz(client: httpx.AsyncClient, value: int) -> str:
    resp = await client.get(f"{BUZZ_URL}/buzz", params={"value": value})
    resp.raise_for_status()
    return resp.json().get("result", "")


async def call_concat(client: httpx.AsyncClient, lhs: str, rhs: str) -> str:
    resp = await client.get(f"{CONCAT_URL}/concat", params={"lhs": lhs, "rhs": rhs})
    resp.raise_for_status()
    return resp.json().get("result", "")


@app.post("/fizzbuzz", response_model=FizzBuzzResponse)
async def fizzbuzz(request: FizzBuzzRequest) -> FizzBuzzResponse:
    value = request.value

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        try:
            fizz_part, buzz_part = await asyncio.gather(
                call_fizz(client, value),
                call_buzz(client, value),
            )
            final_result = await call_concat(client, fizz_part, buzz_part)

        except httpx.ConnectError as exc:
            raise HTTPException(
                status_code=502,
                detail=f"Не получилось( (ошибка 502): {exc}",
            )
        except httpx.TimeoutException as exc:
            raise HTTPException(
                status_code=504,
                detail=f"Не получилось вовремя( (ошибка 504): {exc}",
            )
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=502,
                detail=(
                    f"Не получилось пипец((( (ошибка 502) "
                    f"{exc.response.status_code}: {exc.response.text}"
                ),
            )

    if final_result == "":
        final_result = str(value)

    return FizzBuzzResponse(result=final_result)


@app.get("/health")
async def health():
    """Проверка сервиса + зависимостей."""
    statuses = {}
    async with httpx.AsyncClient(timeout=2.0) as client:
        for name, url in (
            ("fizz", FIZZ_URL),
            ("buzz", BUZZ_URL),
            ("concat", CONCAT_URL),
        ):
            try:
                r = await client.get(f"{url}/docs")
                statuses[name] = "up" if r.status_code == 200 else "unknown"
            except httpx.RequestError:
                statuses[name] = "down"
    return {"status": "ok", "dependencies": statuses}