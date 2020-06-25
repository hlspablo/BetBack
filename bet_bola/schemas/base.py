class BaseResolver():
    queryset = None

    def __init__(self, request, **kwargs):
        self.request = request
        self.kwargs = kwargs

    def get_queryset(self):
        return self.queryset