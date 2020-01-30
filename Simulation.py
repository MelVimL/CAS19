import logging
import os
import matplotlib.pyplot as plt

import networkx as nx
import yaml
from networkx import write_yaml

from fractories import Graphs, Actors, Distributions

log = logging.getLogger(__name__)
BASE_PATH_LAYOUT = "{}/_{}.{}"


class Stats:

    def __init__(self, name, path, config):
        self.name = name
        self.config = config
        self.path = BASE_PATH_LAYOUT.format(path , name, "yml")
        self.number_of_nodes = -1
        self.number_of_edges = -1

    def update(self, simulation):
        actives = self.config["active"]
        if "number_of_nodes" in actives:
            self.number_of_nodes = len(simulation.graph.nodes)
        if "number_of_edges" in actives:
            self.number_of_edges = len(simulation.graph.edges)


    def flush(self, n, ):
        with open(self.path, "a+") as f:
            data = {n: {k: self.__dict__[k] for k in self.__dict__ if k in self.config["active"]}}

            yaml.dump(data=data, stream=f)


class Simulation:
    def __init__(self, config):
        self._config = config
        self._name = self._config.get("name", "Not Defined")

        self._paths = {"snapshot_root": "./snapshots/",
                       "picture_root": "./pictures/",
                       "stat_root": "./stats/"}
        self._create_paths()  # changes the _paths variable!!!
        self._num_of_nodes = self._config.get("nodes")
        self._snapshot_number = 0
        self._draw_number = 0
        self._stats = Stats(name=self._name, path=self._paths["stat_root"],config=self._config.get("stats"))

        self.graph = self._generate_graph()
        self.n = 0

    def _create_paths(self):
        for key in self._paths:
            path = self._paths[key]
            num = 0
            if not os.path.exists(path):
                os.mkdir(path)
            while os.path.exists("{root}{number}_{sim}".format(root=path, number=num, sim=self._name)):
                num += 1
            path = "{root}{number}_{sim}".format(root=path, number=num, sim=self._name)
            os.mkdir(path)
            self._paths[key] = path

    def update(self):
        log.info("Update Simulation: {}".format(self._name))
        self.n += 1

    def stats(self):
        log.info("Creates Stats: {}".format(self._name))
        self._stats.update(self)
        self._stats.flush(self.n)

    def create_snapshot(self):
        log.info("Creates Snapshot: {}_{}".format(self._name, self._snapshot_number))
        write_yaml(self.graph, BASE_PATH_LAYOUT.format(self._paths["snapshot_root"], self._snapshot_number, "yml"))
        self._snapshot_number += 1

    def draw(self):
        log.info("Drawing Graph")
        plt.subplot(212)
        nx.draw(self.graph)
        plt.savefig(BASE_PATH_LAYOUT.format(self._paths["picture_root"], self._draw_number, "pdf"))
        self._draw_number += 1

    def _create_graph(self):
        return self._populate_graph(self._generate_graph())

    def _generate_graph(self):
        settings = self._config.get("graph").get("generator_function")
        function_name = settings.get("name")
        options = dict(settings.get("options", {}))
        options.update({"n": self._num_of_nodes})

        return Graphs.func_by_name(function_name)(**options)

    def _populate_graph(self, graph):
        actor_settings = self._config.get("actor")
        gen_settings = actor_settings.get("generator_function")
        dis_settings = actor_settings.get("distribution_function")

        gen_function_name = gen_settings.get("name")
        gen_options = gen_settings.get("options")

        dis_function_name = dis_settings.get("name")
        dis_options = dict(dis_settings.get("options"))     # Makes a copy because i don't want a mutable config.
        dis_options.update({"graph": graph})

        positions = Distributions.get_func_by_name(dis_function_name)(**dis_options)
        actors = [Actors.get_func_by_name(gen_function_name)(**gen_options) for x in range(len(graph.nodes))]

        for pos, actor in zip(positions, actors):
            graph.nodes[pos]["actor"] = actor

        return graph


