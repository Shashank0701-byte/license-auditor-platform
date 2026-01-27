import requests
import re


class PyPIClient:
    BASE_URL = "https://pypi.org/pypi"

    def fetch_package_metadata(self, package_name):
        url = f"{self.BASE_URL}/{package_name}/json"
        response = requests.get(url)

        if response.status_code != 200:
            return None

        data = response.json()
        info = data.get("info", {})

        license_type = info.get("license")
        latest_version = info.get("version")

        # Last updated date
        releases = data.get("releases", {})
        release_files = releases.get(latest_version, [])
        upload_time = release_files[0]["upload_time"] if release_files else None

        # Dependencies list
        dependencies = info.get("requires_dist") or []

        parsed_deps = []
        for dep in dependencies:
            dep = dep.split(";")[0].strip()  # remove environment markers
            dep = dep.split("(")[0].strip()  # remove parentheses version info
    
            # Remove version constraints like >=, <=, == etc.
            dep_name = re.split(r"[<>=!~]", dep)[0].strip()

            if dep_name:
                parsed_deps.append(dep_name)
        return {
            "license": license_type,
            "last_updated": upload_time,
            "dependencies": parsed_deps
        }
