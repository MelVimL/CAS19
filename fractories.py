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
        return nx.generators.connected_watts_strogatz_graph(n=kwargs.get("n"), k=kwargs.get("k"))

    @staticmethod
    def create_clustered_watts_strogatz(**kwargs):
        return nx.generators.barabasi_albert_graph(kwargs.get("n"), seed=None)

    @staticmethod
    def create_clustered_powerlaw_cluster(**kwargs):
        return nx.powerlaw_cluster_graph()

    @staticmethod
    def create_powerlaw_cluster(**kwargs):
        return nx.powerlaw_cluster_graph(n=kwargs.get("n"), m=kwargs.get("m"))

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
    def create_gradually(**kwargs):
        randoms = [x for x in range(len(kwargs.get("graph").nodes))]
        r.shuffle(randoms)

        return randoms

    @staticmethod
    def create_contradicting(**kwargs):
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
            "random":       Distributions.create_random,
            "gradual":      Distributions.create_gradually,
            "contradicting": Distributions.create_contradicting
        }
        return func_mapper.get(name)


class Rules:
    def __init__(self):
        pass

    # APPLY FUNCTIONS

    @staticmethod
    def create_actions_by_name(edge, graph, conf):
        """

        """
        func_mapper = {
            "association":     Rules.gen_association,
            "disassociation":  Rules.gen_disassociation,
            "dynamic_ad":      Rules.gen_dynamic_ad,
            "social_desirability": Rules.gen_social_desirability,
        }
        return func_mapper.get(conf.get("name"))(edge=edge, graph=graph, conf=conf)

    # PARAM FUNCTIONS

    @staticmethod
    def gen_dynamic_ad(edge, graph, conf):
        node_a = edge[0]
        node_b = edge[1]
        actor_a = graph.nodes[node_a]["actor"]
        actor_b = graph.nodes[node_b]["actor"]
        za = actor_a.orientation_of_action(actor_b)
        zb = actor_b.orientation_of_action(actor_a)
        zv = r.random() * (za + zb)

        node_x, node_y = (node_a, node_b) if zv < za else (node_b, node_a)
        actor_x = graph.nodes[node_x]["actor"]
        actor_y = graph.nodes[node_y]["actor"]
        neighbors_y = list(graph.neighbors(node_y))
        node_z = r.choice(neighbors_y)

        z = r.random()
        if z < actor_x.orientation_of_action(actor_y):
            return [{"name": "add_edge",
                     "node_x": node_x,
                     "node_z": node_z}]
        else:
            return [{"name": "remove_edge",
                     "node_x": node_x,
                     "node_z": node_z}]

    @staticmethod
    def gen_association(edge, graph, conf):
        node_a = edge[0]
        node_b = edge[1]
        actor_a = graph.nodes[node_a]["actor"]
        actor_b = graph.nodes[node_b]["actor"]
        if r.random() < actor_a.orientation(actor_b):
            return []
        za = actor_a.orientation_of_action(actor_b)
        zb = actor_b.orientation_of_action(actor_a)
        zv = r.random() * (za + zb)

        if zv <= za:
            node_x = node_a
            node_y = node_b
        else:
            node_x = node_b
            node_y = node_a

        neighbors_y = list(graph.neighbors(node_y))
        node_z = r.choice(neighbors_y)

        return [{"name": "add_edge",
                 "node_x": node_x,
                 "node_z": node_z}]

    @staticmethod
    def gen_disassociation(edge, graph, conf):
        node_a = edge[0]
        node_b = edge[1]
        actor_a = graph.nodes[node_a]["actor"]
        actor_b = graph.nodes[node_b]["actor"]
        if r.random() > actor_a.orientation(actor_b):
            return []
        za = actor_a.orientation_of_action(actor_b)
        zb = actor_b.orientation_of_action(actor_a)
        zv = r.random() * (za + zb)

        node_x, node_y = (node_b, node_a) if zv > za else (node_a, node_b)

        neighbors_y = list(graph.neighbors(node_y))
        node_z = r.choice(neighbors_y)

        return [{"name": "remove_edge",
                 "node_x": node_x,
                 "node_z": node_z}]

    @staticmethod
    def gen_social_desirability(edge, graph, conf):
        node_a = edge[0]
        actor_a = graph.nodes[node_a]["actor"]
        if not actor_a.obeys_social_pressure():
            norm = [r.choice(1,0,-1) for x in range(len(actor_a.interessts()))]
            for node in graph.nodes:
                d = conf["options"]["d"]
                p = conf["options"]["d"]
                graph.nodes[node]["actor"].set_social_desirability(p=p, d=d, norm=norm)

        return []