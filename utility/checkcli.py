import logging
import subprocess
import pexpect

class SSHCommand:
    def __init__(self, credentials):
        self.startcmd = "ssh -tt -o \"StrictHostKeyChecking no\" "
        self.credentials = credentials
        self.keyexcangemethod = ""
        self.hostkeytype = ""
        #self.sshpass = f"sshpass -p {credentials[3]} "

    def generate_command(self):
        return f"{self.startcmd}{self.keyexcangemethod}{self.hostkeytype}{self.credentials[2]}@{self.credentials[0]}"

    def add_key_exchange_method(self, method):
        self.keyexcangemethod = f"-o KexAlgorithms={method} "

    def add_host_key_type(self, key):
        self.hostkeytype = f"-oHostKeyAlgorithms=+{key} "


class CheckCli:
    def __init__(self, credential):
        self.ssh = None
        self.ssh_class = SSHCommand(credential)
        self.ip = credential[0]
        self.login = credential[2]
        self.password = credential[3]
        self.is_rerun_needed = True
        self.is_succes = False
        self.credential = credential

    def start_connection(self):
        while self.is_rerun_needed:
            self.ssh = pexpect.spawn(self.ssh_class.generate_command(), timeout=10, encoding='utf-8')
            self.is_rerun_needed = False
            case = self.ssh.expect(["Their offer: ", "no matching host key type found", "Connection refused", "Please login:", "[Pp]assword", "closed"])
            if case == 0:
                answers = str(self.ssh.buffer).split(" ")
                for ans in answers:
                    words = ans.split(",")
                    clrcmd = words[0].replace('\r', '')
                    clrcmd = clrcmd.replace('\n', '')
                    self.is_rerun_needed = True
                    self.ssh_class.add_key_exchange_method(clrcmd)
            elif case == 1:
                answers = str(self.ssh.buffer).split(" ")
                for ans in answers:
                    words = ans.split(",")
                    clrcmd = words[0].replace('\r', '')
                    clrcmd = clrcmd.replace('\n', '')
                    self.is_rerun_needed = True
                    self.ssh_class.add_host_key_type(clrcmd)
            elif case == 2 or case == 5:
                logging.info(f"{self.ip} connection refused")
            else:
                if case == 3:
                    self.ssh.sendline(self.login)
                    self.ssh.expect("[Pp]assword")
                self.ssh.sendline(self.password)
                cases = ["[#\$] ", "Login incorrect", "Access denied", "Authentication failed", "User name or password is wrong", "closed"]
                login_case = self.ssh.expect(cases)
                if login_case != 0:
                    logging.info(f"False positive {self.ip}, case \"{cases[login_case]}\"")
                else:
                    #print(str(self.ssh))
                    with open("./data/result.txt", 'a') as out:
                        out.write(f"{self.ssh_class.generate_command()} and password:{self.password}\n")
                    return self.credential
            self.end_connection()
        if self.is_succes:
            print(self.ssh_class.generate_command())

    def end_connection(self):
        self.ssh.kill(0)

        '''
    def check_results(self):
        while self.is_rerun_needed:
            self.current_command = self.ssh.generate_command()
            self.cli.stdin.write(self.current_command.encode())
            #self.full_flush()
            #self.cli.stdin.flush()
            self.cli.stdin.close()
            print(self.cli.stdout.read())
            #print(self.cli.stdin.read())
            stdout, stderr = self.cli.communicate()
            print(self.current_command)
            self.is_rerun_needed = False
            if stdout:
                print("var1")
                return stdout
            else:
                answer = stderr.decode("utf-8")
                if answer.__contains__("no matching key exchange method found"):
                    answers = answer.split(" ")
                    for ans in answers:
                        if ans.__contains__("diffie"):
                            clrcmd = self.trim_answer(ans)
                            self.ssh.add_key_exchange_method(clrcmd)
                if answer.__contains__("no matching host key type found"):
                    answers = answer.split(" ")
                    for ans in answers:
                        if ans.__contains__("ssh"):
                            clrcmd = self.trim_answer(ans)
                            self.ssh.add_host_key_type(clrcmd)
        return stderr

    async def work(self):
        result.txt = []

        for credential in self.credentials:
            try:
                logging.info(f"Started checking: {credential[0]}")
                ssh = SSHCommand(credential)
                logging.info(ssh.generatecommand())
                isrerunneeded = True
                while isrerunneeded:
                    isrerunneeded = False
                    with subprocess.Popen(ssh.generatecommand(), shell=True, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE) as proc:
                        stdout, stderr = proc.communicate()
                        logging.debug(ssh.generatecommand())
                        logging.info(stderr)
                        if stdout:
                            logging.info(ssh.generatecommand())
                        logging.info(f"check {stdout}")
                        answer = stderr.decode("utf-8")
                        if answer.__contains__("no matching key exchange method found"):
                            answers = answer.split(" ")
                            for ans in answers:
                                if ans.__contains__("diffie"):
                                    words = ans.split(",")
                                    clrcmd = words[0].replace('\r', '')
                                    clrcmd = clrcmd.replace('\n', '')
                                    logging.debug(clrcmd)
                                    ssh.addkeyexchangemethod(clrcmd)
                                    isrerunneeded = True
                        if answer.__contains__("no matching host key type found"):
                            answers = answer.split(" ")
                            for ans in answers:
                                if ans.__contains__("ssh"):
                                    words = ans.split(",")
                                    clrcmd = words[0].replace('\r', '')
                                    clrcmd = clrcmd.replace('\n', '')
                                    logging.debug(clrcmd)
                                    ssh.addhostkeytype(clrcmd)
                                    isrerunneeded = True
                    if isrerunneeded:
                        time.sleep(10)

            except subprocess.CalledProcessError:
                logging.debug(f"{Fore.YELLOW}No result.txt for {credential[0]}. Reason: error.{Fore.RESET}")

        return result.txt
        '''
