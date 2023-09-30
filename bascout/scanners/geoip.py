import os
from datetime import datetime

import geoip2.webservice
from dotenv import load_dotenv

from ..config import Config
from .scan import Scan, ScanResult, ScanStatus


class GeoIP(Scan):
    """
    This class represents a GeoIP scan operation.
    """
    def __init__(self, target) -> None:
        self.target = target
        self.result = ScanResult()

    def scan(self) -> None:
        conf = Config()
        self.start_time = datetime.now()

        load_dotenv()

        if conf.maxmind_id == "" or conf.maxmind_key == "":
            self.result.status = ScanStatus.FAILED
            self.result.full = {}
            self.result.simple = "MaxMind license key not set"
            return

        with geoip2.webservice.Client(int(conf.maxmind_id), conf.maxmind_key) as client:
            response = client.city(self.target)
            if response.city.name is None and response.country.name is None:
                self.result.status  = ScanStatus.FAILED
                self.result.full = {}
                self.result.simple = "Lookup failed"
            else:
                self.result.status  = ScanStatus.COMPLETED
                self.result.full = {
                    "city": response.city.name,
                    "country": response.country.name,
                    "continent": response.continent.name,
                    "latitude": response.location.latitude,
                    "longitude": response.location.longitude,
                    "postal": response.postal.code,
                }
                self.result.simple = f"{self.result.full['city']}, {self.result.full['country']}"
       
        self.end_time = datetime.now()
