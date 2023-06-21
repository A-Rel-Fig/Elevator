from dataclasses import dataclass
import sys, getopt
import os.path as path
from colorama import Fore, Style
import time

SINGLE_FLOOR_TRAVEL_TIME = 10


class Elevator: 
  def __init__(self):
    self.single_floor_travel_time = SINGLE_FLOOR_TRAVEL_TIME
    self.total_travel_time = 0
    
  @property
  def current_floor(self):
    return self._current_floor

  @current_floor.setter
  def current_floor(self, new_current_floor):
    if new_current_floor < 0: 
      raise ValueError('current_floor.setter requires positive integer value')
    #print(Fore.GREEN + '[ElevatorArrival] ' + Style.RESET_ALL + user_color_coding('We ') + 'are currently at ' + numerical_color_coding('Floor ' + str(new_current_floor)))
    self._current_floor = new_current_floor
    
  @property
  def requested_floors(self):
    return self._requested_floors
  
  @requested_floors.setter
  def requested_floors(self, new_requested_floor_list):
    if not any(map(lambda floor: floor >= 0, new_requested_floor_list)):
      raise ValueError('requested_floor.setter requires a list of positive integer values')
    requested_floor = str(new_requested_floor_list[-1])
    #requesting_different_floor = requested_floor != str(self._current_floor)
    #if requesting_different_floor:
    print(Fore.BLUE + '[ElevatorRequestAccepted] ' + Style.RESET_ALL + 'Elevator has queued ' + numerical_color_coding('Floor ' + requested_floor) + ' for next destination')
    self._requested_floors = new_requested_floor_list
    
  @property
  def floors_visited_in_order(self):
    return self._floors_visited_in_order
  
  @floors_visited_in_order.setter
  def floors_visited_in_order(self, new_visited_floor_list):
    if not any(map(lambda floor: floor >= 0, new_visited_floor_list)):
      raise ValueError('floors_visited_in_order.setter requires a list of positive integer values')
    visited_floor = str(new_visited_floor_list[-1])
    print(Fore.CYAN + '[ElevatorRequestCompleted] ' + Style.RESET_ALL + 'Elevator has added ' + numerical_color_coding('Floor ' + visited_floor) + ' to list of visited floors')
    self._floors_visited_in_order = new_visited_floor_list
    
  @property
  def floors_traversed_in_order(self):
    return self._floors_traversed_in_order
  
  @floors_traversed_in_order.setter
  def floors_traversed_in_order(self, new_traversed_floor_list):
    if not any(map(lambda floor: floor >= 0, new_traversed_floor_list)):
      raise ValueError('floors_traversed_in_order.setter requires a list of positive integer values')
    traversed_floor = str(new_traversed_floor_list[-1])
    print(Fore.BLACK + '[ElevatorMovement] ' + Style.RESET_ALL + 'Elevator has added ' + numerical_color_coding('Floor ' + traversed_floor) + ' to list of all visited floors')
    self._floors_traversed_in_order = new_traversed_floor_list

    
def parse_argv(argv):
  set_output_file = False
  output_file = ''
  get_options, get_argument = getopt.getopt(argv, 'ho:', ['output='])
  for option, argument in get_options:
    if option == '-h':
      print('usage: main.exe -o <output_file_path> <input_file_path> ')
      sys.exit()
    elif option in ('-o', '--output'):
      output_file = argument
      set_output_file = True
  input_file = get_argument[0]
  if (not path.isfile(input_file)):
    print(Fore.RED + '[FileNotFoundError] ' + Style.RESET_ALL + 'No such file or directory for "input_file_path" argument')
    sys.exit()
  if (not path.isfile(output_file) and set_output_file):
    print(Fore.YELLOW + '[FileNotFoundWarning] ' + Style.RESET_ALL + 'No such file or directory for "output_file_path" option')
      
  with open(input_file) as input_stream: 
    lines = list(input_stream.readlines())
    parsed_lines = list(map(lambda line: line.strip(), lines)) # Remove new line
  return (parsed_lines, output_file)

def move_elevator(elevator: Elevator):
  while elevator.current_floor != elevator.requested_floors[-1]:
    if elevator.current_floor < elevator.requested_floors[-1]:
      elevator.current_floor += 1
      elevator.total_travel_time += elevator.single_floor_travel_time
      elevator.floors_traversed_in_order.append(elevator.current_floor)
      print(Fore.BLACK + '[ElevatorMovement] ' + Fore.YELLOW + "Moving up to floor " + str(elevator.current_floor) + Style.RESET_ALL)
      time.sleep(0.200)
    elif elevator.current_floor > elevator.requested_floors[-1]:
      elevator.current_floor -= 1
      elevator.total_travel_time += elevator.single_floor_travel_time
      elevator.floors_traversed_in_order.append(elevator.current_floor)
      print(Fore.BLACK + '[ElevatorMovement] ' + Fore.YELLOW + "Moving down to floor " + str(elevator.current_floor) + Style.RESET_ALL)
      time.sleep(0.200)
    
def numerical_color_coding(message: str):
    return Fore.LIGHTMAGENTA_EX + message + Style.RESET_ALL

def main(argv):
  parsed_floot_list, output_file = parse_argv(argv)
  print(Fore.MAGENTA + 'Welcome to the Elevator!' + Style.RESET_ALL)
  for single_floor_list in parsed_floot_list:
    floors = [int(floor) for floor in single_floor_list.split(',')]
    if (len(floors) <= 0): 
      print(Fore.RED + '[InputFormatError] ' + Style.RESET_ALL + 'Unable to parse floors from "input_file_path" argument')
      sys.exit()
    
    elevator_start = floors.pop(0)
    elevator = Elevator()
    elevator.requested_floors = [elevator_start]
    elevator.floors_visited_in_order = [elevator_start]
    elevator.floors_traversed_in_order = [elevator_start]
    elevator.current_floor = elevator_start
    print(Fore.GREEN + 'This is the pre-boarding announcement for Floor ' + numerical_color_coding(str(elevator_start)) + Style.RESET_ALL)
    time.sleep(0.500)
    
    for floor in floors:
      if floor != elevator.requested_floors[-1]: # Prevent requesting the what is recently queued 
        current_requested_floors = elevator.requested_floors #elevator.requested_floors = elevator.requested_floors.append(floor)
        current_requested_floors.extend([floor])
        elevator.requested_floors = current_requested_floors
        del current_requested_floors
        
        move_elevator(elevator)
        
        current_visited_floors = elevator.floors_visited_in_order #elevator.floors_visited_in_order = elevator.floors_visited_in_order.append(floor)
        current_visited_floors.extend([floor])
        elevator.floors_visited_in_order = current_visited_floors
        del current_visited_floors
        
        elevator.current_floor = floor
        print(Fore.GREEN + 'This is the pre-boarding announcement for Floor ' + str(floor) + Style.RESET_ALL)
        time.sleep(0.500)
    
    if output_file:
      with open(output_file, 'a') as output_stream:
        output_stream.write(str(elevator.total_travel_time))
        output_stream.write(str(elevator.floors_visited_in_order))
        output_stream.write(str(elevator.floors_traversed_in_order))
        output_stream.write('\n')
      
    #return (elevator.total_travel_time, elevator.floors_visited_in_order)
    #return (elevator.total_travel_time, elevator.floors_visited_in_order, elevator.floors_traversed_in_order)
    print(Fore.LIGHTBLACK_EX + 'Total travel time: ' + Fore.LIGHTGREEN_EX + str(elevator.total_travel_time) + Style.RESET_ALL)
    print(Fore.LIGHTBLACK_EX + 'Floors visited in order: ' + Fore.LIGHTGREEN_EX + str(elevator.floors_visited_in_order) + Style.RESET_ALL)
    print(Fore.LIGHTBLACK_EX + 'Floors traversed in order: ' + Fore.LIGHTGREEN_EX + str(elevator.floors_traversed_in_order) + Style.RESET_ALL)
    
if __name__ == '__main__':
  #total_travel_time, floors_visited_in_order, floors_traversed_in_order = main(sys.argv[1:])
  main(sys.argv[1:])
  