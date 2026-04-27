from typing import Any


class ConfigDistributor:
    def __init__(self, config: dict[str, dict[Any, dict[str, Any]]]):
        self.config = config

    def does_task_fit(self, task: dict, worker: dict) -> bool:
        res = True
        for param, vals in self.config.items():
            task_val = task.get(param)
            if task_val is not None:
                req = vals.get(task.get(param))
                if req is not None:
                    for par, val in req:
                        if worker.get(par) is not None:
                            res = worker[par] == val
                        else:
                            res = False
        return res
