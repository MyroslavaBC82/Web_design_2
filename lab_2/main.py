import json
import select
import socket
import sys
from datetime import datetime


address = ("localhost", 3000)
lastname = "Liubchenko"
timer = 20.0


def run_server():
  server = socket.create_server(address)
  server.setblocking(False)

  rlist = [server]
  wlist = []

  start = None

  data = {"clients": []}

  print("listening")

  while rlist:
    rready, _, xready = select.select(rlist, [], rlist, 0.5)

    if xready:
      print("exception occurred")
      return

    for wo in rready:
      if wo is server:
        conn, addr = server.accept()
        conn.setblocking(False)
        rlist.append(conn)

        print("client connected")

        if start is None:
          start = datetime.now()
          data["timer_start_date"] = start.isoformat(" ", "seconds")

          print("timer started")
      else:
        client_data = json.loads(wo.recv(1024).decode())
        client_data["client_connection_date"] = datetime.now().isoformat(" ", "seconds")
        data["clients"].append(client_data)
        rlist.remove(wo)
        wlist.append(wo)

    if (start is not None) and ((datetime.now() - start).total_seconds() >= timer):
      server.close()
      rlist.remove(server)
      start = None

  data = json.dumps(data).encode()

  print("writing collected data")

  while wlist:
    _, wready, xready = select.select([], wlist, wlist)

    if xready:
      print("exception occurred")
      return

    for wo in wready:
      wo.sendall(data)
      wo.close()
      wlist.remove(wo)
  
  print("done")


def run_client(client_id):
  data = {"id": f"Liubchenko_{client_id}"}

  with socket.create_connection(address) as conn:
    conn.sendall(json.dumps(data).encode())
    data = json.loads(conn.recv(1024).decode())
    print(data)


def main():
  if len(sys.argv) > 1:
    run_client(sys.argv[1])
  else:
    run_server()


if __name__ == "__main__":
  main()
