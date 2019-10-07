import re
import sys
import sqlite3
from collections import Counter
from string import punctuation
from math import sqrt

#initialize the connection to the database
#Creating a connection object
connection = sqlite3.connect('hackpath2.db')
#cursors are used to execute sql commands
cursor = connection.cursor()
import subprocess
import os
create_table_request_list = [
    'CREATE TABLE words(word TEXT UNIQUE)',
    'CREATE TABLE sentences(sentence TEXT UNIQUE, used INT NOT NULL DEFAULT 0)',
    'CREATE TABLE associations (word_id INT NOT NULL, sentence_id INT NOT NULL, weight REAL NOT NULL)',
]
for create_table_request in create_table_request_list:
    try:
        cursor.execute(create_table_request)
    except:
        pass

def get_id(entityName, text):
    """Retrieve an entity's unique ID from the database, given its associated text.
    If the row is not already present, it is inserted.
    The entity can either be a sentence or a word."""
    tableName = entityName + 's'
    columnName = entityName
    cursor.execute('SELECT rowid FROM ' + tableName + ' WHERE ' + columnName + ' = ?', (text,))
    
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        cursor.execute('INSERT INTO ' + tableName + ' (' + columnName + ') VALUES (?)', (text,))
        #cursor.lastrowid will return the id of the previous row by auto_increment method
        return cursor.lastrowid

def get_words(text):
    """Retrieve the words present in a given string of text.
    The return value is a list of tuples where the first member is a lowercase word,
    and the second member the number of time it is present in the text."""
    wordsRegexpString = '(?:\w+|[' + re.escape(punctuation) + ']+)'
    #Return string with all non-alphanumerics backslashed;
    #this is useful if you want to match an arbitrary literal string that may have regular expression metacharacters in it.
    wordsRegexp = re.compile(wordsRegexpString)
    wordsList = wordsRegexp.findall(text.lower())
    return Counter(wordsList).items()

B = 'Hello!'
print('B: ' + B)
H = input('H: ').strip()
B='We provide services like new making a new appointment, checking doctor availability and bill generation. Which service would you like to avail? '
while True:
    # output bot's message
    print('B: ' + B)
    # ask for user input; if blank line, exit the loop
    H = input('H: ').strip()
    if H == '':
        break
    elif H == 'Thanks for the services provided':  
    	break
    elif H == 'Bye':  
    	break	  
    elif 'register' in H:
    	cmd = 'python3 appointment.py'
    	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)  
    elif 'registration' in H:
    	cmd = 'python3 appointment.py'
    	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True) 
    elif 'registering' in H:
    	cmd = 'python3 appointment.py'
    	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True) 
    elif 'doctor availability' in H:
    	cmd = 'python3 doctoravailability.py'
    	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)  	 	 
    elif H=='When is the doctor availability':
    	cmd = 'python3 doctoravailability.py'
    	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)   
    elif 'bill amount' in H:
    	cmd = 'python3 fees.py'
    	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    elif 'bill amount ' in H:
    	cmd = 'python3 fees.py'
    	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)	  
    elif 'bill' in H:
    	cmd = 'python3 fees.py'
    	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)	 		
    print('B: ' + "Would you like to continue?")
    H = input('H: ').strip()
    if H=='Y':
    	continue
    elif H=='y':
    	continue
    # store the association between the bot's message words and the user's response
    words = get_words(B)
    words_length = sum([n * len(word) for word, n in words])
    sentence_id = get_id('sentence', H)
    for word, n in words:
        word_id = get_id('word', word)
        weight = sqrt(n / float(words_length))
        cursor.execute('INSERT INTO associations VALUES (?, ?, ?)', (word_id, sentence_id, weight))
    connection.commit()
    # retrieve the most likely answer from the database
    cursor.execute('CREATE TEMPORARY TABLE results(sentence_id INT, sentence TEXT, weight REAL)')
    words = get_words(H)
    words_length = sum([n * len(word) for word, n in words])
    for word, n in words:
        weight = sqrt(n / float(words_length))
        cursor.execute(
            'INSERT INTO results SELECT associations.sentence_id, sentences.sentence, ?*associations.weight/(4+sentences.used) FROM words INNER JOIN associations ON associations.word_id=words.rowid INNER JOIN sentences ON sentences.rowid=associations.sentence_id WHERE words.word=?',
            (weight, word,))
    # if matches were found, give the best one
    cursor.execute(
        'SELECT sentence_id, sentence, SUM(weight) AS sum_weight FROM results GROUP BY sentence_id ORDER BY sum_weight DESC LIMIT 1')
    row = cursor.fetchone()
    cursor.execute('DROP TABLE results')
    # otherwise, just randomly pick one of the least used sentences
    if row is None:
        cursor.execute(
            'SELECT rowid, sentence FROM sentences WHERE used = (SELECT MIN(used) FROM sentences) ORDER BY RANDOM() LIMIT 1')
        row = cursor.fetchone()
    # tell the database the sentence has been used once more, and prepare the sentence
    B = row[1]
    cursor.execute('UPDATE sentences SET used=used+1 WHERE rowid=?', (row[0],))
    		
    		
