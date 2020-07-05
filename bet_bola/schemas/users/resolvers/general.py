from schemas.base import BaseResolver
from decimal import Decimal as dec


class TodoResolver(BaseResolver):
    queryset = None # TODO

    def todo_method(self):
        pass