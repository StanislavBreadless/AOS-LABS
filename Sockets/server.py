import socket                
import os
from datetime import datetime



LOG_FILE = 'server-log.log'
WHO_COMMAND = 'Who'
WHO_STR = 'Станіслав Безкоровайний, К-27. Віддалена консоль.\n'
EXIT_MARKER = '\nexit\n'
EXIT_MARKER_LEN = len(EXIT_MARKER)

s = socket.socket()          
print ("Socket successfully created")
   
port = 1025 + 3               
s.bind(('', port))         

print ("socket binded to %s", port)
  
s.listen(5)      
print("socket is listening") 

def log_data(data, addr, recv):
  log_file = open(LOG_FILE, 'a+')

  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")

  info_str = ''

  if recv:
    info_str = 'Recevied from %s at %s:\n' % (addr, current_time)
  else:
    info_str = 'Sent to %s at %s:\n' % (addr, current_time)


  log_file.write(info_str)
  log_file.write(data)
  # A little piece of beauty😊
  log_file.write('\n------------------------\n')

  log_file.close()

def exit_marker_found(data_str):
  data_len = len(data_str)
  data_end = data_str[data_len-EXIT_MARKER_LEN: data_len]
  return len(data_str) >= EXIT_MARKER_LEN and data_end == EXIT_MARKER

def get_data(client):
  data_str = '' 
  while True:
    print('Cycle going....')
    packet = client.recv(1024)
    print(not packet)
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
  
   # Establish connection with client. 
   client, addr = s.accept()      
   print ('Got connection from', addr)

   data = get_data(client)
   log_data(data, addr, recv=True)

   executed_data = exec_commands(data)
   log_data(executed_data, addr, recv=False)

   sent_bytes = client.sendall(executed_data.encode('ascii'))
   client.close() 