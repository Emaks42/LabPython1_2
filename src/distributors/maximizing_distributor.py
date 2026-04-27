class MaximizingDistributor:
    def __init__(self, worker_param: str, scaling_task_param: str | None = None, buffer_size: int = 3):
        self.worker_param = worker_param
        self.scaling_task_param = scaling_task_param
        self.buf_size = buffer_size
        self.buffer: list[int] = []

    def does_task_fit(self, task: dict, worker: dict) -> bool:
        param = worker.get(self.worker_param) * (task.get(self.scaling_task_param, 1))
        if param is not None:
            self.buffer.append(param)
            if len(self.buffer) == self.buf_size:
                if param == max(self.buffer):
                    return True
                else:
                    self.buffer.pop(0)
                    return False
        return False
