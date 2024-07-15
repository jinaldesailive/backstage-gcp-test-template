from fastapi import FastAPI
import uvicorn
from google.cloud import spanner
from google.cloud.spanner_admin_instance_v1.types import spanner_instance_admin
from google.cloud.spanner_v1 import DirectedReadOptions, param_types
from google.cloud.spanner_v1.data_types import JsonObject
from google.protobuf import field_mask_pb2  # type: ignore

app = FastAPI()
instance_id="appdb"
database_id="tododb"

@app.get("/hc/")
def healthcheck():
    return 'Health - OK'

@app.get("/db/")
def get_db_data():
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    output1=""

    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            "SELECT id, title, status FROM tasks"
        )

        for row in results:
            output1+="Task ID: {}, Task Title: {}, Task Status: {}".format(*row)
    
    return output1;

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=8080, log_level="info")
    server = uvicorn.Server(config)
    server.run()