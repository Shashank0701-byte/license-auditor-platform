import json

def generate_json_report(graph, output_file="dependency_report.json"):
    data = {
        "total_packages": len(graph.nodes),
        "packages": []
    }

    for node in graph.nodes.values():
        data["packages"].append({
            "name": node.name,
            "license": node.license,
            "last_updated": node.last_updated,
            "risks": node.risk_flags
        })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"\nJSON report saved to {output_file}")
