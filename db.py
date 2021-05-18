import os
import sqlite3

conn = sqlite3.connect('multitask.db')
cursor = conn.cursor()

def Create_database():                                                                            
    with open("createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()

def Join(user_id, name):
    cursor.execute(f'INSERT OR IGNORE INTO Users VALUES({user_id}, "{name}")')
    print(f'user start bot|| name: {name}; id: {user_id}')
    conn.commit()

def Verification(user_id):
    cursor.execute(f'SELECT user_id FROM Users WHERE user_id={user_id}')
    response = cursor.fetchall()
    conn.commit()
    if not response:
        return False
    else:
        return True

def Get_WeeklyAffairs(user_id, day, time, text):
    cursor.execute(f'INSERT INTO Affairs VALUES({user_id}, {day}, {time}, "{text}")')
    conn.commit()

def Get_Affair(user_id, date, time, text):
    cursor.execute(f'INSERT INTO Affairs VALUES({user_id}, {date}, {time}, "{text}")')
    conn.commit()

def Get_QuickAffair(user_id, timer, text):
    cursor.execute(f'INSERT INTO Affairs VALUES({user_id}, {timer}, "{text}")')
    conn.commit()
