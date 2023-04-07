import logging
import subprocess


class Scan:

    def __init__(self):
        self.targets = "500"
        self.cmd = f"nmap -oG - -Pn -T4 --open -p 22 -iR {str(self.targets)}"

        logging.info("Spinning up scan module...")
        logging.debug(f"Loading command: {self.cmd}")
    
    def work(self):
        result = []
        returned_output = subprocess.check_output(self.cmd, shell=True)
        answer = returned_output.decode("utf-8")
        answer = answer.split("\n")

        for string in answer:
            if string.__contains__("Ports"):
                words = string.split(" ")
                ip = words[1]
                port = words[3][0] + words[3][1]
                result.append((ip, port))
        return result
