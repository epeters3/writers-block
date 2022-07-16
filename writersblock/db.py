import os
import redis

REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]

db = redis.Redis(
    host=REDIS_HOST, port=REDIS_PORT, charset="utf-8", decode_responses=True
)

QUEUE_NAME = "sequence_queue"
HASH_NAME = "sequence_hash"


def enqueue(prompt: str) -> bool:
    """
    Add a prompt to the queue for GPT-2 to grab
    and continue.
    """
    return db.lpush(QUEUE_NAME, prompt)


def dequeue() -> str:
    """
    Remove and return the next prompt from the queue.
    TODO: Support removing a whole batch of prompts.
    """
    return db.lpop(QUEUE_NAME)


def get_queue_len() -> int:
    """Get the number of prompts in the queue"""
    return db.llen(QUEUE_NAME)


def get_continuation(prompt: str) -> str:
    """
    Get GPT-2's continuation of the prompt,
    if it's been created already.
    """
    return db.hget(HASH_NAME, prompt)


def set_continuation(prompt: str, continuation: str) -> bool:
    """
    Add a continuation that GPT-2 has created, identified
    by its prompt.
    """
    return db.hset(HASH_NAME, prompt, continuation)


def count_continuations() -> int:
    """
    Get the number of prompts that already
    have continuations created.
    """
    return len(db.hkeys(HASH_NAME))
