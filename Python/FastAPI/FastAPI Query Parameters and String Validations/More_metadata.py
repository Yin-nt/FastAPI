from typing import Annotated, Union
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(
    q: Annotated[
        Union[str, None],
        Query(
            default=...,
            min_length=3,
            max_length=50,
            title="Search Query",
            description="This is the query parameter used for searching items",
            alias="search-query",
            example="foo"
        )
    ]
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
#alias="search-query": Đặt một bí danh (alias) cho tham số q, giúp người dùng có thể sử dụng tên khác khi gửi request.