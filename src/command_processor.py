class CommandProcessor:

    def __init__(self):
        self.command_list = []
        print("Command Processor Loaded")

    def get_commands(self):
        return self.command_list

    def dump_commands(self):
        self.print_section("Dump commands")
        for command in self.command_list:
            print(command)

    def tokenize(self, data):
        tokens = []
        for line in data.splitlines():
            line = line.split('#')[0]
            tokens.extend(line.split())
        return tokens

    def parse_block(self, tokens, index):
        """Parse tokens from index until a closing ] or end of tokens.
        Returns (list of [command, param] pairs, next index)."""
        commands = []
        while index < len(tokens):
            token = tokens[index]

            if token == ']':
                return commands, index + 1

            elif token.upper() == 'REPEAT':
                count = int(tokens[index + 1])
                index += 2
                if index < len(tokens) and tokens[index] == '[':
                    index += 1  # skip [
                block_commands, index = self.parse_block(tokens, index)
                for _ in range(count):
                    commands.extend(block_commands)

            elif token.upper() == 'FOR':
                start = int(tokens[index + 1])
                end = int(tokens[index + 2])
                step = int(tokens[index + 3])
                index += 4
                if index < len(tokens) and tokens[index] == '[':
                    index += 1  # skip [
                block_commands, index = self.parse_block(tokens, index)
                for i in range(start, end + 1, step):
                    for cmd in block_commands:
                        param = i if cmd[1] == '$i' else cmd[1]
                        commands.append([cmd[0], param])

            elif index + 1 < len(tokens) and (tokens[index + 1].isdigit() or tokens[index + 1] == '$i'):
                param = tokens[index + 1] if tokens[index + 1] == '$i' else int(tokens[index + 1])
                commands.append([token.upper(), param])
                index += 2

            else:
                index += 1

        return commands, index

    def process_raw_input(self, data):
        self.command_list.clear()

        self.print_section("RawData")
        print(data)

        tokens = self.tokenize(data)
        self.command_list, _ = self.parse_block(tokens, 0)

    def print_section(self, name):
        self.print_seperator()
        print(name)
        self.print_seperator()

    def print_seperator(self):
        print("---------------------------")

    def load_test_file(self, filename):
        data = None

        try:
            with open(filename, 'r') as file:
                data = file.read()
        except Exception as e:
            print(e)

        if data is not None:
            self.process_raw_input(data)

        self.dump_commands()

        return data



if __name__ == '__main__':
    import command_processor
    c = command_processor.CommandProcessor()
    c.load_test_file("command_test.txt")
    commands = c.get_commands()

    for command in commands:
        print(command)
