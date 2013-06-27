#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import json
import os

from sh import llvm_objdump

projects = {}
default_payload = "-0.00001"

def shift_zeros(s):
  """
  @author: Daniel Zulla (zulla@mit.edu)
  
  """

  s = list(s)
  if len(s) > 2 and s[0] == '0' and s[1] == '0':
    s = shift_zeros(s[2:])
  elif len(s) >= 2 and s[0] == '0' and s[1] != '0':
    s = shift_zeros(s[1:])
  else:
    s = "".join(s)
  return s

def read_functions():
  """
  @author: Daniel Zulla (zulla@mit.edu)
  
  """

  global projects, default_payload

  for k, v in projects.items():
    print(k)
    functions = open("lst/%s.lst" %k, "r").read().split("\n")
    payloads = []
    for func in functions:
      payloads.append("this.plugin.%s('%s')" %(func, default_payload))
      payloads.append("this.plugin.%s(%s)" %(func, default_payload))
    print(json.dumps(payloads, indent=2))

def add_new_project(name, dataset):
  """
  @author: Daniel Zulla (zulla@mit.edu)
  
  """
  global projects

  projects[name] = dataset

def read_binaries():
  """
  @author: Daniel Zulla (zulla@mit.edu)
  
  """

  global projects

  files = os.listdir('binaries')
  for name in files:
    text = llvm_objdump("-section-headers", "binaries/%s" %name)
    words = filter(lambda x: x, [filter(lambda x: x, [word.rstrip().encode("utf-8") for word in line.rstrip().split(" ")])[1:] for line in text])
    for word in words:
      if word[0] == '__cstring':
	add_new_project(name, [shift_zeros(x) for x in word[1:]])

def main():
  read_binaries()
  read_functions()

if __name__ == "__main__":
  main()

