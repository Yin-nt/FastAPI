from typing import Union

from fastapi import FastAPI, Query
from typing_extensions import Annotated

app = FastAPI()


@app.get("/items/")
async def read_items(
        q: Annotated[Union[str, None], Query(min_length = 3, max_length=50, pattern="^fixedquery$")] = None):
    # using Query inside of Annotated you cannot use the default parameter for Query.
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
#Advantages of Annotated: call that same function in other places without FastAPI,
#a required parameter (without a default value), your editor will let you know with an error
#Having a default value of any type, including None, makes the parameter optional (not required).

