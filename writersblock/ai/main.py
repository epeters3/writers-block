import time

from writersblock.db import get_queue_len, dequeue, set_continuation

if __name__ == "__main__":
    # TODO: Run process loop that grabs jobs
    # off the redis queue and runs them through GPT-2
    while True:
        queue_len = get_queue_len()
        if queue_len > 0:
            # TODO: Grab job from queue and run it through GPT-2,
            # finally storing it in the continuations hash.
            prompt = dequeue()
            continuation = ...
            set_continuation(prompt, continuation)
        else:
            time.sleep(0.01)

