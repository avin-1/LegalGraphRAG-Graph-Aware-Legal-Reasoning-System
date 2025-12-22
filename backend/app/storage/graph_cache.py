GRAPH_CACHE = {}

def make_key(case_ids):
    return tuple(sorted(case_ids))

def get_cached(case_ids):
    return GRAPH_CACHE.get(make_key(case_ids))

def set_cache(case_ids, result):
    GRAPH_CACHE[make_key(case_ids)] = result