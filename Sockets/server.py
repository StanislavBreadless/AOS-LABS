import socket                
import os
import logging
import sys
from datetime import datetime

LOG_FILE = 'server-log.log'
WHO_COMMAND = 'Who'
WHO_STR = 'Станіслав Безкоровайний, К-27. Віддалена консоль.\n'
EXIT_MARKER = '\nexit\n'
EXIT_MARKER_LEN = len(EXIT_MARKER)
PORT = 1025 + 3

logging.basicConfig(filename=LOG_FILE, encoding='ascii', level=logging.INFO)

s = socket.socket()          
print ("Socket successfully created")

s.bind(('', PORT))         
print ("socket binded to", PORT)

s.listen(5)      
print("socket is listening") 

def log_data(data, addr, recv):
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")

  info_str = ''

  if recv:
    info_str = 'Recevied from %s at %s:\n' % (addr, current_time)
  else:
    info_str = 'Sent to %s at %s:\n' % (addr, current_time)


  info_str = info_str = '\n' + data
  # A little piece of beauty😊
  info_str = info_str + '\n------------------------\n'

  logging.info(info_str)

def exit_marker_found(data_str):
  data_len = len(data_str)
  data_end = data_str[data_len-EXIT_MARKER_LEN: data_len]
  return len(data_str) >= EXIT_MARKER_LEN and data_end == EXIT_MARKER

def get_data(client):
  data_str = '' 
  while True:
    packet = client.recv(1024)
    if not packet:
      break
    data_str += packet.decode('ascii')

    if exit_marker_found(data_str):
      break

  return data_str


def exec_commands(commands_str):
  commands = commands_str.splitlines()

  result_str = ''

  for command in  commands:
    if command == WHO_COMMAND:
      result_str += WHO_STR
      continue

    stream = os.popen(command)
    result_str += stream.read()

  return result_str


while True: 
  
  try: 
    # Establish connection with client. 
    client, addr = s.accept()      
    print ('Got connection from', addr)

    data = get_data(client)
    log_data(data, addr, recv=True)

    executed_data = exec_commands(data)
    log_data(executed_data, addr, recv=False)

    sent_bytes = client.sendall(executed_data.encode('ascii'))
    client.close() 
  except OSError as err:
    logging.error('OS Error: {0}'.format(err))
  except IOError as err:
    logging.error("I/O error({0}): {1}".format(err))
  except: 
    logging.error("Unexpected error:", sys.exc_info()[0])
    raise