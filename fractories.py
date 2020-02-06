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

        return [r.choice([1.0, 0.0, -1.0]) for x in range(kwargs.get("n")) ]

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
        r.shuffle(randoms)

        return randoms

    @staticmethod
    def func_by_name(name):
        """
        This function returns a function from a name. If you want to add another option you have to alter the
        func_mapper in this function.
        :param name: is the name referred to a generator function.
        :return: a function to create a actor
        """
        func_mapper = {
            "random":       Distributions.create_random
        }
        return func_mapper.get(name)


class Rules:
    def __init__(self):
        pass

    # APPLY FUNCTIONS

    @staticmethod
    def create_actions_by_name(node, graph, conf):
        """

        """
        func_mapper = {
            "association":     Rules.gen_association,
            "disassociation":  Rules.gen_disassociation,
            "social_desirability": Rules.gen_social_desirability,
        }
        return func_mapper.get(conf.get("name"))(node=node, graph=graph, conf=conf)

    # PARAM FUNCTIONS

    @staticmethod
    def gen_association(node, graph, conf):
        result = []
        node_a = node
        actor_a = graph.nodes[node_a]["actor"]
        neighbors_a = set(graph.neighbors(node_a))

        for node_b in neighbors_a:
            actor_b = graph.nodes[node_b]["actor"]
            neighbors_b = set(graph.neighbors(node_b))
            possible_cs = (neighbors_b - neighbors_a) - set([node_a])

            if r.random() > actor_a.orientation(actor_b) and possible_cs:
                node_c_id = r.choice([x for x in possible_cs])
                result += [{"name": "add_edge",
                            "node_a_id": node_a,
                            "node_b_id": node_c_id}]

        return result

    @staticmethod
    def gen_disassociation(node, graph, conf):
        result = []
        node_a = node
        actor_a = graph.nodes[node_a]["actor"]

        for node_b in graph.neighbors(node_a):
            actor_b = graph.nodes[node_b]["actor"]
            if -(r.random()) > actor_a.orientation(actor_b) and graph.has_edge(actor_a, actor_b):
                result += [{"name": "remove_edge",
                            "node_a_id": node_a,
                            "node_b_id": node_b}]

        return result

    @staticmethod
    def gen_social_desirability(node, graph, conf):
        return [r.choice([1.0, 0.0, -1.0]) for x in range(r.choice(range(kwargs.get("n"))) + 1)]