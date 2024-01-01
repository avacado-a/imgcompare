import requests
def newkey():
  x = requests.get(f'https://data.sparik7633.repl.co/newkey/')
  if x.status_code != 200:
    raise Exception("FreeDB is down or has an unsolvable error and is unable to be contacted")
  resp = eval(x.text)
  return resp["response"] if "response" in list(resp) else Exception(resp["error"])
def post(key,value):
  x = requests.get(f'https://data.sparik7633.repl.co/post/{key}/{value}/')
  if x.status_code != 200:
    raise Exception("FreeDB is down or has an unsolvable error and is unable to be contacted")
  resp = eval(x.text)
  if not "response" in list(resp):
    raise Exception(str(resp["error"]))
  else:
    return resp["response"]
def get(key):
  x = requests.get(f'https://data.sparik7633.repl.co/get/{key}/')
  if x.status_code != 200:
    raise Exception("FreeDB is down or has an unsolvable error and is unable to be contacted")
  resp = eval(x.text)
  if not "response" in list(resp):
    raise Exception(str(resp["error"]))
  else:
    return resp["response"]
def delete(key):
  x = requests.get(f'https://data.sparik7633.repl.co/delete/{key}/')
  if x.status_code != 200:
    raise Exception("FreeDB is down or has an unsolvable error and is unable to be contacted")
  resp = eval(x.text)
  if not "response" in list(resp):
    raise Exception(str(resp["error"]))
  else:
    return "Deleted"