from fastapi import FastAPI

app = FastAPI(title="fizz-microservice")

@app.get("/fizz")
def fizz(value: int):
    if value % 3 == 0:
        result = "fizz"
    else:
        result = ""
    return {"result": result}