def generate_report(graph, output_file="dependency_report.txt"):
    total = len(graph.nodes)
    license_risks = []
    abandoned_nodes = []

    for node in graph.nodes.values():
        if "LICENSE_RISK" in node.risk_flags:
            license_risks.append(node.name)
        if "ABANDONED_PACKAGE" in node.risk_flags:
            abandoned_nodes.append(node)

    # Remove duplicates (case-insensitive)
    license_risks = sorted(set(pkg.lower() for pkg in license_risks))
    abandoned_nodes = {node.name.lower(): node for node in abandoned_nodes}.values()

    report_lines = []
    report_lines.append("Dependency Scan Summary")
    report_lines.append("-----------------------")
    report_lines.append(f"Total packages scanned: {total}")
    report_lines.append(f"Risky licenses found: {len(license_risks)}")
    report_lines.append(f"Abandoned packages: {len(list(abandoned_nodes))}\n")

    report_lines.append("Severity Overview")
    report_lines.append("-----------------")
    report_lines.append(f"HIGH: {len(license_risks)} license compliance risks")
    report_lines.append(f"MEDIUM: {len(list(abandoned_nodes))} potentially abandoned packages\n")

    if license_risks:
        report_lines.append("⚠ License Risks:")
        for pkg in license_risks:
            report_lines.append(f" - {pkg}")
        report_lines.append("")

    if abandoned_nodes:
        report_lines.append("⚠ Abandoned Packages:")
        for node in abandoned_nodes:
            report_lines.append(f" - {node.name} (last updated: {node.last_updated})")
        report_lines.append("")

    report_text = "\n".join(report_lines)

    # Print to terminal
    print("\n" + report_text)

    # Save to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report_text)
