from fastapi import FastAPI
import uvicorn
from sqlalchemy import MetaData, Table, create_engine, selectimport 

app = FastAPI()
engine = create_engine(
    "spanner:///projects/png-gcp-learning-poc/instances/appdb/databases/tododb"
)
table = Table("tasks", MetaData(bind=engine), autoload=True)

@app.get("/hc/")
def healthcheck():
    return 'Health - OK'

@app.get("/db/")
def get_db_data():
    with engine.begin() as connection:
    for row in connection.execute(select(["*"], from_obj=table)).fetchall():
        print(row)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=8080, log_level="info")
    server = uvicorn.Server(config)
    server.run()