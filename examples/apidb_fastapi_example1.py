
from fastapi import FastAPI

from flask_mysqldb import MySQL 

import dbhydra.dbhydra_core as dh
import apidb.apidb_core as ad
import uvicorn


description = """
This is your API
"""

app = FastAPI(title="Example API",
    description=description,
    version="1.0.0",
    )


db1=dh.Mysqldb(config_file="config-mysql.ini")

app.config={}
app.config['MYSQL_USER'] = db1.DB_USERNAME
app.config['MYSQL_PASSWORD'] = db1.DB_PASSWORD
app.config['MYSQL_DB'] = db1.DB_DATABASE
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['JWT_SECRET_KEY'] = 'secret'



mysql = MySQL(app)
from fastapi.middleware.cors import CORSMiddleware
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



db_api_dict={'workspaces':'read','nodes':['read','create','update','delete']}
column_names=["workspace_name"]


ad.initialize_fastapi(app, db_api_dict, column_names, mysql)


@app.get("/api/v1/custom_workspaces")
def get_workspaces():
    """
    Returns all workspaces
    """
    return {"workspaces": []}


def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__=="__main__":
    run_api()