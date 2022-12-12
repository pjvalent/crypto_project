import math 
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import zmq
import json

# miller rabin primality test
def miller_rabin(n, k):
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = rd.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# generate a random prime number
def generate_prime_number(n):
    while True:
        p = rd.randrange(2**(n-1), 2**n)
        if miller_rabin(p, 128):
            return p


def send_to_verifier(data, r, s):
  context = zmq.Context()

  # Socket to talk to server
  print("Connecting to server…")
  socket = context.socket(zmq.REQ)
  socket.connect("tcp://localhost:5555")

  print("Sending request …")
  socket.send(json.dumps(data).encode('utf-8'))

  message = json.loads(socket.recv())
  print("Received reply [ %s ]" % (message))

  if(message["alpha"] == 0):
    gamma = r
    socket.send(json.dumps({"gamma": gamma}).encode('utf-8'))
  else:
    gamma = r*s % data["n"]
    socket.send(json.dumps({"gamma": gamma}).encode('utf-8'))

  result = json.loads(socket.recv())
  print("Received reply [ %s ]" % (result))


def main():
  p = generate_prime_number(128)
  q = generate_prime_number(128)
  n = p*q

  s = rd.randint(math.sqrt(n), n)


  if(math.sqrt(n) > s or s > n):
    print("Error: secret number needs to be between sqrt(n) and n")
    return

  if(s == p or s == q):
    print("Error: this number is not available")
    return 

  v = s**2 % n

  r = rd.randint(1, n-1)

  x = (r**2) % n

  print("p = ", p)
  print("q = ", q)
  print("n = ", n)
  print("s = ", s)
  print("v = ", v)
  print("r = ", r)
  print("x = ", x)

  info = {"x": x, "v": v, "n": n}

  print("Sending info to verifier")
  send_to_verifier(info, r, s)
  

if __name__ == "__main__":
  main()
