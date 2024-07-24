from typing import Annotated, Union

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(q: Annotated[Union[list[str], None], Query()] = None):
    query_items = {"q": q}
    return query_items
#using list
@app.get("/items1/")
async def read_items(q: Annotated[list, Query()] = []):
    query_items = {"q": q}
    return query_items
# in this case, FastAPI won't check the contents of the list.
#