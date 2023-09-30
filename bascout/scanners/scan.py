import datetime
import json
from collections import OrderedDict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, Protocol


class ScanStatus(Enum):
    """
    This class represents the status of a scan operation.
    """
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"

@dataclass
class ScanResult:
    """
    This class represents the result of a scan operation.
    """
    status: ScanStatus = ScanStatus.PENDING
    full: dict[str, Any] = field(default_factory=dict)
    simple: str = ""

class Scan(Protocol):
    """
    This abstract class represents a scan operation.
    """
    target: str
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    result: ScanResult

    def __init__(self, target: str) -> None:
        ...

    def scan(self) -> None:
        """
        Perform a scan operation on the specified target and capture the result.
        """
        ...

    def dict(self) -> dict:
        """
        Return a dictionary representation of the Scan object.
        """
        result_dict: OrderedDict[str, Any] = OrderedDict({"target": self.target})

        if self.start_time:
            result_dict["start_time"] = self.start_time.isoformat()

        if self.end_time:
            result_dict["end_time"] = self.end_time.isoformat()

        result_dict["result"] = self.result

        if self.result.simple:
            result_dict["results_simple"] = self.result.simple

        return result_dict

    def json(self) -> str:
        """
        Return a JSON representation of the Scan object.
        """
        def default(o):
            if type(o) is datetime.date or type(o) is datetime.datetime:
                return o.isoformat()

        return json.dumps(
            self.dict(),
            indent=4,
            default=default,
        )
