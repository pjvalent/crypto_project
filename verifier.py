import random as rd
import math
import zmq
import time 
import json


def main():
  context = zmq.Context() 
  socket = context.socket(zmq.REP)
  socket.bind("tcp://*:5555")

  while True:
    message = json.loads(socket.recv())
    print("Received request: %s" % message)
    print("Type of message: ", type(message))

    alpha = rd.randint(0,1)
    msg2 = {"alpha": alpha}

    time.sleep(1)
    socket.send(json.dumps(msg2).encode('utf-8'))

    print("Waiting for response message from prover")
    msg3 = json.loads(socket.recv())

    print(msg3)
    gamma_sqr = msg3["gamma"]**2 % message["n"]

    check = message["x"] * message["v"]**alpha % message["n"]

    if(gamma_sqr == check):
      print("The proof is correct")
      socket.send(json.dumps({"result": True}).encode('utf-8'))
    
    else:
      print("The proof is incorrect")
      socket.send(json.dumps({"result": False}).encode('utf-8'))



if __name__ == "__main__":
  main()