import telnetlib


class TelnetService():

    def __init__(self, host):
        self.host = host
        self.telnet = telnetlib.Telnet(self.host, 23)

    def login(self):
        print("Telnet Login")
        self.telnet.read_until(b"login: ")
        self.telnet.write(b"root\n")
        self.telnet.read_until(b"Password: ")
        self.telnet.write(b"dvix\n")
        print(self.telnet.read_all())

    def do_dvix_test_command(self, command):
        self.login()
        self.telnet.read_until(b"$")
        print("Telnet: Write dvix_test")
        self.telnet.write(b"dvix_test\n")
        print(self.telnet.read_all())
        self.telnet.read_until(b"test>")
        print(self.telnet.read_all())
        self.telnet.write(command)
        print(self.telnet.read_all())
        result = self.telnet.read_all()
        print(self.telnet.read_all())
        self.telnet.read_until(b"test>")
        self.telnet.write(b"q\n")
        self.telnet.read_until(b"$")
        self.telnet.write(b"exit\n")
        return result
