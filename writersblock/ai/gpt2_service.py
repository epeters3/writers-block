import sys
import os
import json
import os
import time

import numpy as np
import tensorflow as tf

from writersblock.db import dequeue, set_continuation, get_queue_len

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "gpt-2", "src"))
import model, sample, encoder

# path to parent folder containing model subfolders (i.e.
# contains the <model_name> folder)
MODELS_DIR = os.path.join(os.path.dirname(__file__), "gpt-2", "models")


def run_gpt2_service(
    model_name="117M",
    seed=None,
    nsamples=1,
    batch_size=1,
    length=None,
    temperature=1,
    top_k=40,
    top_p=1,
    queue_check_freq=0.01,
):
    """
    Interactively run the model
    :model_name=117M : String, which model to use
    :seed=None : Integer seed for random number generators, fix seed to reproduce
     results
    :nsamples=1 : Number of samples to return total
    :batch_size=1 : Number of batches (only affects speed/memory).  Must divide nsamples.
    :length=None : Number of tokens in generated text, if None (default), is
     determined by model hyperparameters
    :temperature=1 : Float value controlling randomness in boltzmann
     distribution. Lower temperature results in less random completions. As the
     temperature approaches zero, the model will become deterministic and
     repetitive. Higher temperature results in more random completions.
    :top_k=0 : Integer value controlling diversity. 1 means only 1 word is
     considered for each step (token), resulting in deterministic completions,
     while 40 means 40 words are considered at each step. 0 (default) is a
     special setting meaning no restrictions. 40 generally is a good value.
    :queue_check_freq=.01: The time in seconds to wait between each check to Redis
     to see if any samples are available.
    """

    print(" * Initializing GPT-2")

    if batch_size is None:
        batch_size = 1
    assert nsamples % batch_size == 0

    enc = encoder.get_encoder(model_name, MODELS_DIR)
    hparams = model.default_hparams()
    with open(os.path.join(MODELS_DIR, model_name, "hparams.json")) as f:
        hparams.override_from_dict(json.load(f))

    if length is None:
        length = hparams.n_ctx // 2
    elif length > hparams.n_ctx:
        raise ValueError(
            "Can't get samples longer than window size: %s" % hparams.n_ctx
        )

    print("Starting up model")

    with tf.Session(graph=tf.Graph()) as sess:
        context = tf.placeholder(tf.int32, [batch_size, None])
        np.random.seed(seed)
        tf.set_random_seed(seed)
        output = sample.sample_sequence(
            hparams=hparams,
            length=length,
            context=context,
            batch_size=batch_size,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
        )

        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join(MODELS_DIR, model_name))
        saver.restore(sess, ckpt)

        print(" * Listening to queue")

        while True:

            queue_len = get_queue_len()
            if queue_len > 0:
                # Grab job from queue and run it through GPT-2,
                # finally storing it in the continuations hash.
                prompt = dequeue()
                print("prompt:", prompt)
                context_tokens = enc.encode(prompt)
                for _ in range(nsamples // batch_size):
                    out = sess.run(
                        output,
                        feed_dict={
                            context: [context_tokens for _ in range(batch_size)]
                        },
                    )[:, len(context_tokens) :]
                    for i in range(batch_size):
                        continuation = enc.decode(out[i])
                        set_continuation(prompt, continuation)
            else:
                time.sleep(0.01)

