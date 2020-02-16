import logging
import os
import matplotlib.pyplot as plt

import networkx as nx
import yaml
from networkx import write_yaml

from actors import Actor
from fractories import Graphs, Actors, Distributions, Rules

log = logging.getLogger(__name__)
BASE_PATH_LAYOUT = "{}/{}.{}"


class Stats:

    def __init__(self, name, path, config):
        self.name = name
        self.config = config
        self.path = BASE_PATH_LAYOUT.format(path, name, "yml")
        self.number_of_nodes = -1
        self.number_of_edges = -1
        self.average_orientation = -1
        self.graph_density = -1
        self.graph_transitivity = -1

    def update(self, simulation):
        actives = self.config["active"]
        self.number_of_nodes = len(simulation.graph.nodes)
        self.number_of_edges = len(simulation.graph.edges)
        e = self.number_of_edges
        n = self.number_of_nodes

        if "average_orientation" in actives:
            sum_of_orientation = 0
            for node_a, node_b in simulation.graph.edges:
                actor_a = simulation.graph.nodes[node_a]["actor"]
                actor_b = simulation.graph.nodes[node_b]["actor"]
                sum_of_orientation += actor_a.orientation(actor_b)
            self.average_orientation = -1 if e == 0 else float((1 / e) * sum_of_orientation)
        if "graph_density" in actives:
            self.graph_density = nx.density(simulation.graph)
        if "graph_transitivity" in actives:
            self.graph_transitivity = nx.transitivity(simulation.graph)

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
        self._stats = Stats(name=self._name, path=self._paths["stat_root"], config=self._config.get("stats"))

        self.graph = self._create_graph()
        self.n = 0

    def _create_paths(self):
        for key in self._paths:
            cur_path = self._paths[key]
            n = 0
            if not os.path.exists(cur_path):
                os.mkdir(cur_path)
            test_path = "{root}{n}".format(root=cur_path, n=n)

            while os.path.exists(test_path):
                if not [s for s in os.listdir(test_path) if self._name in s]:
                    log.debug("Didn't found a File in the directory.")
                    break
                n += 1
                test_path = "{root}{n}".format(root=cur_path, n=n)

            cur_path = test_path

            if not os.path.exists(cur_path):
                os.mkdir(cur_path)
            self._paths.update({key: cur_path})



    def update(self):
        log.info("Update Simulation: {}".format(self._name))
        actions = self._generate_action()

        for action in actions:
            for sub_action in action:
                if sub_action["name"] is "remove_edge":
                    log.debug("Remove Edge")
                    self._remove_edge_(sub_action)
                elif sub_action["name"] is "add_edge":
                    log.debug("Add Edge")
                    self._add_edge(sub_action)
                elif sub_action["name"] is "add_node":
                    log.debug("Add Node")
                    self.graph.add_node()
                elif sub_action["name"] is "remove_node":
                    log.debug("Remove Node")
                    self.graph.remove_node(sub_action["node_x"])
        self.n += 1

    def _remove_edge_(self, action):
        node_x = action["node_x"]
        node_z = action["node_z"]
        if self.graph.has_edge(node_x, node_z):
            self.graph.remove_edge(node_x, node_z)

    def _add_edge(self, action):
        node_x = action["node_x"]
        node_z = action["node_z"]
        if not self.graph.has_edge(node_x, node_z):
            self.graph.add_edge(node_x, node_z)

    def _generate_action(self):
        result = []
        for edge in self.graph.edges:
            for conf in self._config.get("rules"):
                result.append(Rules.create_actions_by_name(edge=edge, graph=self.graph, conf=conf))
        return result

    def stats(self):
        log.info("Creates Stats: {}".format(self._name))
        self._stats.update(self)
        self._stats.flush(self.n)

    def create_snapshot(self):
        log.info("Creates Snapshot: {}_{}".format(self._name, self._snapshot_number))
        write_yaml(self.graph, BASE_PATH_LAYOUT.format(self._paths["snapshot_root"], self._name, "yml"))
        self._snapshot_number += 1

    def draw(self):
        log.info("Drawing Graph")
        #plt.subplot(212)
        #nx.draw(self.graph)
        #plt.savefig(BASE_PATH_LAYOUT.format(self._paths["picture_root"],
        #                                    "_".join([self._name, str(self._draw_number)]),
        #                                    "pdf"))
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
        log.debug(dis_function_name)
        dis_options = dict(dis_settings.get("options", {}))  # Makes a copy because i don't want a mutable config.
        dis_options.update({"graph": graph})

        positions = Distributions.func_by_name(dis_function_name)(**dis_options)
        actors = [Actors.func_by_name(gen_function_name)(**gen_options) for x in range(len(graph.nodes))]

        log.info("Populate Graph with Actors.")
        for pos, actor in zip(positions, actors):
            actor = Actor(actor)
            graph.nodes[pos]["actor"] = actor

        return graph
