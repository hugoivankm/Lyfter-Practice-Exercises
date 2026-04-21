from flask import Flask, jsonify, request

from tasks import TaskManager, Task, Status

app = Flask(__name__)
data_source = TaskManager()


@app.route("/tasks", methods=["GET"])
def list_tasks():
    try:
        status_filter: Status | None = request.args.get("status_filter")
        filtered_data_source = data_source.get_all()
        if status_filter is not None:
            filtered_data_source = {
                k: v
                for k, v in filtered_data_source.items()
                if v.status == status_filter
            }
        return jsonify(filtered_data_source)
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

        new_task = data_source.add_task(data)
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
        if not request.is_json:
            return jsonify({"error": "Invalid or missing MIME type"}), 400

        data: dict = request.get_json(silent=True)
        if not data:
            return {"message": "No JSON data received"}, 400
        
        updated_task: Task = data_source.edit(id, data)

        if not updated_task:
            return {"message": "Malformed JSON values"}, 400 

        return jsonify(updated_task.to_dict())
    except Exception:
        return jsonify(
            message="Oops something went wrong while editing your tasks"
        ), 500


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id: int):
    return jsonify({"error": "NOT IMPLEMETED"})


if __name__ == "__main__":
    app.run(host="localhost", debug=True)
