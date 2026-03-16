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
        
    def process_line(self,line,line_number):

        commands = line.split()

        current_command_index=0
        command_count=len(commands)
        
        if command_count>0:
            do_continue=True
        else:
            do_continue=False


        while do_continue:

            parm_val=None

            command = commands[current_command_index]
            next_command=None

            if current_command_index<command_count-1:
                next_command=commands[current_command_index+1]

                if next_command.isdigit():
                    parm_val=int(next_command)

            if parm_val is not None:
                current_command_index=current_command_index+2
                self.command_list.append([ command,parm_val ] )
                print("line: %d Command: %s Parameter: %d"%(line_number+1,command,parm_val))
            else:
                current_command_index=current_command_index+1
                    
            if current_command_index==command_count:
                do_continue=False

    def print_section(self,name):
        self.print_seperator()
        print(name)
        self.print_seperator()


    def print_seperator(self):
        print("---------------------------")

    def process_raw_input(self,data):
        self.command_list.clear()
        
        self.print_section("RawData")
        print(data)

        lines = data.splitlines()

        for line_number,line in enumerate(lines):
            self.process_line(line,line_number)


    def load_test_file(self,filename):
        data=None

        try:
            with open(filename, 'r') as file:
                raw = file.read()
                data = raw
        except Exception as e:
            print(e)

        if data is not None:
            self.process_raw_input(data)

        self.dump_commands()

        return data



        


        

