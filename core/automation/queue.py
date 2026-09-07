from collections import deque


class TaskQueue:
    def __init__(self):
        self.queue = deque()

    def add(self, task):
        self.queue.append(task)

    def next(self):
        if not self.queue:
            return None

        return self.queue.popleft()

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)

    def clear(self):
        self.queue.clear()
