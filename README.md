# toy_robot_simulator
This is a simulation of a toy robot placed on a 2D 5×5 tabletop grid. The robot can be placed at specific coordinates, rotated left or right, moved forward, and asked to report its position. Commands are provided in plain text and are processed in order.

The simulator must ensure that:
- The robot does not fall off the table.
- Only executes valid commands.
- The robot’s final position and direction are reported when requested.

## Commands
- `PLACE X,Y,F`: Place the robot on the table at position (X, Y) facing F (`NORTH`, `SOUTH`, `EAST`, or `WEST`).
- `MOVE`: Move one unit forward in the current direction.
- `LEFT`: Turn the robot 90° to the left.
- `RIGHT`: Turn the robot 90° to the right.
- `REPORT`: Output the current position and direction.

## Tabletop Grid and Coordinates
- The tabletop is a 5×5 grid.
- The bottom-left corner is `(0, 0)` and the top-right corner is `(4, 4)`.

## Constraints and Rules
1. **Initial Placement**: The robot must be placed on the table using a valid `PLACE` command before any other command will be executed.
2. **Invalid Commands**: Commands are ignored if:
   - The robot has not yet been placed on the table.
   - The `PLACE` command includes out-of-bounds coordinates (e.g., `PLACE 5,5,NORTH`).
   - A `MOVE` command would cause the robot to fall off the table.
   - The command format is invalid or unrecognised.

## Examples of Input and Output
### Example A:
PLACE 0,0,NORTH
MOVE
REPORT
-> Output: 0,1,NORTH

### Example B
PLACE 1,2,EAST
MOVE
MOVE
LEFT
MOVE
REPORT
-> Output: 3,3,NORTH

### Example C
PLACE 5, 6, SOUTH   
RIGHT   
MOVE
RIGHT
MOVE
REPORT
-> Output:
*No output* (because the initial `PLACE` was invalid — the robot is never placed on the table)

## How to Run
> TBD
