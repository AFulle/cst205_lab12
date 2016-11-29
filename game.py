def welcome_message():
  printNow("Welcome to Bitspice Island!")
  
def help_message():
  printNow("""In each room you will be told which directions you can go
You'll be able to go north, south, east or west by typing that direction
Type help to redisplay this introduction
Type exit to quit at any time""")
def command_parser(command):
  if command == "help":
    help_message()
    return ('help', None)
  elif command == "exit":
    return ('exit', None)
  elif command.startswith("go"):
    direction = command.split(" ")[1]
    if direction == None:
      return ('move', (0,0))
    else:
      if direction == "north":
        return ('move', (0, -1))
      elif direction == "south":
        return ('move', (0, 1))
      elif direction == "west":
        return ('move', (-1, 0))
      elif direction == "east":
        return ('move', (1, 0))
      else:
        return ('move', (0,0))
    
class Room(object):
  """base room class for all the rooms in the game"""
  def __init__(self, room_name, room_description, row, column, total_rows, total_columns):
    self.room_name = room_name
    self.room_description = room_description
    self.row = row
    self.column = column
    self.total_rows = total_columns
    self.total_columns = total_columns
    
  def get_move_directions(self):
    move_directions = []
    if self.column >= 0 and self.column < self.total_columns - 1:
      move_directions = move_directions + ["east"]
    if self.column < self.total_columns and self.column != 0:
      move_directions = move_directions + ["west"]
    if self.row >= 0 and self.row < self.total_rows - 1:
      move_directions = move_directions + ["south"]
    if self.row < self.total_rows and self.row != 0:
      move_directions = move_directions + ["north"]
    return move_directions
    
  def get_description(self):
    return self.room_description
    
  def get_name(self):
    return self.room_name
  
  def get_position(self):
    return (self.column, self.row)
    
# Rooms with descriptions
class EntranceRoom(Room):
  def __init__(self, row, column, total_rows, total_columns):
    super(EntranceRoom, self).__init__("Entrance Room (" + str(column) + "," + str(row) +")", "This is the entrance to the room, you see nothing of particular value in this room.", row, column, total_rows, total_columns)
class Lobby(Room):
  def _init_(self, row, column, total_rows, total_columns):
    super(Lobby, self).__init__("Lobby (" + str(column) + "," + str(row) +")", "This is the lobby, you see expensive funiture all around and two doors. A corner of this room is filled with broken chairs. You can go east or north.", row, column, total_rows, total_columns)
class DiningRoom(Room):
  def _init_(self, row, column, total_rows, total_columns):
    super(DiningRoom, self).__init__("Dining Room (" + str(column) + "," + str(row) +")", "This is the dining room, you see a huge table. There are very expensive paintings on the wall and two doors. You can go east or west.", row, column, total_rows, total_columns)
class DarkRoom(Room):
  def __init__(self, row, column, total_rows, total_columns):
    super(DarkRoom, self).__init__("Dark Room (" + str(column) + "," + str(row) +")", "This is the dark room, you see a large collection of previous visitors. There are two doors, you can go north and south.", row, column, total_rows, total_columns)
class Basement(Room):
  def __init__(self, row, column, total_rows, total_columns):
    super(Basement, self).__init__("Basement (" + str(column) + "," + str(row) +")", "This is the basement, you see empty boxes and cages. There is a weird smell in the air and a weird door to the west. You can go west or south.", row, column, total_rows, total_columns)
class Dungeon(Room):
  def _init_(self, row, column, total_rows, total_columns):
    super(Dungeon, self).__init__("Dungeon(" + str(column) + "," + str(row) +")", "You took a wrong turn and wound up in the dungeon. GAME OVER", row, column, total_rows, total_columns)
class HiddenRoom(Room):
  def __init__(self, row, column, total_rows, total_columns):
    super(HiddenRoom, self).__init__("Hidden Room (" + str(column) + "," + str(row) +")", "Congratualtions! You found the hidden room. You see diamonds and gold on a wooden table. YOU WIN!", row, column, total_rows, total_columns)

def create_game(rows, columns):
  map = {}
  starting_column = 0
  starting_row = 0
  for row in range(0,rows):
    for column in range(0, columns):
      ### TODO: We need to randomly choose from a list of predefined rooms.
      ### Possible solution: Make a list of pre-created rooms, and slowly fill the map with them.
      ### We can even randomize the map by choosing a random location for each. If we do so
      ### We need to set the starting_column and starting_row to that of wherever the entrance room is.
      ### Ex: if entrance_room, set starting_column = column, starting_row = row
      ### If you want to attempt random, use randint and you import 'from random import randint' at the top
      ### in order to not overwrite rooms, make sure you check if a room exists there already, if it does, run random again until you get an empty slot.
      ### Alternative method: Have a list of all possible room slots, randomly pick one for a room, and remove it from the list. Could be faster and less error prone.
      room = EntranceRoom(row, column, rows, columns)
      if map.get(column) == None:
        map[column] = {}
      map[column][row] = room
  return (map, (starting_column, starting_row))
  
# Game Loop
done = False
game_map, starting_room = create_game(3,3)
current_room = game_map[starting_room[0]][starting_room[1]]
welcome_message()
help_message()
while(True):
  printNow("You have entered the '" + current_room.get_name() + "'")
  printNow(current_room.get_description())
  command = requestString("What do you want to do? (Valid Directions: " + ", ".join(current_room.get_move_directions()) + ")").strip()
  result = command_parser(str(command))
  if result[0] == 'move':
    new_room_position = tuple([i1+i2 for i1, i2 in zip(current_room.get_position(), result[1])])
    ### TODO: Need to verify directions is valid before moving. compare agains get_move_directions.
    ### Maybe make a custom function which has hybrid capability between get_move_directions and the command parser
    ### for the north/south/east/west movement.
    current_room = game_map[new_room_position[0]][new_room_position[1]]
  if result[0] == 'exit':
    printNow("Thanks for playing!")
    break
