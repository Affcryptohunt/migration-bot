import redis
from rq import Queue

redis_conn = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

q = Queue("default", connection=redis_conn)
