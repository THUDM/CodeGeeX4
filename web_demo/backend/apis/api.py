class API:
    def call(self, **kwargs):
        return self.__call__(**kwargs)

    def __call__(self, **kwargs):
        search_kwargs = {'query': kwargs['query'], 'freshness': 'month'}
        search_res = self.search(**search_kwargs)
        return search_res

    @classmethod
    def search(cls, **kwargs) -> list[str]:
        raise NotImplementedError
