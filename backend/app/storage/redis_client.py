import redis
import os

class InMemoryRedis:
    """Simple in-memory storage for when Redis is unavailable."""
    def __init__(self):
        self.store = {}
        print("--- [STORAGE] Warning: Redis not connected. Using In-Memory storage. ---")

    def get(self, key):
        return self.store.get(key)
    
    def set(self, key, value):
        self.store[key] = value

    def ping(self):
        return True

# Singleton instance
redis_conn = None

def get_redis_connection():
    global redis_conn
    if redis_conn is not None:
        return redis_conn

    # Try connecting to real Redis
    try:
        redis_url = os.getenv("REDIS_URL")
        if redis_url:
            print(f"--- [STORAGE] Attempting to connect to Redis via REDIS_URL... ---")
            client = redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=1
            )
        else:
            host = os.getenv("REDIS_HOST", "localhost")
            print(f"--- [STORAGE] Attempting to connect to Redis at {host}... ---")
            client = redis.Redis(
                host=host,
                port=6379,
                decode_responses=True,
                socket_connect_timeout=1  # Fast fail
            )
        client.ping()
        print("--- [STORAGE] Connected to Redis successfully. ---")
        redis_conn = client
    except Exception as e:
        print(f"--- [STORAGE] Redis connection failed ({e}). Falling back to In-Memory. ---")
        redis_conn = InMemoryRedis()
    
    return redis_conn

# Initialize immediately
redis_conn = get_redis_connection()