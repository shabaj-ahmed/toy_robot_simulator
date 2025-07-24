class Simulator:
    def __init__(self, controller):
        self.controller = controller

    def run_from_default_file(self):
        filename = "data/commands.txt"
        try:
            with open(filename, "r") as file:
                for line in file:
                    command = line.strip()
                    if command:
                        self.controller.process_command(command)
        except FileNotFoundError:
            print(f"Error: '{filename}' not found.")
