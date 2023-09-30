import json

from .scanners.scan import Scan


class ScanEncoder(json.JSONEncoder):
    """
    JSON encoder for encoding Scan objects into JSON format.
    """
    def default(self, scan: Scan) -> dict:
        """
        Override the default method to handle encoding of Scan objects.
        """
        return {
            "target": scan.target,
            "start_time": scan.start_time.isoformat() if scan.start_time else None,
            "end_time": scan.end_time.isoformat() if scan.end_time else None,
            "result": scan.result.full,
            "results_simple": scan.result.simple
        }
