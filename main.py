# Constants
GET_CARDINAL_DIRECTIONS = ["NORTH", "EAST", "SOUTH", "WEST"]
GET_DIRECTION_DELTAS = {
    "NORTH": (0, 1),
    "EAST": (1, 0),
    "SOUTH": (0, -1),
    "WEST": (-1, 0)
}
GRID_SIZE = 5

def is_within_bounds(x, y, direction):
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and direction in GET_CARDINAL_DIRECTIONS

def process_commands(commands):
    is_placed = False
    current_x = 0
    current_y = 0
    current_direction = None

    for command in commands:
        command = command.strip() # Remove leading/trailing whitespace
        args = command.split(" ") # Split command into parts

        if args[0] == "PLACE":
            initial_placement = args[1].split(",")
            new_x = int(initial_placement[0])
            new_y = int(initial_placement[1])
            new_direction = initial_placement[2].strip().upper()

            if is_within_bounds(new_x, new_y, new_direction):
                current_x, current_y, current_direction = new_x, new_y, new_direction
                is_placed = True

        elif not is_placed:
            continue  # Ignore commands until robot is placed

        elif command == "MOVE":
            dx, dy = GET_DIRECTION_DELTAS[current_direction]
            new_x = current_x + dx
            new_y = current_y + dy
            if is_within_bounds(new_x, new_y, current_direction):
                current_x, current_y = new_x, new_y

        elif command == "LEFT":
            current_idx = GET_CARDINAL_DIRECTIONS.index(current_direction)
            current_direction = GET_CARDINAL_DIRECTIONS[(current_idx - 1) % 4] # Turn left (counter-clockwise)

        elif command == "RIGHT":
            current_idx = GET_CARDINAL_DIRECTIONS.index(current_direction)
            current_direction = GET_CARDINAL_DIRECTIONS[(current_idx + 1) % 4] # Turn right (clockwise)

        elif command == "REPORT":
            print(f"{current_x},{current_y},{current_direction}")

if __name__ == "__main__":
    commands = [
        "PLACE 1,2,EAST",
        "MOVE",
        "MOVE",
        "LEFT",
        "MOVE",
        "REPORT"
    ]
    # Expected: 3,3,NORTH

    commands = [
        "PLACE 0,4,NORTH",
        "MOVE",
        "REPORT"
    ]
    # Expected: 0,4,NORTH (move should be ignored)

    commands = [
        "MOVE",
        "LEFT",
        "RIGHT",
        "REPORT",
        "PLACE 2,2,SOUTH",
        "MOVE",
        "REPORT"
    ]
    # Expected: 2,1,SOUTH

    commands = [
        "PLACE 5,5,EAST",  # Invalid
        "PLACE 3,3,NORTH",
        "MOVE",
        "REPORT"
    ]
    # Expected: 3,4,NORTH

    commands = [
        "PLACE 0,0,NORTH",
        "MOVE",
        "REPORT",
        "PLACE 4,4,WEST",
        "MOVE",
        "REPORT"
    ]
    # Expected:
    # 0,1,NORTH
    # 3,4,WEST

    process_commands(commands)