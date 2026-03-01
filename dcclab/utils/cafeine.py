import time
import socket
import subprocess
import atexit


class Cafeine:
    def __init__(self, username='dcclab'):
        self.username = username
        self.sshProcess = None
        self._localPort = None

    def startMySQLTunnel(self, ssh_host="cafeine2.crulrg.ulaval.ca",
                         remote_bind_address="127.0.0.1", remote_port=3306):
        self._localPort = self._find_free_port()
        self.sshProcess = subprocess.Popen(
            ["ssh", "-N", "-o", "BatchMode=yes",
             "-o", "StrictHostKeyChecking=accept-new",
             "-o", "ConnectTimeout=5",
             "-L", "{0}:{1}:{2}".format(self._localPort, remote_bind_address, remote_port),
             "{0}@{1}".format(self.username, ssh_host)],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        atexit.register(self.stopMySQLTunnel)

        for _ in range(20):
            try:
                s = socket.create_connection(("127.0.0.1", self._localPort), timeout=1)
                s.close()
                return self._localPort
            except (socket.timeout, socket.error, OSError):
                pass
            if self.sshProcess.poll() is not None:
                stderr = self.sshProcess.stderr.read().decode()
                raise RuntimeError("SSH tunnel failed: {0}".format(stderr))
            time.sleep(0.25)
        raise RuntimeError("SSH tunnel to {0} timed out".format(ssh_host))

    @staticmethod
    def _find_free_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', 0))
            return s.getsockname()[1]

    @property
    def localMySQLPort(self):
        return self._localPort

    def stopMySQLTunnel(self):
        if self.sshProcess is not None and self.sshProcess.poll() is None:
            self.sshProcess.terminate()
            self.sshProcess.wait(timeout=5)
        self.sshProcess = None
        self._localPort = None


if __name__ == "__main__":
    tunnel = Cafeine()
    tunnel.startMySQLTunnel()
    print("You can connect to mysql with `mysql -u dcclab -p -h 127.0.0.1 -P {0}`".format(tunnel.localMySQLPort))
    time.sleep(100000)
    tunnel.stopMySQLTunnel()
