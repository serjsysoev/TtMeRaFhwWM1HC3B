from typing import NoReturn, TextIO, List, Iterable, TypeVar
import networkx

INPUT_FILE_NAME: str = "input.txt"

T = TypeVar('T')  # for generic types


def read_line_of_numbers(file: TextIO) -> List[int]:
    return [int(x) for x in file.readline().split()]


def parse_graph_from_file(filename: str) -> networkx.DiGraph:
    with open(filename, "r") as input_file:
        n, m = read_line_of_numbers(input_file)

        graph: networkx.DiGraph = networkx.empty_graph(n, networkx.DiGraph)
        for _ in range(m):
            from_vertex, to_vertex = read_line_of_numbers(input_file)
            graph.add_edge(to_vertex - 1, from_vertex - 1)  # inverting edges and making them 0-based

        input_file.readline()  # skipping S1 size
        graph.graph["s1_nodes"] = [x - 1 for x in read_line_of_numbers(input_file)]  # making nodes 0-based

        input_file.readline()  # skipping S2 size
        graph.graph["s2_nodes"] = [x - 1 for x in read_line_of_numbers(input_file)]  # making nodes 0-based

        return graph


def paths_length_from_set(graph: networkx.DiGraph, nodes_set: Iterable[int]) -> List[int]:
    graph_size = graph.number_of_nodes()
    graph.add_node("fake_root")
    for node in nodes_set:
        graph.add_edge("fake_root", node)

    result = [graph_size] * graph_size  # graph_size is infinity in terms of path length
    for from_node, to_node in networkx.algorithms.traversal.bfs_edges(graph, "fake_root"):
        result[to_node] = 0 if from_node == "fake_root" else result[from_node] + 1

    graph.remove_node("fake_root")
    return result


def flatten_list(input_list: List[List[T]]) -> List[T]:
    return [item for sublist in input_list for item in sublist]


def main() -> NoReturn:
    graph = parse_graph_from_file(INPUT_FILE_NAME)

    paths_length_from_s1 = paths_length_from_set(graph, graph.graph["s1_nodes"])
    paths_length_from_s2 = paths_length_from_set(graph, graph.graph["s2_nodes"])

    node_count = graph.number_of_nodes()
    count_sort_list = [[] for _ in range(2 * node_count)]
    for i in range(node_count):
        if paths_length_from_s1[i] == node_count or paths_length_from_s2[i] == node_count:
            # path length == infinity => no path
            continue
        path_length_sum = paths_length_from_s1[i] + paths_length_from_s2[i]
        count_sort_list[path_length_sum].append(i)

    for node in flatten_list(count_sort_list):
        print(node + 1)  # returning to 1-based


if __name__ == "__main__":
    main()
