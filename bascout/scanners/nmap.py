import ipaddress
from datetime import datetime

import nmap

from .scan import Scan, ScanResult, ScanStatus


class Nmap(Scan):
   """
   This class represents a nmap scan operation.
   """
   def __init__(self, target: str) -> None:
       self.target = target
       self.result = ScanResult()

   def scan(self):
        self.start_time = datetime.now()

        nm = nmap.PortScanner()
        arguments="-sV -sC"
        ports = "80,443"

        try:
            target_ip = ipaddress.ip_address(self.target)
            if target_ip.version == 6:
                arguments = f"-6 {arguments}"
        except ValueError:
            pass
        
        scan_results = nm.scan(hosts=self.target, ports=ports, arguments=arguments)

        if not scan_results:
            self.result.status = ScanStatus.FAILED
            self.result.full = {}
            self.result.simple = "Scan failed"
            return

        self.result.status = ScanStatus.COMPLETED

        self.result.full = {
            "command_line": scan_results["nmap"]["command_line"],
            "scanstats": scan_results["nmap"]["scanstats"],
            "scan": {},
        }

        open_ports_set: set[str] = set()
        for host in scan_results["scan"]:
            nmscan = {
                "hostnames": scan_results["scan"][host]["hostnames"],
                "status": scan_results["scan"][host]["status"]["state"],
                "open_ports": {}
            }
            for proto in nm[host].all_protocols():
                lport = nm[host][proto].keys()
                for port in lport:
                    nmscan["open_ports"][port] = {
                        "state": nm[host][proto][port]["state"],
                        "name": nm[host][proto][port]["name"],
                        "product": nm[host][proto][port]["product"],
                        "version": nm[host][proto][port]["version"],
                        "extrainfo": nm[host][proto][port]["extrainfo"],
                        "reason": nm[host][proto][port]["reason"],
                        "conf": nm[host][proto][port]["conf"],
                        "cpe": nm[host][proto][port]["cpe"],
                    }
                    open_ports_set.add(str(port))

            self.result.full["scan"][host] = nmscan

        self.result.simple = f"Open ports: {', '.join(sorted(open_ports_set))}"
        self.end_time = datetime.now()
