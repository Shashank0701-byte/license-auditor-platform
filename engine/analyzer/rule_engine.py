class RuleEngine:
    def __init__(self, rules):
        self.rules = rules

    def analyze(self, graph):
        for node in graph.nodes.values():
            for rule in self.rules:
                rule.check(node)
