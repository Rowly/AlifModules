import logging
import time
import requests
from requests.auth import HTTPDigestAuth
import os
from telnet_service import TelnetService


# GUARDS = ["10.10.10.101", "10.10.10.102", "10.10.10.10.3"]
GUARDS = ["10.10.10.104"]
TESTING = {"CopperSFP":["10.10.10.151", "10.10.10.152"],
           "mm2km":["10.10.10.151", "10.10.10.152"],
           "mm550m":["10.10.10.151", "10.10.10.152"],
           "sm10km":["10.10.10.151", "10.10.10.152"],
           "sm30km":["10.10.10.151", "10.10.10.152"]}

def logging_start():
    logging.basicConfig(filename="/var/log/alif-modules/result.log",
                        format="%(asctime)s:%(levelname)s:%(message)s",
                        level=logging.INFO)
    logging.info("ADDER: ==== Started Logging ====")


def logging_stop():
    logging.info("ADDER: ==== Stopped Logging ====")
    time.sleep(1)
    logging.shutdown()


def send_power_on(ip):
    logging.info("ADDER: Power On {}".format(ip))
    r = requests.get("http://{}/hidden.htm?M0:O1=On".format(ip), auth=HTTPDigestAuth("api", "api"))
    assert(r.status_code == 200)


def send_power_off(ip):
    logging.info("ADDER: Power Off {}".format(ip))
    r = requests.get("http://{}/hidden.htm?M0:O1=Off".format(ip), auth=HTTPDigestAuth("api", "api"))
    assert(r.status_code == 200)


def send_power_restart(ip):
    logging.info("ADDER: Power Restart {}".format(ip))
    r = requests.get("http://{}/hidden.htm?M0:O1=Restart".format(ip), auth=HTTPDigestAuth("api", "api"))
    assert(r.status_code == 200)


def telnet_to_alif(ip):
    telnet = TelnetService(ip)
    return telnet.do_dvix_test_command(b"fibre")
    
    
if __name__ == "__main__":
    executions = 0
    passes = 0
    fails = 0
    logging_start()
    for guard in GUARDS:
        send_power_on(guard)
    while True:
        logging.info("ADDER: Execution {}".format(executions += 1)
        for guard in GUARDS:
            send_power_restart(guard)
        time.sleep(180)
        for (k,v) in TESTING:
            logging.info("ADDER: Module {}".format(k))
            result_a = telnet_to_alif(v[0])
            result_b - telnet_to_alif(v[1])
            
            
        
        

