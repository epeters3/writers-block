import time
import os

from flask import Flask, jsonify, request, send_from_directory

from writersblock.db import enqueue, get_continuation

app = Flask("HTTP API Server")


@app.route("/")
def landing():
    return send_from_directory(os.path.dirname(__file__), "index.html")


@app.route("/append-to-sequence", methods=["POST"])
def append_to_sequence():
    req_data = request.get_json()

    if "text" not in req_data or not isinstance(req_data["text"], str):
        return (
            jsonify({"result": "Request must have a 'text' attribute of type string."}),
            400,
        )

    prompt = req_data["text"]
    if len(prompt) == 0:
        return (
            jsonify({"result": "Your text must not be empty."}),
            400,
        )

    # If the continuation for this prompt is already stored in the
    # database, we don't need to add it to the queue.
    result = get_continuation(prompt)
    if result is not None:
        return jsonify({"result": result})

    # Put request in redis server then listen
    # for a response
    enqueue(prompt)
    while True:
        # Listen until the continuation is available
        result = get_continuation(prompt)
        if result is not None:
            # The continuation is here
            break
        time.sleep(0.01)

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0")
