QUERY_CACHE = {}

def get_query(query: str):
    return QUERY_CACHE.get(query)

def set_query(query: str, result):
    QUERY_CACHE[query] = result