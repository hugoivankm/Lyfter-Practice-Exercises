from flask import Flask, jsonify, request, Response
from tasks import TasksManager, ResponseManager

app: Flask = Flask(__name__)
data_manager: TasksManager = TasksManager()
rm = ResponseManager()


@app.route("/tasks", methods=["GET"])
def list_tasks():
    try:
        status_filter = request.args.get("status")
        filtered_tasks = data_manager.filter_by_status(status_filter)

        if filtered_tasks is None:
            return rm.error("Invalid task status", 400)
        
        return rm.success(filtered_tasks)
    except Exception:
        return rm.error("Oops something went wrong while listing your tasks", 500) 


@app.route("/tasks", methods=["POST"])
def create_task():
    try:
        if not request.is_json:
            return rm.error("Invalid or missing MIME type", 400)

        data = request.get_json(silent=True)
        if not data:
            return rm.error("No JSON data received", 400)
        
        new_task = data_manager.add_task(data)
        if new_task is None:
            return rm.error("Tasks must have a non-empty title and description", 400)
      
        return rm.success(new_task, 201) 
    except Exception:
        return rm.error("Oops something went wrong while creating your tasks", 500)


@app.route("/tasks/<int:id>", methods=["PATCH"])
def edit_task(id: int):
    try:
        if not request.is_json:
            return rm.error("Invalid or missing MIME type", 400) 

        data = request.get_json(silent=True)
        if not data:
            return rm.error("No JSON data received", 400) 

        updated_task = data_manager.edit(id, data)

        if updated_task is None:
            return rm.error("Task not found", 404)

        return rm.success(updated_task, 200) 
    except Exception:
        return rm.error("Oops something went wrong while editing your tasks", 500)


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id: int):
    try:
        result: bool = data_manager.delete(id)
        if not result:
            return rm.error("Task not found", 404)
        return Response(status=204)

    except Exception:
        return rm.error("Oops something went wrong while deleting your tasks", 500)

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
