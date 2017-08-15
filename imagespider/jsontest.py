# -*- coding: utf-8 -*-
import json
f = open("/Users/apple/Desktop/log.json",'r')
jsonArray = json.load(f)

if __name__ == '__main__':
    for obj in  jsonArray:
        print obj