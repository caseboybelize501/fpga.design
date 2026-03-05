import xml.etree.ElementTree as ET
from typing import Dict, List

async def parse_timing_report(report_path: str) -> Dict:
    # Parse timing report from Vivado or Quartus
    try:
        if report_path.endswith('.xml'):
            return parse_xml_timing_report(report_path)
        else:
            return parse_text_timing_report(report_path)
    except Exception as e:
        return {
            "wns": 0.0,
            "whs": 0.0,
            "critical_path": "unknown",
            "error": str(e)
        }

async def parse_xml_timing_report(report_path: str) -> Dict:
    # Parse Vivado XML timing report
    try:
        tree = ET.parse(report_path)
        root = tree.getroot()
        
        wns = 0.0
        whs = 0.0
        critical_path = "unknown"
        
        # Extract timing data from XML
        for elem in root.iter():
            if 'WNS' in elem.tag:
                wns = float(elem.text)
            elif 'WHS' in elem.tag:
                whs = float(elem.text)
            elif 'critical_path' in elem.tag:
                critical_path = elem.text
        
        return {
            "wns": wns,
            "whs": whs,
            "critical_path": critical_path
        }
    except Exception as e:
        return {
            "wns": 0.0,
            "whs": 0.0,
            "critical_path": "unknown",
            "error": str(e)
        }

async def parse_text_timing_report(report_path: str) -> Dict:
    # Parse text-based timing report
    try:
        with open(report_path, 'r') as f:
            content = f.read()
            
        wns = 0.0
        whs = 0.0
        critical_path = "unknown"
        
        lines = content.split('\n')
        for line in lines:
            if 'WNS' in line and 'ns' in line:
                wns = float(line.split()[1])
            elif 'WHS' in line and 'ns' in line:
                whs = float(line.split()[1])
            elif 'Critical path' in line:
                critical_path = line
        
        return {
            "wns": wns,
            "whs": whs,
            "critical_path": critical_path
        }
    except Exception as e:
        return {
            "wns": 0.0,
            "whs": 0.0,
            "critical_path": "unknown",
            "error": str(e)
        }