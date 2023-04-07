import logging
import subprocess

import pexpect
from colorama import Fore

import utility.checkcli as utility


class SSHCommand:
    def __init__(self, credentials):
        self.startcmd = "ssh -tt -o \"StrictHostKeyChecking no\" "
        self.credentials = credentials
        self.keyexcangemethod = ""
        self.hostkeytype = ""
        self.sshpass = f"sshpass -p {credentials[3]} "

    def generatecommand(self):
        return f"{self.sshpass}{self.startcmd}{self.keyexcangemethod}{self.hostkeytype}{self.credentials[2]}@{self.credentials[0]}"

    def addkeyexchangemethod(self, method):
        self.keyexcangemethod = f"-o KexAlgorithms={method} "

    def addhostkeytype(self, key):
        self.hostkeytype = f"-oHostKeyAlgorithms=+{key} "



class Checker:

    def __init__(self):
        self.credentials = []
        self.cmd = ""
        logging.info("Spinning up checker module...")

    def load_info(self, info):
        self.credentials = info

    def work(self):
        result = []

        for credential in self.credentials:
            logging.info(f"Start checking: {credential[0]}")
            try:
                cli = utility.CheckCli(credential)
                try:
                    credential = cli.start_connection()
                    return credential
                except pexpect.exceptions.TIMEOUT as err_timeout:
                    logging.info(f"Timeout for {credential[0]}")
                except BaseException as ex:
                    logging.critical(f"Something goes terrible error: {ex}")
                finally:
                    cli.end_connection()

            except subprocess.CalledProcessError:
                logging.debug(f"{Fore.YELLOW}No result for {credential[0]}. Reason: error.{Fore.RESET}")

        return result
