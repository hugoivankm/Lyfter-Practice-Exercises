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

    def __str__(self):
        return f" id: {self.id}, title: {self.title}, description: {self.description}, status: {self.status}"

    def __repr__(self) -> str:
        return self.__str__()

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the task to a dictionary.
        """
        return dict(self)


class TaskManager:
    def __init__(self):
        self.tasks: dict[int, Task] = {}
        self.current_id = 1

    def save(self, task: Task):
        self.tasks[self.current_id] = task

    def delete(self, id: int) -> bool:
        if id in self.tasks:
            del self.tasks[id]
            return True
        return False
    
    def is_empty(self) -> bool:
        return len(self.tasks) == 0

    def get_all(self) -> list[dict[str, str]]:
        return [task.to_dict() for task in self.tasks.values()]

    def get_by_id(self, id: int):
        return self.tasks.get(id)


    def add_task(self, task_data: dict[str, Any]) ->  dict[str, Any] | None:
        if "title" not in task_data or "description" not in task_data:
            return None

        title: str | None = task_data.get("title")
        if not title:
            return None

        description = task_data.get("description")
        if not description:
            return None

        if not title.strip() or not description.strip():
            return None

        new_task = Task(self.current_id, title, description, Status.PENDING)

        self.save(new_task)
        self.current_id += 1
        
        return new_task
    
    def edit(self, id: int, task_data: dict[str, Any]) ->  dict[str, Any] | None:

        original_task: Task | None = self.get_by_id(id)
        if not original_task:
            return None

        candidate = Task(
            id=original_task.id,
            title=original_task.title,
            description=original_task.description,
            status=original_task.status
        )
        try:
            if "title" in task_data:
                title: str = task_data["title"]
                if not title.strip():
                    return None
                candidate.title = title

            if "description" in task_data:
                description = task_data["description"]
                if not description.strip():
                    return None
                candidate.description = description

            if "status" in task_data:
                candidate.status = Status(task_data["status"].lower())

        except(ValueError, KeyError, AttributeError):
            return None

        self.tasks[id] = candidate
        return candidate
    
    def filter_by_status(self, status_filter: str | None = None) -> dict[int, dict[str, Any]]:
        
        all_tasks = {t_id: t.to_dict() for t_id, t in self.tasks.items()}
        
        if not status_filter:
            return all_tasks
        
        try:
            target_status = Status(status_filter.lower())
            return {
                t_id: t_dict
                for t_id, t_dict in all_tasks.items()
                if t_dict["status"] == target_status
            }

        except ValueError:
            return {} 


