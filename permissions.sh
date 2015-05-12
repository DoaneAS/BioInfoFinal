#!/bin/bash
export SRC_DIR=$(cd ..; pwd)

chmod 777 cgi-bin/*
setfacl -m m:rwx ~/final/images/
setfacl -m u:apache:rwx ~/final/images/