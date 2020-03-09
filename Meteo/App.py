# coding: utf-8
import json
import serial
import time
import pymongo

if __name__ == '__main__':
  print("---App_MAIN---")
  baseName="Agriculture"
  colName="dht"
  client=pymongo.MongoClient()
  dbTest=client[baseName][colName]
  ser = serial.Serial(port='COM3',baudrate=57600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
  while 1:
    x = ser.readline()
    if x:
      x = x.rstrip()
      x = x.decode(encoding="utf-8",errors='ignore')
      dht=json.loads(x)
      print(dht,type(dht))
      dbTest.insert_one(dht)
    time.sleep(5)