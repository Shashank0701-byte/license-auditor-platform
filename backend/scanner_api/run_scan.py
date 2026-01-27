from parser.requirements_parser import parse_requirements
from fetcher.pypi_client import PyPIClient
from graph.graph_builder import DependencyGraph
from rules.license_rule import LicenseRule
from rules.abandon_rule import AbandonRule
from analyzer.rule_engine import RuleEngine


def run_scan(requirements_file, max_depth=2):
    client = PyPIClient()
    graph = DependencyGraph()

    root_packages = parse_requirements(requirements_file)

    for name, version in root_packages:
        graph.build_recursive(name, client, depth=0, max_depth=max_depth)

    rules = [LicenseRule(), AbandonRule()]
    engine = RuleEngine(rules)
    engine.analyze(graph)

    results = []
    for node in graph.nodes.values():
        results.append({
            "name": node.name,
            "license": node.license,
            "last_updated": node.last_updated,
            "risks": node.risk_flags
        })

    return {
        "total_packages": len(graph.nodes),
        "packages": results
    }
