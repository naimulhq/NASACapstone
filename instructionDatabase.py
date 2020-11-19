import sqlite3
import csv

class instructionDatabase:

    def __init__(self):
        self.conn = sqlite3.connect('instructions.db') # Create database connection
        self.cur = self.conn.cursor() # Cursor used to execute SQL statements
        self.createDB()

    def createDB(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS instructions(instruction text, stage text)""")

    def insertDB(self,instruction,stage):
        self.cur.execute("INSERT INTO instructions VALUES (?,?)",(instruction,stage))
        self.conn.commit()

    def printDB(self):
        self.cur.execute("SELECT * FROM instructions")
        print(self.cur.fetchall())

    def deleteAllData(self):
        self.cur.execute("DELETE FROM instructions")
        self.conn.commit()



# Create Database
instructionDB = instructionDatabase()
instructionDB.deleteAllData() # Delete Instruction Info

# Get info from csv
with open("/home/naimulhq/Capstone/instructions.csv",'r') as file:
    reader = csv.reader(file)
    data = list(reader)

# Store information into instruction database
for i in data:
    instructionDB.insertDB(i[0],i[1])


