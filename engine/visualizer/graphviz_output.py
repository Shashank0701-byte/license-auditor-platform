import os
os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Graphviz\bin"
from graphviz import Digraph

def export_graph(graph, output_file="dependency_graph"):
    dot = Digraph(comment="Dependency Graph", format="png")

    for node in graph.nodes.values():
        color = "lightgreen"

        if node.is_risky_license:
            color = "red"
        elif node.is_abandoned:
            color = "orange"

        dot.node(node.name, node.name, style="filled", fillcolor=color)

        for dep in node.dependencies:
            dot.edge(node.name, dep.name)

    dot.render(output_file, cleanup=True)

