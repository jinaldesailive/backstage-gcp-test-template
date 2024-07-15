from fastapi import FastAPI
import uvicorn
from google.cloud import spanner
from fastapi.responses import HTMLResponse

app = FastAPI()
instance_id="appdb"
database_id="tododb"

@app.get("/hc/")
def healthcheck():
    return 'Health - OK'

@app.get("/db/", response_class=HTMLResponse)
def get_db_data():
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    output1="Task ID, Task Title, Task Status <br>"

    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            "SELECT id, title, status FROM tasks"
        )
        for row in results:
            output1+=  row[0] + ", " + row[1] + ", " + row[2] + "<br>"
    return output1;

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=8080, log_level="info")
    server = uvicorn.Server(config)
    server.run()