from flask import Flask, jsonify, request, Response
from typing import Any, cast
from tasks import TaskManager, Task, Status

app: Flask = Flask(__name__)
data_manager: TaskManager = TaskManager()


@app.route("/tasks", methods=["GET"])
def list_tasks():
    try:
        status_filter = request.args.get("status")
        filtered_tasks = data_manager.filter_by_status(status_filter)
        return jsonify(filtered_tasks, 200)
    except Exception:
        return jsonify(
            message="Oops something went wrong while listing your tasks"
        ), 500


@app.route("/tasks", methods=["POST"])
def create_task():
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid or missing MIME type"}), 400

        data = request.get_json(silent=True)
        if not data:
            return {"message": "No JSON data received"}, 400

        new_task = data_manager.add_task(data)
        if new_task is None:
            return jsonify(
                {"error": "Tasks must have a non empty title and description"}
            ), 400

        return jsonify(new_task.to_dict())
    except Exception:
        return jsonify(
            message="Oops something went wrong while creating your tasks"
        ), 500


@app.route("/tasks/<int:id>", methods=["PATCH"])
def edit_task(id: int):
    try:
        if data_manager.is_empty():
            return {"error": "No task to change"}, 404
        if not request.is_json:
            return {"error": "Invalid or missing MIME type"}, 400

        data: dict = request.get_json(silent=True)
        if not data:
            return {"message": "No JSON data received"}, 400

        updated_task: Task = data_manager.edit(id, data)

        if not updated_task:
            return {"message": "Malformed JSON values"}, 400

        return jsonify(updated_task.to_dict())
    except Exception:
        return jsonify(
            message="Oops something went wrong while editing your tasks"
        ), 500


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id: int):
    try:
        result: bool = data_manager.delete(id)
        if not result:
            return {"error": "Task not found"}, 404
        return Response(status=204)

    except Exception:
        return jsonify(
            message="Oops something went wrong while deleting your tasks"
        ), 500


if __name__ == "__main__":
    app.run(host="localhost", debug=True)
