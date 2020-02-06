import threading as th
import logging

log = logging.getLogger(__name__)


class SimulationWorker(th.Thread):

    def __init__(self, simulation, config):
        super().__init__()
        self.simulation = simulation
        self.config = config
        self.loops = self.config.get("simulation").get("loops_per_run")
        self.stats_interval = self.config.get("simulation").get("stats_interval")
        self.snapshot_interval = self.config.get("simulation").get("snapshot_interval")
        self.draw_interval = self.config.get("simulation").get("draw_interval")

    def run(self):
        log.info("Simulation worker {} runs.".format(self.simulation._name))
        for n in range(self.loops):
            if self.__is_time_for_stats(n):
                self.simulation.stats()
            if self.__is_time_for_snapshot(n):
                self.simulation.create_snapshot()
            if self.__is_time_for_draw(n):
                self.simulation.draw()

            self.simulation.update()

    def __is_time_for_snapshot(self, n):
        return n % self.snapshot_interval == 0 or n == 0

    def __is_time_for_stats(self, n):
        return n % self.stats_interval == 0 or n == 0

    def __is_time_for_draw(self, n):
        return n % self.draw_interval == 0 or n == 0
