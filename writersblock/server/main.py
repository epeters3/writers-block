import time

from flask import Flask, jsonify, request

from writersblock.db import enqueue, get_continuation

app = Flask("HTTP API Server")


@app.route("/")
def landing():
    return """
    <body>
        <h1>Welcome to Writer's Block!</h1>
        <p>
            Send a POST request to the `/append-to-sequence` endpoint
            containing a text prompt in the body to see what GPT2 will
            add to it!
        </p>
        <p>
            The request should be formatted like this:
        </p>
        <pre>
        {
            "text": "Once upon a time, in a land far away"
        }
        </pre>
        <p>
            GPT-2 will add to the story for you.
        </p>
   </body>
   """


@app.route("/append-to-sequence", methods=["POST"])
def append_to_sequence():
    req_data = request.get_json()

    if "text" not in req_data or not isinstance(req_data["text"], str):
        return (
            {"result": "Request must have a 'text' attribute of type string."},
            400,
        )

    # Put request in redis server then listen
    # for a response
    prompt = req_data["text"]
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
    app.run()

