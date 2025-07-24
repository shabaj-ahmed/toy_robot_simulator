## Table of Contents
- [toy\_robot\_simulator](#toy_robot_simulator)
  - [Tabletop Grid and Coordinates](#tabletop-grid-and-coordinates)
  - [Supported Commands](#supported-commands)
  - [Constraints and Rules](#constraints-and-rules)
  - [Design Assumptions](#design-assumptions)
  - [Example Commands and Output](#example-commands-and-output)
    - [Example A:](#example-a)
    - [Example B](#example-b)
    - [Example C](#example-c)
  - [Project Structure](#project-structure)
  - [Logging Behaviour](#logging-behaviour)
  - [Setup Instructions](#setup-instructions)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Create a Virtual Environment (Recommended)](#2-create-a-virtual-environment-recommended)
    - [3. Install Dependencies](#3-install-dependencies)
    - [4. Run the Simulator](#4-run-the-simulator)
    - [5. Running Tests](#5-running-tests)
  - [Sample Commands and Expected Output](#sample-commands-and-expected-output)
    - [Sample commands.txt file](#sample-commandstxt-file)
    - [Expected Console Output](#expected-console-output)
    - [Expected Log Output](#expected-log-output)
  - [Execution Flow Explained](#execution-flow-explained)
    - [Step-by-step Flow:](#step-by-step-flow)
  - [Future improvements.](#future-improvements)

# toy_robot_simulator 
This is a simulation of a toy robot placed on a 5×5 tabletop grid using text-based commands. The robot can be placed at specific coordinates, rotated left or right, moved forward, and asked to report its position. Commands are read from a plain text file and processed in order.

This simulator ensures that:
- The robot does not fall off the table.
- Only valid commands are executed.
- Warnings and errors are logged to a file.
- The robot’s final position and direction are reported when requested.

## Tabletop Grid and Coordinates 
- The tabletop is a 5×5 grid.
- The bottom-left corner is `(0, 0)` and the top-right corner is `(4, 4)`.

## Supported Commands 
- `PLACE X,Y,F`: Place the robot on the table at position (X, Y) facing F (`NORTH`, `SOUTH`, `EAST`, or `WEST`).
- `MOVE`: Move one unit forward in the current direction.
- `LEFT`: Turn the robot 90° to the left.
- `RIGHT`: Turn the robot 90° to the right.
- `REPORT`: Output the current position and direction.

## Constraints and Rules 
1. **Initial Placement**: The robot must be placed on the table using a valid `PLACE` command before any other command will be executed.
2. **Invalid Commands**: Commands are ignored if:
  - The robot has not yet been placed on the table.
  - The `PLACE` command includes out-of-bounds coordinates (e.g., `PLACE 5,5,NORTH`).
  - A `MOVE` command would cause the robot to fall off the table.
  - The command format is invalid or unrecognised.

## Design Assumptions 
* Commands are received asynchronously (e.g., from a file or future message queue).
* Messages cannot be guaranteed to be in the correct format or case, so they must be validated before processing (e.g., `place` and `north` are invalid).
* If no commands are executed or all commands are invalid, an empty string will be printed when `REPORT` is requested.
* The simulator only prints results to the terminal. Logs (warnings/errors) are saved to a separate log file.
* The first valid `PLACE` command enables the robot. All subsequent valid commands are then accepted.
* If a `PLACE` command is invalid, the robot retains its previous valid position and direction.


## Example Commands and Output
### Example A: 
```
PLACE 0,0,NORTH 
MOVE 
REPORT
```
-> Output: 0,1,NORTH

### Example B 
```
PLACE 1,2,EAST 
MOVE 
MOVE 
LEFT 
MOVE 
REPORT 
```
-> Output: 3,3,NORTH

### Example C
The initial PLACE is out of bounds. All subsequent commands are ignored.
```
PLACE 5, 6, SOUTH 
RIGHT 
MOVE 
RIGHT 
MOVE 
REPORT
```
-> Output: 
*No output* (because the initial `PLACE` was invalid — the robot is never placed on the table)

## Project Structure
```
toy_robot_simulator/ 
│ 
├── config/ 
│ ├── __init__.py 
│ └── logging_config.py # Sets up logging format and handlers 
│ 
├── data/ 
│ └── commands.txt # Input file containing newline-separated commands 
│ 
├── logs/ 
│ └── robot_simulator.log # Output log file for warnings and errors 
│ 
├── tests/ # Unit and integration tests 
│ ├── __init__.py 
│ ├── test_robot.py # Tests for Robot movement and direction logic 
│ ├── test_navigation.py # Tests for grid boundaries and valid positions 
│ ├── test_controller.py # Tests for command parsing and control logic 
│ └── test_integration.py # End-to-end tests of command sequences 
│ 
├── toy_robot/ # Core simulator logic 
│ ├── __init__.py 
│ ├── robot.py # Handles position, orientation, and movement 
│ ├── navigation.py # Validates grid boundaries and safe moves 
│ ├── controller.py # Parses and processes commands 
│ └── simulator.py # Feeds commands to the controller (from commands.txt) 
│ 
├── main.py # Entry point: runs the simulator with data/commands.txt file 
├── .gitignore 
├── README.md 
└── requirements.txt
```

## Logging Behaviour 
- All logs are saved to `logs/robot_simulator.log`.
- Only warnings and errors are logged (e.g., invalid moves, out-of-bounds placements).
- Logging configuration is defined in `config/logging_config.py`.

## Setup Instructions 


### 1. Clone the Repository 

```bash
git clone https://github.com/your-username/toy_robot_simulator.git
cd toy_robot_simulator
```
### 2. Create a Virtual Environment (Recommended) 
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies 
```bash
pip install -r requirements.txt
```

### 4. Run the Simulator 
```bash
python main.py
```
By default, this reads from data/commands.txt 


### 5. Running Tests
To run all unit and integration tests, run the following command from the project root directory:
```bash
pytest
```

## Sample Commands and Expected Output
This project includes a sample command sequence stored in data/commands.txt. You can run the simulator with this file or modify it to test your scenarios.


### Sample commands.txt file
```
MOVE
PLACE 5,5,EAST
LEFT
PLACE 0,0,SOUTH
MOVE
REPORT
PLACE 0,0,NORTH
MOVE
MOVE
LEFT
MOVE
REPORT
PLACE 1,2,EAST
MOVE
MOVE
LEFT
MOVE
REPORT
```

### Expected Console Output
```bash
Output: 0,2,WEST
Output: 3,3,NORTH
```

### Expected Log Output
Warnings and invalid commands are automatically saved to logs/robot_simulator.log. For example, given malformed or unsafe commands, the log may contain:
```bash
2025-07-24 11:05:43,110 - RobotController - WARNING - Ignoring 'MOVE' as no PLACE command has been issued yet.
2025-07-24 11:05:43,110 - Navigation - WARNING - Invalid position check: (5,5) is out of bounds.
2025-07-24 11:05:43,110 - RobotController - WARNING - PLACE ignored: invalid position (5,5,EAST)
2025-07-24 11:05:43,110 - RobotController - WARNING - Ignoring 'LEFT' as no PLACE command has been issued yet.
2025-07-24 11:05:43,110 - Navigation - WARNING - Invalid position check: (0,-1) is out of bounds.
2025-07-24 11:05:43,110 - RobotController - WARNING - Unsafe MOVE ignored: (0,-1SOUTH)
2025-07-24 11:05:43,111 - Navigation - WARNING - Invalid position check: (-1,2) is out of bounds.
2025-07-24 11:05:43,111 - RobotController - WARNING - Unsafe MOVE ignored: (-1,2WEST)
```

## Execution Flow Explained
Example commands that are processed:

```
  PLACE 0,0,NORTH
  MOVE
  REPORT
```

### Step-by-step Flow:
First command – `PLACE 0,0,NORTH`:
1. Simulator reads `PLACE 0,0,NORTH` and sends it to the Controller.
2. RobotController validates the command and asks Navigation if (0,0) is within bounds.
3. Since it's valid, it instructs Robot to place itself at (0,0) facing NORTH.
Second command – `MOVE`:
4. The command `MOVE` is read.
5. RobotController asks Robot to propose_move() → it returns (0,1).
6. Navigation confirms (0,1) is within bounds.
7. RobotController instructs Robot to update_position().
Final command – `REPORT`:
8. `REPORT` is executed.
9. Robot requested to print its position and direction:
```
   0,1,NORTH
```

## Future improvements.
* Custom exception classes for better error handling.
* Real-time message queue for microservice-style command input.
* Dockerised execution environment.
* Create a project Wiki with interface details and architecture overview.