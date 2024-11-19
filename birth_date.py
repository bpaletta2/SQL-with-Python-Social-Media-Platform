import sqlite3
import csv
import time
import pandas as pd 
import numpy as np

conn = sqlite3.connect('social_media.db', isolation_level = None)

cur = conn.cursor()

check = False

try:
    cur.execute("ALTER TABLE users ADD birth_date TEXT")
except sqlite3.OperationalError:
    print("Birth date column already exists")
    

dates = ['10/18/1999', '8/19/1998', '9/29/2001', '11/26/1995', '10/22/2002', '12/22/1999', '10/5/2000', '1/3/2003']
ids = ['1', '2', '3', '4', '5', '6', '7', '8']
count = 1
#with open("birth_dates.csv", "r") as file:
#    for line in file:
#        currentline = line.split(",")

cur.execute('DELETE FROM users WHERE user_id = ""')


s = 'UPDATE users SET birth_date = ?'
for i in range(8):
    s = "UPDATE users SET birth_date = '" + dates[i] + "' WHERE user_id = '" + ids[i] +"'"
    cur.execute(s)

conn.close()
