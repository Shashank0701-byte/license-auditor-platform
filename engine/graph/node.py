class PackageNode:
    def __init__(self, name, version):
        self.name = name
        self.version = version
        
        # Metadata (filled after fetching from PyPI)
        self.license = None
        self.last_updated = None
        
        # Graph edges
        self.dependencies = []  # list of PackageNode objects
        
        # Analysis results
        self.risk_flags = []
        self.is_risky_license = False
        self.is_abandoned = False

    def __repr__(self):
        return f"PackageNode(name={self.name}, version={self.version})"
