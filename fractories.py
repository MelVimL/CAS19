import networkx as nx
import random as r

from actors import Actor


class Graphs:

    def __init__(self):
        pass

    @staticmethod
    def create_complete(**kwargs):
        """
        Creates a completely connected graph.
        :param n: number of nodes.
        :return: a Graph with n Nodes and all connected.
        """
        return nx.generators.complete_graph(kwargs.get("n"))

    @staticmethod
    def create_barabasi_albert(**kwargs):
        return nx.generators.barabasi_albert_graph(n=kwargs.get("n"), m=kwargs.get("m"), seed=None)

    @staticmethod
    def create_clustered_barabasi_albert(**kwargs):
        return nx.generators.barabasi_albert_graph(kwargs.get("n"), seed=None)

    @staticmethod
    def create_watts_strogatz(**kwargs):
        return nx.generators.connected_watts_strogatz_graph()

    @staticmethod
    def create_clustered_watts_strogatz(**kwargs):
        return nx.generators.barabasi_albert_graph(kwargs.get("n"), seed=None)

    @staticmethod
    def create_clustered_powerlaw_cluster(**kwargs):
        return nx.powerlaw_cluster_graph()

    @staticmethod
    def create_powerlaw_cluster(**kwargs):
        return nx.powerlaw_cluster_graph()

    @staticmethod
    def func_by_name(name):
        """
        This function returns a function from a name. If you want to add another option you have to alter the
        func_mapper in this function.
        :param name: is the name referred to a generator function.
        :return: a function to create a graph
        """
        func_mapper = {
            "complete":                     Graphs.create_complete,
            "barabasi_albert":              Graphs.create_barabasi_albert,
            "clustered_barabasi_albert":    Graphs.create_clustered_barabasi_albert,
            "watts_strogatz":               Graphs.create_watts_strogatz,
            "clustered_watts_strogatz":     Graphs.create_clustered_watts_strogatz,
            "powerlaw_cluster":             Graphs.create_powerlaw_cluster,
            "clustered_powerlaw_cluster":   Graphs.create_clustered_powerlaw_cluster

        }
        return func_mapper.get(name)


class Actors:

    def __init__(self):
        pass

    @staticmethod
    def create_nihilist(**kwargs):

        return Actor([0 for x in range(kwargs.get("n"))])

    @staticmethod
    def create_opportunist(**kwargs):

        return Actor([0 for x in range(kwargs.get("n"))])

    @staticmethod
    def create_random(**kwargs):

        return Actor([r.random() for x in range(r.choice(range(kwargs.get("n"))))])

    @staticmethod
    def func_by_name(name):
        """
        This function returns a function from a name. If you want to add another option you have to alter the
        func_mapper in this function.
        :param name: is the name referred to a generator function.
        :return: a function to create a actor
        """
        func_mapper = {
            "nihilist":     Actors.create_nihilist,
            "opportunist":  Actors.create_opportunist,
            "random":       Actors.create_random
        }
        return func_mapper.get(name)


class Distributions:

    def __init__(self):
        pass

    @staticmethod
    def create_random(**kwargs):
        randoms = [x for x in range(len(kwargs.get("graph").nodes))]

        return [randoms.pop(r.choice(randoms)) for x in randoms]

    @staticmethod
    def func_by_name(name):
        """
        This function returns a function from a name. If you want to add another option you have to alter the
        func_mapper in this function.
        :param name: is the name referred to a generator function.
        :return: a function to create a actor
        """
        func_mapper = {
            "nihilist":     Actors.create_nihilist,
            "opportunist":  Actors.create_opportunist,
            "random":       Actors.create_random
        }
        return func_mapper.get(name)