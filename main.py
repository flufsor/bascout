#!/usr/bin/env python3
import argparse
import os

from dotenv import load_dotenv

from bascout import Config, scanners

load_dotenv()
config = {
    "maxmind_id": os.getenv("MAXMIND_ID"),
    "maxmind_key": os.getenv("MAXMIND_KEY"),
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="Target to scan")
    args = parser.parse_args()

    modules = []
    #modules.append(("Nmap", scanners.Nmap))
    modules.append(("GeoIP", scanners.GeoIP))

    for module in modules:
        print(f"Running {module[0]} scan...")
        scanner = module[1](args.target)
        scanner.scan()

        print(scanner.result.simple)
        print()
        print(scanner.result)

