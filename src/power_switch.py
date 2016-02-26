import logging
import time
import requests
from requests.auth import HTTPDigestAuth
import os
from telnet_service import TelnetService


# GUARDS = ["10.10.10.101", "10.10.10.102", "10.10.10.10.3"]
GUARDS = ["10.10.10.104"]
TESTING = {"CopperSFP": ["10.10.10.151", "10.10.10.152"],
           "mm2km": ["10.10.10.151", "10.10.10.152"],
           "mm550m": ["10.10.10.151", "10.10.10.152"],
           "sm10km": ["10.10.10.151", "10.10.10.152"],
           "sm30km": ["10.10.10.151", "10.10.10.152"]}

def logging_start():
    logging.basicConfig(filename="result.log",
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


def telnet_to_alif_fibre_command(ip, command):
    telnet = TelnetService(ip)
    telnet.do_dvix_test_command(b"fibre phy 1")
    return telnet.do_dvix_test_command(b"fibre phy 1")
    

def telnet_to_alif_net_command(ip, command):
    telnet = TelnetService(ip)
    return telnet.do_dvix_test_command(b"net 8")


if __name__ == "__main__":
    executions = 0
    passes = 0
    fails = 0
    logging_start()
    for guard in GUARDS:
        send_power_on(guard)
    while True:
        executions =+ 1
        logging.info("ADDER: Execution {}".format(executions))
        for guard in GUARDS:
            send_power_restart(guard)
        time.sleep(300)
        for (k,v) in TESTING:
            logging.info("ADDER: Module {}".format(k))
            fibre_result_a = telnet_to_alif_fibre_command(v[0])
            net_result_a = telnet_to_alif_net_command(v[0])
            fibre_result_b = telnet_to_alif_fibre_command(v[1])
            net_result_b = telnet_to_alif_net_command(v[1])
            fibre_a_flag = "Link UP" in fibre_result_a
            fibre_b_flag = "Link UP" in fibre_result_b
            net_a_flag = "SYNC OK; AN OK;" in net_result_a
            net_b_flag = "SYNC OK; AN OK;" in net_result_b
            logging.info("ADDER: Fibre - {} {} Net - {} {}".format(fibre_a_flag, fibre_b_flag, net_a_flag, net_b_flag))
            if fibre_a_flag and fibre_b_flag and net_a_flag and net_b_flag:
                passes =+ 1
            else:
                fails =+ 1
            logging.info("ADDER: Passes {} Fails {}".format(passes, fails))

            
            
            
        
        

