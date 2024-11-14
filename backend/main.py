from fastapi import FastAPI, Request, Header, HTTPException
import logging
from typing import Annotated
from uvicorn import run

app = FastAPI()


logger = logging.getLogger("middleware_logger")
handler = logging.FileHandler("genreal.log")
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)



@app.middleware("http")
async def log_requests(request: Request, call_next):
    if "X-Custom-Header" in request.headers:
        response = await call_next(request)
        logger.info(f"Request Method: {request.method}, Request URL: {request.url}")
        return response
    else:
        raise HTTPException(400, "Request must include X-Custom-Header")

@app.get('/')
def index():
    return {"Hello" : "World"}


@app.get("/header_check")
async def check(X_Custom_Header: Annotated[str | None, Header()] = None):
    return {"header": X_Custom_Header}


if __name__ == "__main__":
    run(app=app, port=8000)

