import random
import string


class Mutator:

    def __init__(self, path_to_file, path_to_filefreq):
        self.path_to_file = path_to_file
        self.path_to_filefreq = path_to_filefreq
        self.info = {}

    def set_zero_freq(self):
        with open(self.path_to_file, 'r') as infile, open(self.path_to_filefreq, 'w') as outfile:
            for line in infile:
                outfile.write("1\n")

    def update(self, data):
        data += "\n"
        self.__update_info()
        self.info[data] = str(int(self.info[data].strip()) + 1) + "\n"
        self.__sort()

    def mutate(self):
        self.__update_info()
        variants = [self.__add_new_data, self.__remove_unused_data, self.__remove_unused_data, self.__remove_unused_data, self.__mutate_data]
        for i in range(10):
            variants.append(self.__skip)
        choice = random.choice(variants)
        choice()
        self.__sort()
        self.__update_info()

    def __skip(self):
        pass

    def __mutate_data(self):
        key = random.choice(list(self.info))
        new_key = key.strip()
        variants = []
        new_var1 = new_key
        for rand in range(random.randint(1, 10)):
            new_var1 += random.SystemRandom().choice(string.ascii_letters + string.digits)
        new_var1 += "\n"
        variants.append(new_var1)
        if len(new_key) > 1:
            random_val = random.randint(1, (len(new_key) - 1))
            variants.append(new_key[0:-random_val] + "\n")
        self.info[random.choice(variants)] = "0\n"

    def __remove_unused_data(self):
        zero_efficient = [name for name, freq in self.info.items() if freq == "0\n"]
        if len(zero_efficient) > 1:
            key = random.choice(zero_efficient)
            value = self.info.pop(key)

    def __add_new_data(self):
        output_string = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
        output_string += "\n"
        self.info[output_string] = "0\n"

    def __update_info(self):
        self.info = {}
        with open(self.path_to_file, 'r') as infile, open(self.path_to_filefreq, 'r') as freq:
            for line in infile:
                freq_for_line = freq.readline()
                self.info[line] = freq_for_line

    def __sort(self):
        self.info = dict(sorted(self.info.items(), key=lambda item: int(item[1]), reverse=True))
        with open(self.path_to_file, 'w') as out, open(self.path_to_filefreq, 'w') as freq:
            for x, y in self.info.items():
                out.write(x)
                freq.write(y)


