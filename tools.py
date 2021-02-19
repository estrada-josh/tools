
#This file contains lines of code to accomplish tasks in a program
#Feel free to copy and paste these as needed.

#By Joshua Estrada

#############################################################

#reads file and sets up a dictionary and creates histogram
#file has to be in the same folder as the python file

#asks for a file name to be entered
name = input('Enter file: ')
#if the length of the file name is less that 1 character,
#set as a default file name
if len(name) < 1 : name = 'mbox-short.txt'
#creates a connection to the file named handle
handle = open(name)

#sets an empty dictionary
#dictionaries are like tables with 2 columns; name and value
counts = dict()

#reads through file line by line
for line in handle:
    #if the line doesnt start with "From: " we skip the line
    if not line.startswith("From: ") :
        continue
    #splits each line into words and makes a list of words in each lines
    #stored in the variable "words"
    words = line.split()
    #grabs words in 2nd and 3rd position in list of words
    email = words[1:2]
    #creates the histogram
    for word in email:
        counts[word] = counts.get(word,0) + 1

###############################################################

#reads through a file and creates a list of integers out of
#the numbers in the file

#create an emtmty list named allnumbers
allnumbers = list()
for line in handle:
    read = line.strip()
    #finds all digits and stores them in numbers
    numbers = map(int,re.findall('[0-9]+',read))
    #adds whatever is in numbers to the empty list
    for allnumber in numbers:
        allnumbers.append(allnumber)

#############################################################

# Sort_values is a list of sorted value from the counts dict
sorted_values = sorted(counts.values())
#sorted_dict is an empty dictionary
sorted_dict = {}

for value in sorted_values:
    for keys in counts.keys():
        if counts[keys] == value:
            sorted_dict[keys] = counts[keys]
            #print(value, keys)
            break


###############################################################

#Socket connection and HTTP Request

import socket

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect(('data.pr4e.org', 80))
cmd = 'GET http://data.pr4e.org/romeo.txt HTTP/1.0\r\n\r\n'.encode()
mysock.send(cmd)

while True:
    data = mysock.recv(512)
    if (len(data) < 1):
        break
    print(data.decode())
mysock.close()

###### Simplified using urllib ######

import urllib.request, urllib.parse, urllib.error

fhand = urllib.request.urlopen('URL')
for line in fhand:
    print(line.decode().strip())

################################################################

#Creates an HTML parser and pulls out all anchor tags and
#href links

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter - ')
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

tags = soup('a')
for tag in tags:
    print(tag.get('href', None))

###############################################################

#importing xml element tree

import xml.etree.ElementTree as ET

################################################################

# Find pieces of information in a JSON file and put it into a list

import json
import urllib.request, urllib.parse, urllib.error


url = input('Enter URL: ')
if len(url) < 1 : url = 'http://py4e-data.dr-chuck.net/comments_1089692.json'

urlhandle = urllib.request.urlopen(url)
data = urlhandle.read().decode()

js = json.loads(data)

#prints json in terminal in neat format
#print(json.dumps(js, indent=4))

#makes list
newlist = list()

for numbers in js['comments']:
    for count in numbers :
        count = numbers['count']
    newlist.append(count)

###################################################################


#Error message display if JSON cannot be retreived

try:
    js = json.loads(data)
except:
    js = None

if not js or 'status' not in js or js['status'] != 'OK':
    print('==== Failure To Retrieve ====')
    print(data)
    continue

###########################################################

# Accessing and Parsing an API JSON file

import json
import urllib.request, urllib.parse, urllib.error
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

api_key = '42'
serviceurl = 'http://py4e-data.dr-chuck.net/json?'
address = input('Enter place: ')
if len(address) < 1 : address = 'Zagazig University'

endofurl = {'address' : address , 'key' : api_key}

url = serviceurl + urllib.parse.urlencode(endofurl)

urlhandle = urllib.request.urlopen(url)
data = urlhandle.read().decode()

js = json.loads(data)
#shows json in nice format
#print(json.dumps(js, indent=4))

###########################################################

# Finds specific strings in a text file and makes a Database with them

import sqlite3
import urllib.request, urllib.parse, urllib.error
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#Creates a file in sqlite and connects to it
conn = sqlite3.connect('orgdb.sqlite')
#allows python to execute SQL commands in sqlite
cur = conn.cursor()

#Deletes table if it already exists in the file
cur.execute('DROP TABLE IF EXISTS Counts')
#Creates table with 2 columns
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

name = input('enter file name: ')
if len(name) < 1 : name = 'mbox.txt'
handle = open(name)

for line in handle:
    if not line.startswith("From ") :
        continue
    pieces = line.split()
    email = pieces[1]
    orgpos = email.find('@')
    org = email[orgpos + 1:]

    #Selects the column that we are going to be changing
    cur.execute('SELECT count FROM Counts WHERE org = ?', (org,))
    #Checks if it has reached the end of the database
    row = cur.fetchone()
    if row is None: #if there is no rows, it creates a new row starting at a count of 1
        cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (org,))
    else: #if there is a existing row then add 1 to the count column
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (org,))
    #sends info to sqlite
    conn.commit()


########################################################################

#the following code reads an xml file and creates a SQLlite db out of it

import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')


fname = input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'Library.xml'

# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>
def lookup(d, key):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None

stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict')
print('Dict count:', len(all))
for entry in all:
    if ( lookup(entry, 'Track ID') is None ) : continue

    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')
    genre = lookup(entry, 'Genre')

    if name is None or artist is None or album is None or genre is None :
        continue

    print(name, artist, album, count, rating, length, genre)

    cur.execute('''INSERT OR IGNORE INTO Artist (name)
        VALUES ( ? )''', ( artist, ) )
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
    artist_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Genre (name)
        VALUES ( ? )''', ( genre, ) )
    cur.execute('SELECT id FROM Genre WHERE name = ? ', (genre, ))
    genre_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id)
        VALUES ( ?, ? )''', ( album, artist_id ) )
    cur.execute('SELECT id FROM Album WHERE title = ? ', (album, ))
    album_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, len, rating, count, genre_id)
        VALUES ( ?, ?, ?, ?, ?, ? )''',
        ( name, album_id, length, rating, count, genre_id ) )

    conn.commit()

######################


#PULLING STOCK DATA FROM YAHOO

import datetime as dt
from datetime import date
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

start = dt.datetime(2000,1,1)
today = date.today()

#Style for plotting dataframes
style.use('ggplot')

df = web.DataReader('AMD', 'yahoo', start, today)

df = pd.read_csv('amd.csv', parse_dates = True, index_col=0)

#create extra columns
df['50ma'] = df['Adj Close'].rolling(window=50).mean()
df['100ma'] = df['Adj Close'].rolling(window=100).mean()
df['200ma'] = df['Adj Close'].rolling(window=200).mean()

df = df.tail()
df.datetimeIndex(dayfirst)


print(df[['Volume','Adj Close','50ma']] [df['Adj Close'] >= df['50ma']])

print(df)
########

#GRAPHING STOCK DATA~

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

#start = dt.datetime(2000,1,1)
#end = dt.datetime(2020,12,31)

#df = web.DataReader('TSLA', 'yahoo', start, end)
#df.to_csv('tsla.csv')
df = pd.read_csv('tsla.csv', parse_dates = True, index_col=0)

df['100ma'] = df['Adj Close'].rolling(window=100).mean()

print(df.tail())
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

ax1.plot(df.index,df['Adj Close'])
ax1.plot(df.index,df['100ma'])
ax2.bar(df.index,df['Volume'])

plt.show()
##########

#Compares 50ma to Adj Close and counts how many are higher and lower

import pandas as pd
from datetime import date
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

#yahoo finance workaround
yf.pdr_override()

#stock to read
stock = input("Enter a stock ticker symbol: ")
if len(stock) < 1 : stock = "AMD"

#start and end of info gathering
start = dt.datetime(2000,1,1)
end = date.today()

#create data frame with stock info
df = pdr.get_data_yahoo(stock,start,end)

#create new column for
ma = 50
ma_str = str(ma) + "ma"
df[ma_str] = df['Adj Close'].rolling(window=ma).mean()

#setting variables for counting below
hc = 0
lc = 0
c = 0

#Look through each item in index column and their values
for i in df.index:
    c = c + 1
    adj_close_values = (df['Adj Close'][i])
    ma_values = (df[ma_str][i])

    #compare two columns values and count each
    if adj_close_values > ma_values:
        hc = hc + 1
    else:
        lc = lc + 1

#print the counts
print(hc, lc, c)

############

# CREATE A DATAFRAME FROM YAHOO FINANCE FOR SINGLE TICKER AND CALCULATE RSI

import pandas as pd, shutil, os, time, glob
from datetime import date
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
import requests
from statistics import mean

#yahoo finance workaround
yf.pdr_override()

#stock to read
stock = input("Enter a stock ticker symbol: ")
if len(stock) < 1 : stock = "AMD"

#start and end of info gathering
start = dt.datetime(2000,1,1)
end = date.today()

#create data frame with stock info
df = round(pdr.get_data_yahoo(stock,start,end),3)

################

#Calculating RSI

#create column that tracks difference in price over each day and creates new up or down colums
# dont need to create columns for this. But they are useful to visualize the values and check work
# df['Delta'], df['Up'], df['Down']
delta = df.iloc[:,4].diff()
up = delta.clip(lower=0)
down = -1 * delta.clip(upper=0)

#variables that contain average value over 14 days of differences in price per day
ema_up = up.ewm(com=13, adjust=False).mean()
ema_down = down.ewm(com=13, adjust=False).mean()

#RSI formula and put it in a new RSI column in the dataframe
rs = ema_up/ema_down
df['RSI'] = 100 - (100/(1 + rs))
################

#list of numbers to use for ema periods
ema_used = [3,5,8,10,12,15,30,35,40,45,50,60]

#creates new column for each ema period in the above list
for per in ema_used:
    ema_str = str(per) + 'EMA'
    df[ema_str] = round(df.iloc[:,4].ewm(span=per, adjust=False).mean(),3)

#looking up value for each column and checking the lowest ema value and the highest ema value
# for i in df.index:
#     crit_min = min(df['3EMA'][i],df['5EMA'][i],df['8EMA'][i],df['10EMA'][i],df['12EMA'][i],df['15EMA'][i])
#     crit_max = max(df['30EMA'][i],df['35EMA'][i],df['40EMA'][i],df['45EMA'][i],df['50EMA'][i],df['60EMA'][i])
#     close = df['Adj Close'][i]

    #if the previous adjusted close is lower than the next adjusted close
print(df.tail())

###########################
