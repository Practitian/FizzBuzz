from fastapi import FastAPI

app = FastAPI(title="buzz-microservice")

@app.get("/buzz")
def buzz(value: int):
    if value % 5 == 0:
        result = "buzz"
    else:
        result = ""
    return {"result": result}