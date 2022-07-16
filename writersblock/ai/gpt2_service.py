import os
import time

from transformers import pipeline

from writersblock.db import dequeue, set_continuation, get_queue_len


def run_gpt2_service(model_name="distilgpt2", batch_size=1, queue_check_freq=0.01):
    """
    Interactively run the model.

    Parameters
    ----------
    model_name : str
        The name of the HuggingFace model to use for text generation.
    batch_size : int
        The number of prompts to generate for at once.
    queue_check_freq : float
        The time in seconds to wait between each check to Redis to see if any samples are available.
    """

    print(f" * Initializing {model_name}")

    pipe = pipeline("text-generation", model=model_name)

    print(" * Listening to queue")

    while True:

        queue_len = get_queue_len()
        if queue_len > 0:
            print(" * Jobs found, starting new batch")
            # Grab job from queue and run it through GPT-2,
            # finally storing it in the continuations hash.
            prompt = dequeue()
            print("prompt:", prompt)
            continuation = pipe(prompt)[0]["generated_text"][len(prompt) :]
            print("continuation:", continuation)
            set_continuation(prompt, continuation)
        else:
            time.sleep(queue_check_freq)
