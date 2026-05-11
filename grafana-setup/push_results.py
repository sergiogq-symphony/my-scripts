import xml.etree.ElementTree as ET
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import sys

# InfluxDB Configuration
TOKEN = "my-super-secret-auth-token"
ORG = "my-org"
BUCKET = "automation_results"
URL = "http://localhost:8086"

def parse_and_push(xml_file):
    if not os.path.exists(xml_file):
        print(f"Error: File {xml_file} not found.")
        return

    client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    tree = ET.parse(xml_file)
    root = tree.getroot()

    # If the root is 'testsuite', it might have multiple 'testcase' children
    # If it's 'testsuites', we iterate through suites
    suites = [root] if root.tag == 'testsuite' else root.findall('testsuite')

    for suite in suites:
        suite_name = suite.get('name', 'unknown_suite')
        
        for testcase in suite.findall('testcase'):
            name = testcase.get('name')
            classname = testcase.get('classname')
            duration = float(testcase.get('time', 0))
            
            # Determine status
            status = "passed"
            if testcase.find('failure') is not None:
                status = "failed"
            elif testcase.find('error') is not None:
                status = "error"
            elif testcase.find('skipped') is not None:
                status = "skipped"

            point = Point("test_result") \
                .tag("suite", suite_name) \
                .tag("test_name", name) \
                .tag("classname", classname) \
                .tag("status", status) \
                .field("duration", duration) \
                .field("count", 1)

            write_api.write(BUCKET, ORG, point)
            print(f"Pushed: {name} - {status} ({duration}s)")

    client.close()
    print("All results pushed successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python push_results.py <path_to_xml>")
    else:
        parse_and_push(sys.argv[1])
