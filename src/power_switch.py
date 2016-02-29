import logging
import time
import requests
from requests.auth import HTTPDigestAuth
import os
from telnet_service import TelnetService


GUARDS = ["10.10.10.101", "10.10.10.102", "10.10.10.103", "10.10.10.104", "10.10.10.105"]
TESTING = {"CopperSFP 10/100/1000 RJ45 SGMI": ["10.10.10.151", "10.10.10.152"],
           "MultiMode 1310 LC 2km": ["10.10.10.151", "10.10.10.152"],
           "MultiMode 850 LC 550m": ["10.10.10.151", "10.10.10.152"]
           "SingleMode 1310 LC 10km": ["10.10.10.151", "10.10.10.152"],
           " SingleMode 1310 LC 30km": ["10.10.10.151", "10.10.10.152"]
           }

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


def telnet_to_alif_fibre_command(ip):
    telnet = TelnetService(ip)
    return telnet.do_dvix_test_command(b"fibre phy 1")
    

def telnet_to_alif_net_command(ip):
    telnet = TelnetService(ip)
    return telnet.do_dvix_test_command(b"net 8")


if __name__ == "__main__":
    executions = 0
    logging_start()
    """
    For each 1Guard ensure they are powered on
    """
    for guard in GUARDS:
        send_power_on(guard)
    while True:
        results = []
        try:
            executions += 1
            logging.info("ADDER: =====Execution {}=====".format(executions))
            """
            For each 1Guard start a restart cycle
            """
            for guard in GUARDS:
                send_power_restart(guard)
            """
            Wait 3 minutes to ensure ALIFs have rebooted
            """
            time.sleep(180)
            """
            For each module telnet into the corresponding devices and
            return the value from 'net 8'
            """
            for key, value in TESTING.items():
                logging.info("ADDER: Module {}".format(key))
                logging.info("ADDER: Devices {} & {}".format(value[0], value[1]))
                """
                In the case of the CopperSFP module also telnet to get the result
                of 'fibre phy 1'
                """
                if key == "CopperSFP":
                    fibre_result_a = telnet_to_alif_fibre_command(value[0])
                    fibre_result_b = telnet_to_alif_fibre_command(value[1])
                    fibre_a_flag = "Link UP" in fibre_result_a
                    fibre_b_flag = "Link UP" in fibre_result_b
                else:
                    net_result_a = telnet_to_alif_net_command(value[0])
                    net_result_b = telnet_to_alif_net_command(value[1])
                 
                net_a_flag = "SYNC OK; AN OK;" in net_result_a
                net_b_flag = "SYNC OK; AN OK;" in net_result_b
                
                """
                Form the results line for logging and append it to the list of results
                """
                if key == "CopperSFP":
                    results.append("{} 'fibre phy 1' check {} {}\n" +
                                   "{} 'net 8' check {} {}".format(key, fibre_a_flag, fibre_b_flag,
                                                                   key, net_a_flag, net_b_flag))
                else:
                    results.append("{} 'net 8' check {} {}".format(key, net_a_flag, net_b_flag))
            
            """
            Log each result in turn
            """
            for result in results:
                logging.info("ADDER: {}".format(result))
                
        except KeyboardInterrupt:
            logging_stop()
            break


            
            
            
        
        

