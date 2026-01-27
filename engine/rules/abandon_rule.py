from datetime import datetime
from rules.base_rule import BaseRule


class AbandonRule(BaseRule):
    YEARS_THRESHOLD = 2

    def apply(self, node):
        if node.last_updated:
            if datetime.now() - node.last_updated > timedelta(days=730):
                node.is_abandoned = True

    def check(self, node):
        if node.last_updated:
            try:
                updated_date = datetime.strptime(node.last_updated, "%Y-%m-%dT%H:%M:%S")
                years_old = (datetime.utcnow() - updated_date).days / 365

                if years_old > self.YEARS_THRESHOLD:
                    node.risk_flags.append("ABANDONED_PACKAGE")
            except:
                pass
