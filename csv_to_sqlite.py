import sqlite3
import csv
import time
import pandas as pd 
import numpy as np

conn = sqlite3.connect('social_media.db', isolation_level = None)

cur = conn.cursor()

file = open('users.csv')
contents = csv.reader(file)
userData = pd.read_csv('users.csv')
userData.to_sql('users', conn, if_exists='replace', index = True, index_label = 'number')
file.close()
file = open('followers.csv')
contents = csv.reader(file)
followers = pd.read_csv('followers.csv')
followers.to_sql('followers', conn, if_exists='replace', index = True, index_label = 'number')
file.close()
file = open('posts.csv')
contents = csv.reader(file)
posts = pd.read_csv('posts.csv')
posts.to_sql('posts', conn, if_exists='replace', index = True, index_label = 'number')
file.close()
