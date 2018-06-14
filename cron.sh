#!/bin/sh
git pull
go run list2md.py
git commit -m "Auto update" -a
git push origin
