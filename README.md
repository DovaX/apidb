# apidb
Autogenerate API based on DB structure directly from Python using ORM

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install apidb.

```bash
pip install apidb
```
from fastapi import FastAPI
import apidb.apidb_core as ad
import uvicorn


## Usage
```python

description = """
This is your API
"""

app = FastAPI(title="Example API",
    description=description,
    version="1.0.0",
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
```
![obrazek](https://user-images.githubusercontent.com/29150831/214747236-0827330f-7c17-4749-a3ac-0b98003e741d.png)

## Current scope
Aims: Easy generation of API in Fastapi + Flask based on structure in DB (current dialects: MySQL, PostgreSQL, SQL Server, Mongo) or on series of predefined functions

Done: Flask and FastAPI simple example

Todo: Generalization


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
