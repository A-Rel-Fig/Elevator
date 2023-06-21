# Elevator Simulation

# Requirements: 
Python code that simulates an elevator.

  1. The result should be an executable, or script, that can be run with the following inputs and generate the following outputs.
     - Inputs: [list of floors to visit] (e.g elevator start=12 floor=2,9,1,32)
     - Outputs: [total travel time, floors visited in order] (e.g 560 12,2,9,1,32)               
     - Program Constants: Single floor travel time: 10

## How It Works:
  
  - Pass a file containing a collection of floors for this elevator program to navigate through as the only required argument
    
    - This file will parse each floor entry as an positive integer with a comma being used as the delimiter, and each set of floors to travel to will be parsed by reading the next line for the next set of floor entries. 
    - An example floor list: `12, 2, 9, 1, 32`
  
  - Pass a optional file with the -o flag to write the 'total travel time' and 'floors visited in order'
