#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# 2013 zulla@zulla.org
# All rights reversed. ;)

import json
import os

from sh import llvm_objdump

projects = {}
default_payload = "-0.00001"

def shift_zeros(s):
  """
  Parse and shift memory addresses of the 
  __TEXT.__cstring section of the Mach-O binary 
 
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
  Read the pre-parsed functions and generate the
  Javascript. Extraction of these functions should
  happen automatically here, ftw

  @@FIXME 
 
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
  Function for beauty 
 
  """
  global projects

  projects[name] = dataset

def read_binaries():
  """
  Get the memory addresses of __TEXT.__cstrings
  out of the binary 
 
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

