from fastapi import FastAPI

app = FastAPI(title="Concat Microservice")

@app.get("/concat")
def concat(lhs: str = "", rhs: str = ""):
    return {"result": lhs + rhs}
