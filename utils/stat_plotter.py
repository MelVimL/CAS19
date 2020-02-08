import yaml
import os
import matplotlib.pyplot as plt

STAT_PATH = "../stats/"


def gather_all_stats():
    result = {}
    dirs = os.listdir(STAT_PATH)

    for generation in dirs:
        cur_path = "{}{}".format(STAT_PATH, generation)

        for sim_file in os.listdir(cur_path):
            sim_name, __, __ = sim_file.partition(".")
            sim_path = "{}/{}".format(cur_path, sim_file)
            result.setdefault(sim_name, {}).update({})
            result[sim_name][generation] = {}
            with open(sim_path, "r") as f:
                file_dict = yaml.load(stream=f, Loader=yaml.FullLoader)
                for sub_gen in file_dict:
                    for stat_key in file_dict[sub_gen]:
                        result[sim_name][generation].setdefault(stat_key, []).append(file_dict[sub_gen][stat_key])
    return result

def main():
    stats = gather_all_stats()
    for sim in stats:
        for generation in stats[sim]:
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.set_title(sim)
            x1 = stats[sim][generation]["average_orientation"]
            x2 = stats[sim][generation]["graph_density"]
            x3 = stats[sim][generation]["graph_transitivity"]

            ax.set_ylabel("Percents")
            ax.set_xlabel("Generations")
            ax.grid(True)
            ax.plot(x1, label="average orientation")
            ax.plot(x2, label="graph_density")
            ax.plot(x3, label="graph_transitivity")

            plt.legend()
            plt.show()








if __name__ == "__main__":
    main()