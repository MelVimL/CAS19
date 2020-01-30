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
        setup_logger(self.config.get("logger"))

    def update(self):
        simulations = self.__create_simulations()
        self.__start_all_simulations(simulations)

        self.__wait_for_all_simulations()
        return False

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
        for thread in self.threads:
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


if __name__ == "__main__":
    app = App()
    app.run()
