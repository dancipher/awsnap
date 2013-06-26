#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os

from sh import llvm_objdump

def main():
  files = os.listdir('binaries')
  for f in files:
    text = llvm_objdump("-section-headers", "binaries/" + f)
    for line in text:
      line = line.rstrip()
      if "__cstring" in line:
	line = line.split(" 0000000")[1]
	addr = "0000000%s" %line 
	print("Addr: %s" %addr)
	   
if __name__ == "__main__":
  main()
