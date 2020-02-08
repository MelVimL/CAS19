import threading as th
import queue as q

import yaml

STOP_STAT = "STOP"

class StatsFileHandler:

    class StatsWriter(th.Thread):
        def __init__(self, queue, file_path):
            self.running = True
            self.queue = queue
            self.file_path = file_path
            self.f_pointer_map = {}

        def _handle(self, stat):
            if self._is_time_to_stop(stat):
                self.running = False
                return
            name = stat["name"]
            value = stat["stat"]
            file_name = self.f_pointer_map.setdefault(name, "".join([self.file_path, name, ".yml"]))
            with open(file_name, "a+") as f:
                yaml.dump(data=value, stream=f)

        def run(self):
            while self.running:
                self._handle(self.queue.pop())

        def _is_time_to_stop(self, task):
            return task is STOP_STAT


    def __init__(self, path):
        self.queue = q.Queue()
        self.worker = self.StatsWriter(self.queue, path)

    def add_stats(self, name, value):
        self.queue.put({"name": name,
                        "stat": value})

    def start(self):
        self.worker.start()

    def stop(self):
        pass

