#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Connectivity test for oref.org.il (no MQTT, no notifications)."""
import json
import os
import threading

import urllib3
from loguru import logger

region = os.getenv('REGION', '*')
debug = os.getenv('DEBUG_MODE')
INCLUDE_TEST_ALERTS = os.getenv("INCLUDE_TEST_ALERTS")

http = urllib3.PoolManager()
_headers = {
    'Referer': 'https://www.oref.org.il/heb',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    'X-Requested-With': 'XMLHttpRequest',
}
url = 'https://www.oref.org.il/warningMessages/alert/Alerts.json'
if debug == 'True':
    url = 'http://localhost/alerts.json'

alerts = [0]


def is_test_alert(alert):
    return INCLUDE_TEST_ALERTS == 'False' and ('בדיקה' in alert['data'] or 'בדיקה מחזורית' in alert['data'])


def monitor():
    threading.Timer(1, monitor).start()
    r = None
    try:
        r = http.request('GET', url, headers=_headers, timeout=10.0)
        alert_data = r.data.decode('utf-8-sig').replace('\x00', '').strip()
        logger.info(f"HTTP {r.status}, {len(r.data)} bytes")
        if alert_data:
            alert = json.loads(alert_data)
            logger.info("Alert data successfully parsed.")
            if region in alert["data"] or region == "*":
                if alert["id"] not in alerts and not is_test_alert(alert):
                    alerts.append(alert["id"])
                    logger.info(str(alert))
        else:
            logger.info("No active alerts")
    except Exception as ex:
        logger.error(str(ex))
    finally:
        if r is not None:
            r.release_conn()


if __name__ == '__main__':
    logger.info("Monitoring alerts for: " + region)
    monitor()
