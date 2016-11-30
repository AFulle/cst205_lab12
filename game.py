from random import randint
import sys

# This will convert a string of the name of a class into the actual class.
def str_to_class(str):
    return globals()[str]

def welcome_message():
  printNow("Welcome to Bitspice Island!")
  
def help_message():
  printNow("""In each room you will be told which directions you can go
You'll be able to go north, south, east or west by typing that direction
Type pickup to pick up an item, you need to type the name exactly, including capitalization.
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
  elif command.startswith("pickup"):
    return ('pickup', command[len("pickup "):])
    
    
def get_move_directions(column, row, total_columns, total_rows):
  move_directions = []
  if column >= 0 and column < total_columns - 1:
    move_directions = move_directions + ["east"]
  if column < total_columns and column != 0:
    move_directions = move_directions + ["west"]
  if row >= 0 and row < total_rows - 1:
    move_directions = move_directions + ["south"]
  if row < total_rows and row != 0:
    move_directions = move_directions + ["north"]
  return move_directions

class Room(object):
  """base room class for all the rooms in the game"""
  def __init__(self, room_name, room_description, row, column, total_rows, total_columns):
    move_directions = get_move_directions(column, row, total_columns, total_rows)
    self.room_name = room_name
    tense = "is"
    if not len(move_directions) == 1:
      tense = "are"
    self.room_description = room_description + " There " + tense + " " + str(len(move_directions)) + " doors, and you can go " + ", ".join(move_directions)
    self.row = row
    self.column = column
    self.total_rows = total_rows
    self.total_columns = total_columns
    self.items = []
    
  def get_move_directions(self):
    return get_move_directions(self.column, self.row, self.total_columns, self.total_rows)
    
  def get_description(self):
    return self.room_description
    
  def get_name(self):
    return self.room_name
  
  def get_position(self):
    return (self.column, self.row)
    
  def add_item(self, item_name):
    self.items = self.items + [item_name]
    
  def get_items(self):
    return self.items
    
  def remove_item(self, item_name):
    if item_name in self.items: 
      self.items.remove(item_name)
      return item_name
    return "invalid"
    
# Rooms with descriptions
class EntranceRoom(Room):
  def __init__(self, row, column, total_rows, total_columns):
    super(EntranceRoom, self).__init__("Entrance Room (" + str(column) + "," + str(row) +")", "This is the entrance to the room, you see nothing of particular value in this room.", row, column, total_rows, total_columns)

class DiningRoom(Room):
  def __init__(self, row, column, total_rows, total_columns):
    super(DiningRoom, self).__init__("Dining Room (" + str(column) + "," + str(row) +")", "This is the dining room, you see a huge table. There are very expensive paintings on the wall.", row, column, total_rows, total_columns)

class DarkRoom(Room):
  def __init__(self, row, column, total_rows, total_columns):
    super(DarkRoom, self).__init__("Dark Room (" + str(column) + "," + str(row) +")", "This is the dark room, you see a large collection of previous visitors.", row, column, total_rows, total_columns)

class Dungeon(Room):
  def __init__(self, row, column, total_rows, total_columns):
    super(Dungeon, self).__init__("Dungeon (" + str(column) + "," + str(row) +")", "This is the dungeon, there are glowing eyes in the darkness, and the door comes to a loud thundering close behind you.", row, column, total_rows, total_columns)

class Basement(Room):
  def __init__(self, row, column, total_rows, total_columns):
    super(Basement, self).__init__("Basement (" + str(column) + "," + str(row) +")", "This is the basement, you see empty boxes and cages. There is a weird smell in the air", row, column, total_rows, total_columns)

class HiddenRoom(Room):
  def __init__(self, row, column, total_rows, total_columns):
    super(HiddenRoom, self).__init__("Hidden Room (" + str(column) + "," + str(row) +")", "You try the secret key and it opens the door. Congratualtions! You found the hidden room. You see diamonds and gold on a wooden table.", row, column, total_rows, total_columns)

def create_game(rows, columns):
  map = {}
  starting_column = 0
  starting_row = 0
  rooms = [EntranceRoom,DiningRoom, DarkRoom, Basement, HiddenRoom, Dungeon]
  for row in range(0,rows):
    for column in range(0, columns):
      if len(rooms) > 1:
        choice = randint(0,len(rooms)-1)
      else:
        choice = 0
      printNow(rooms[choice])
      room = rooms[choice](row, column, rows, columns)
      rooms.remove(rooms[choice])
      if "Entrance Room" in room.get_name():
        starting_column = column
        starting_row = row
        room.add_item("Rose")
      if "Dining Room" in room.get_name():
        room.add_item("Secret Key")
      if "Dark Room" in room.get_name():
        room.add_item("Skeleton Key")
      if "Dungeon" in room.get_name():
        room.add_item("Death")
      if map.get(column) == None:
        map[column] = {}
      map[column][row] = room
  return (map, (starting_column, starting_row))
  
# Game Loop
done = False
game_map, starting_room = create_game(3,2)
current_room = game_map[starting_room[0]][starting_room[1]]
player_inventory = []
welcome_message()
help_message()
while(True):
  printNow("You have entered the '" + current_room.get_name() + "'")
  printNow(current_room.get_description())
  printNow("You see the following items in the room: " + ", ".join(current_room.get_items()))

  command = requestString("What do you want to do? (Valid Directions: " + ", ".join(current_room.get_move_directions()) + ")").strip()
  result = command_parser(str(command))
  if result[0] == 'move':
    if len(command.split(" ")) == 2 and command.split(" ")[1] in current_room.get_move_directions():
      new_room_position = tuple([i1+i2 for i1, i2 in zip(current_room.get_position(), result[1])])
      new_room = game_map[new_room_position[0]][new_room_position[1]]

      current_room = new_room
    else:
      printNow("Invalid direction, please try again.")
  if result[0] == 'pickup':
    item = current_room.remove_item(result[1])
    if item == "invalid":
      printNow("You entered an invalid item name, try again.")
    player_inventory = player_inventory + [item]
  if result[0] == 'exit':
    printNow("Thanks for playing!")
    break
  
