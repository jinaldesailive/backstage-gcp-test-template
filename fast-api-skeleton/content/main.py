from fastapi import FastAPI
import uvicorn
from google.cloud import spanner
from fastapi.responses import HTMLResponse
import json

app = FastAPI()
instance_id="appdb"
database_id="tododb"

@app.get("/hc/")
def healthcheck():
    return 'Health - OK'

@app.get("/tasks/")
def get_db_data():
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            "SELECT id, title, status FROM tasks"
        )
    return results.to_dict_list();

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=8080, log_level="info")
    server = uvicorn.Server(config)
    server.run()