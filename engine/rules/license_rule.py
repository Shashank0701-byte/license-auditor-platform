from rules.base_rule import BaseRule


class LicenseRule(BaseRule):
    RISKY_LICENSES = ["GPL", "AGPL"]

    def apply(self, node):
        if node.license and any(x in node.license.lower() for x in ["gpl", "agpl"]):
            node.is_risky_license = True

    def check(self, node):
        if node.license:
            for risky in self.RISKY_LICENSES:
                if risky in node.license.upper():
                    node.risk_flags.append("LICENSE_RISK")
