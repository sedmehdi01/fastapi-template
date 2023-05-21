from math import ceil
from fastapi import HTTPException
from pymongo.collection import Collection
from .utils import obj_to_str


class MongoDBPagination:
    def __init__(
        self,
        collection: Collection,
        page: int,
        limit: int,
        filters: dict = {},
        sorted_by: list = None,
        order_by: int = 1
        # project=None,
    ):
        self.collection = collection
        self.page = page
        self.sorted_by = sorted_by
        self.limit = limit
        self.order_by = order_by

        if page > 0:
            self.skip = (page - 1) * self.limit
        else:
            self.skip = 0

        if not filters or not isinstance(filters, dict):
            self.filters = {}
        else:
            self.filters = filters

        if not self.order_by:
            self.order_by = 1

        # self.project = {}

        self.count = 0
        self.num_pages = 0

    def validate(self):
        if self.collection is not None:
            if (self.page == -1 or self.page > 0) and self.limit > 0:
                return True
        return

    async def get_num_pages(self):
        hits = max(1, self.count)
        self.num_pages = ceil(hits / self.limit)
        if self.num_pages < self.page:
            raise HTTPException(404, "Invalid page!")

    async def get_items_in_page(self):
        result = self.collection
        result = result.find(self.filters)
        if self.sorted_by:
            result = result.sort(self.sorted_by, self.order_by)

        if self.page == -1:
            return await result.to_list(self.count)

        return await result.skip(self.skip).limit(self.limit).to_list(self.limit)

    async def get_next_link(self):
        if self.page < self.num_pages:
            return self.page + 1

    async def get_previous_link(self):
        if self.page > 1:
            return self.page - 1

    async def response_pagination(self) -> dict:
        if self.validate():
            self.count = await self.collection.count_documents(self.filters)

            await self.get_num_pages()
            return {
                "meta": {
                    "count": self.count,
                    "next": await self.get_next_link(),
                    "previous": await self.get_previous_link(),
                },
                "data": obj_to_str(await self.get_items_in_page()),
            }
        return {
            "meta": {
                "count": 0,
                "next": None,
                "previous": None,
            },
            "data": [],
        }
