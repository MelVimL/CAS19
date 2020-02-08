import threading

from Simulation import Simulation
from simulation_worker import SimulationWorker
from utils.logger import setup_logger
from utils.config_loader import ConfigLoader
import logging


log = logging.getLogger(__name__)


class App:

    def __init__(self):
        self.threads = []
        self.config = ConfigLoader.load()
        self.max_threads = self.config.get("simulation").get("max_threads")
        self.simulations = self.__create_simulations()
        setup_logger(self.config.get("logger"))


    def update(self):
        self._start_n_simulations(n=self.max_threads, simulations=self.simulations)
        self.__wait_for_all_simulations()
        log.info("{} Simulation(s) left.".format(len(self.simulations)))
        return self.simulations

    def run(self):
        while self.update():
            pass

    def __create_simulations(self):
        result = []

        for config in self.config["simulations"]:
            result.append(self.__create_simulation(config=config))

        log.info("All Simulations created.")
        return result

    @staticmethod
    def __create_simulation(config):
        """
        Creates a Simulation.
        :param config: config with the Simulation parameters.
        :return: a Simulation instance.
        """
        log.info("Simulation created.")

        return Simulation(config=config)

    def __wait_for_all_simulations(self):
        """
        Waits until all threads are done.
        :return: None
        """
        for i in range(len(self.threads)):
            thread = self.threads.pop()
            thread.join()
            log.info("Thread joined.")

    def __start_all_simulations(self, simulations):
        """
        Starts all threads.

        :param simulations: a List of Simulations
        :return: None
        """
        for simulation in simulations:
            thread = self.__start_simulation(simulation)
            self.threads.append(thread)

    def __start_simulation(self, simulation):
        """
        Starts a Simulation in a Thread.

        :param simulation: an instance of the Simulation class.
        :return: a thread for later joining.
        """
        thread = SimulationWorker(simulation, config=self.config)
        thread.start()
        log.info("Thread started.")

        return thread

    def _start_n_simulations(self, n, simulations):
        for i in range(n):
            if simulations:
                thread = self.__start_simulation(simulations.pop(0))
                self.threads.append(thread)


if __name__ == "__main__":
    app = App()
    app.run()
