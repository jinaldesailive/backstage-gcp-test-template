from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/hc/")
def healthcheck():
    return 'Health - OK'

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=8080, log_level="info")
    server = uvicorn.Server(config)
    server.run()