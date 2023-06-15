import os, argparse, re
from pathlib import Path

class ArgumentParserWrapper:
    
    CMD_VAR_REGEX = "%\((.*?)\)s"
    VALID_ARGUMENTS = set(["INPUT", "OUTPUT"])

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--command", type=str, required=True)
        self.parser.add_argument("-i", "--input_format", required=True)
        self.parser.add_argument("-o", "--output_format")

    def make_command(self) -> str:
        args = self.parser.parse_args()
        self.assert_command_validity(args)
        return args.command, args.input_format, args.output_format

    def assert_command_validity(self, args) -> None:
        matches = re.findall(self.CMD_VAR_REGEX, args.command)
        matches_set = set(matches)
        assert matches_set != set(), "No INPUT or OUTPUT found in command"
        assert "INPUT" in matches_set, "INPUT is compulsory" 
        assert len(matches_set) == len(matches), "Name conflict. INPUT and OUTPUT can only appear once."
        assert not (matches_set.difference(self.VALID_ARGUMENTS)), "Invalid argument name. Only use %(INPUT)s or %(OUTPUT)s in the general command string."

        if "OUTPUT" in matches_set:
            assert not args.output_format is None, "OUTPUT argument specified but format not provided."

class DirHandler:
    def __init__(self, command_args:tuple) -> None:
        self.command, self.input_format, self.output_format = command_args

    def get_key_folder(self, input_file_list:list) -> int:
        fpath_1, fpath_2 = input_file_list[0].split(os.sep), input_file_list[1].split(os.sep)
        assert len(fpath_1) == len(fpath_2), "Folder structure not consistent. Please check children directories."
        for index in range(len(fpath_1)):
            if fpath_1[index] != fpath_2[index]:
                return index

    def get_all_input_files(self) -> list:
        input_file_list = []
        for root, _, files in os.walk(os.getcwd()):
            for file in files:
                if file.endswith(self.input_format):
                    input_file_list.append(os.path.join(root, file))
        return input_file_list

    def get_commands(self):
        commands = []
        input_files = self.get_all_input_files()
        key_index = self.get_key_folder(input_files)
        
        for input in input_files:
            key = input.split(os.sep)[key_index]

            output = ""
            if self.output_format:
                pwd = Path(input).parent.absolute()
                output = os.path.join(pwd, f"{key}{self.output_format}")
            
            mapping = {"INPUT" : input, "OUTPUT" : output}
            full_command = self.command%mapping
            commands.append(full_command)
        return commands
    
    def run_all_commands(self, command_list):
        for command in command_list:
            print(command)
            os.system(command)
            print()

    def verify_run(self):
        commands = self.get_commands()
        print("Is the example command shown below formatted correctly? (y/n)")
        response = input(commands[0] + "\n")
        if response == "y":
            self.run_all_commands(commands)
        else:
            print("Script aborting...")

    
apw = ArgumentParserWrapper()
dh = DirHandler(apw.make_command())
dh.verify_run()
