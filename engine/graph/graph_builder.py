from graph.node import PackageNode


class DependencyGraph:
    def __init__(self):
        self.nodes = {}

    def get_or_create_node(self, name, version="latest"):
        if name in self.nodes:
            return self.nodes[name]

        node = PackageNode(name, version)
        self.nodes[name] = node
        return node

    def add_dependency(self, parent_node, child_node):
        if child_node not in parent_node.dependencies:
            parent_node.dependencies.append(child_node)

    def build_recursive(self, package_name, client, visited=None, depth=0, max_depth=2):

        if visited is None:
            visited = set()
        print(f"Fetching: {package_name} (depth={depth})")

        if depth > max_depth:
            return


        if package_name in visited:
            return

        visited.add(package_name)

        node = self.get_or_create_node(package_name)
        metadata = client.fetch_package_metadata(package_name)

        if not metadata:
            return

        node.license = metadata["license"]
        node.last_updated = metadata["last_updated"]

        for dep_name in metadata["dependencies"]:
            child_node = self.get_or_create_node(dep_name)
            self.add_dependency(node, child_node)

            # Recursive call
            self.build_recursive(dep_name, client, visited, depth + 1, max_depth)

