from fastapi import FastAPI

app = FastAPI(title="concat-microservice")

@app.get("/concat")
def concat(lhs: str = "", rhs: str = ""):
    return {"result": lhs + rhs}