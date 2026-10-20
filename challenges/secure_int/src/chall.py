#!/usr/bin/env python3

FLAG = open('flag.txt').read()

class SecureInt:
  """
  Integers, but with constant-time equality check !
  Use them in all your crypto CTFs
  """
  def __init__(self, val):
    self.val = val

  def __hash__(self):
    return hash(self.val)

  def __eq__(self, other):
    return hash(self.val) == hash(other.val)


users = {
    SecureInt(1): {"name": "bob", "admin": True},
    SecureInt(2): {"name": "joe", "admin": False}
}

user_id = int(input("Enter your user ID: "))
if user_id == 1:
    print("I don't believe you!")
    exit()

user_id = SecureInt(user_id)
if user_id in users:
  print(f'Hello {users[user_id]["name"]}!')
  if users[user_id]["admin"]:
    print(FLAG)
else:
  print("User unknown...")