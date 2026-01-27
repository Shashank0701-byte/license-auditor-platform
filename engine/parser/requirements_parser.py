def parse_requirements(file_path):
    packages = []

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "==" in line:
                name, version = line.split("==")
            else:
                name = line
                version = "latest"

            packages.append((name.strip(), version.strip()))

    return packages
