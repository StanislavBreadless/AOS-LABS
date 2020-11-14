# # Import socket module 
import socket            
import logging   
import sys
from datetime import datetime

PORT = 1025 + 3
FILE_MODE = '1'
PROMRT_MODE = '2'
LOG_FILE = 'client-log.log'

logging.basicConfig(filename=LOG_FILE, encoding='ascii', level=logging.INFO)

def get_socket():
  s = socket.socket()
  s.connect(('127.0.0.1', PORT))
  
  return s

def get_mode():
  while True:
    print('Choose mode: file(%s) or prompt(%s)' % (FILE_MODE, PROMRT_MODE))
    mode = input()

    if mode != FILE_MODE and mode != PROMRT_MODE:
      print('You should enter either 1 or 2!')
    else:
      return mode


def log_data(data, recv):
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")

  info_str = ''

  if recv:
    info_str = 'Recevied from server at %s:\n' % (current_time)
  else:
    info_str = 'Sent to server at %s:\n' % (current_time)

  info_str = info_str + '\n'
  info_str = info_str + data
  
  # A little piece of beauty😊
  info_str = info_str + '\n------------------------\n'

  logging.info(info_str)

def get_commands_from_file():
  print('Please, enter path to the file:')
  file_path = input()
  f = open(file_path, 'r')
  return f.readlines()

def get_commands_from_prompt():
  print('Enter your commands, one per line.')
  print('When you are done, enter "exit" (without quotes).')

  commands = []

  while True:
    command = input()
    if command == 'exit':
      break
    else:
      commands.append(command)
  
  return commands

def send_to_server(socket, commands):

  if len(commands) == 0:
    commands.append('\nexit')
  else:
    commands.append('exit')

  data = '\n'.join(commands) + '\n'

  socket.sendall(data.encode('ascii', errors='strict'))
  
  log_data(data, recv=False)

def get_data(socket):
  data_str = '' 
  while True:
    packet = socket.recv(1024)
    if not packet:
      break
    data_str += packet.decode('ascii')
  
  return data_str


mode = get_mode()

commands = ''

if mode == FILE_MODE:
  commands = get_commands_from_file()
else:
  commands = get_commands_from_prompt()

try:
  socket = get_socket()
  send_to_server(socket, commands)
  recevied_data = get_data(socket)
  log_data(recevied_data, recv=True)
except OSError as err:
  logging.error('OS Error: {0}'.format(err))
except IOError as err:
  logging.error("I/O error({0}): {1}".format(err))
except: 
  logging.error("Unexpected error:", sys.exc_info()[0])
  raise



