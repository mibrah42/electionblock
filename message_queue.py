from flask import Flask, request
import redis
from rq import Queue
from background_task import background_task

app = Flask(__name__)

r = redis.Redis()
queue = Queue(connection=r)


@app.route("/task")
def add_task():
    if request.args.get("n"):
        job = queue.enqueue(background_task, request.args.get("n"))
        q_len = len(queue)
        return f"Task {job.id} added to queue at {job.enqueued_at}. {q_len} tasks in the queue"

    return "No value for n"


if __name__ == "__main__":
    app.run(debug=True)
