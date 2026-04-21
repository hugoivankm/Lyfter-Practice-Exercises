from enum import StrEnum, auto
from typing import Any, Generator


class Status(StrEnum):
    """
    Valid statuses for a task.
    """

    PENDING = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()


class Task:
    def __init__(
        self,
        id: int,
        title: str,
        description: str = "",
        status: Status = Status.PENDING,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.status = status

    def __iter__(self) -> Generator[tuple[str, Any], None, None]:
        yield "id", self.id
        yield "title", self.title
        yield "description", self.description
        yield "status", self.status

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the task to a dictionary.
        """
        return dict(self)

    def __str__(self):
        return f" id: {self.id}, title: {self.title}, description: {self.description}, status: {self.status}"

    def __repr__(self) -> str:
        return self.__str__()


class TaskManager:
    def __init__(self):
        self.tasks: dict[int, Task] = {}
        self.current_id = 1

    def save(self, task: Task):
        self.tasks[self.current_id] = task
        self.current_id += 1

    def delete(self, id: int) -> bool:
        if id in self.tasks:
            del self.tasks[id]
            return True
        return False

    def add_task(self, task_data: dict[str, Any] | None) -> Task:
        if "title" not in task_data or "description" not in task_data:
            return None

        title = task_data.get("title")
        description = task_data.get("description")

        if not title.strip() or not description.strip():
            return None

        new_task = Task(self.current_id, title, description, Status.PENDING)
        self.save(new_task)
        return new_task

    def get_all(self) -> list[dict]:
        return [task.to_dict() for task in self.tasks.values()]

    def get_by_id(self, id: int):
        return self.tasks.get(id)

    def edit(self, id: int, task_data: dict) -> Task | None:
        original_task: Task = self.get_by_id(id)
        if not original_task:
            return None

        candidate = copy.deepcopy(original_task)

        if "title" in task_data:
            if not task_data["title"].strip():
                return None
            candidate.title = task_data["title"]
        if "description" in task_data:
            if not task_data["description"].strip():
                return None
            candidate.description = task_data["description"]
        if "status" in task_data:
            status: str = task_data.get("status", "").lower()
            try:
                candidate.status = Status(status)
            except ValueError:
                return None
        
        self.delete(original_task.id)
        self.save(candidate)

        return candidate
