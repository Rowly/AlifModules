import telnetlib


class TelnetService():

    def __init__(self, host):
        self.host = host
        self.telnet = telnetlib.Telnet()
        
    def login(self):
        self.telnet.open(self.host, 23, 5)
        self.telnet.read_until(b"login: ", 10)
        self.telnet.write(b"root\n")
        self.telnet.read_until(b"Password: ", 10)
        self.telnet.write(b"dvix\n")

    def do_dvix_test_command(self, command):
        self.login()
        self.telnet.read_until(b"$")
        
        if command != b"fibre phy 1":
            self.telnet.write(b"dvix_test " + command + b"; exit\n")
        else:
            self.telnet.write(b"dvix_test " + command + b";" +
                              b"dvix_test " + command + b";" +
                              b"exit\n")
        return str(self.telnet.read_all())
