from typing import Annotated, Union

from fastapi import FastAPI, Query

app = FastAPI()

#not declare a default value
@app.get("/items1/")
async def read_items1(q: Annotated[str, Query(min_length=3)]):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
#use Ellipsis(...)
@app.get("/items2/")
async def read_items2(q: Annotated[str, Query(min_length=3)] = ...):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
#use None
@app.get("/items3/")
async def read_items3(q: Annotated[Union[str, None], Query(min_length=3)] = ...):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
#In most of the cases, when something is required => omit the default => don't have to use ....
#? tại sao không hiện require trong docs ở 2 cách cuối
