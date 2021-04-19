import sqlite3
import csv

class instructionDatabase:

    def __init__(self):
        self.conn = sqlite3.connect('instructions.db') # Create database connection
        self.cur = self.conn.cursor() # Cursor used to execute SQL statements
        self.createDB()
        self.cur.execute("SELECT * FROM instructions")
        self.databaseList = self.cur.fetchall()
        self.count = 0
        self.size = len(self.databaseList)

    def createDB(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS instructions(instruction text, stage text)""")
    
    def updateSizeandArray(self):
        self.cur.execute("SELECT * FROM instructions")
        self.databaseList = self.cur.fetchall()
        self.size = len(self.databaseList)

    def insertDB(self,instruction,stage):
        self.cur.execute("INSERT INTO instructions VALUES (?,?)",(instruction,stage))
        self.conn.commit()
        self.updateSizeandArray()

    def getInstruction(self):
        if(self.count >= self.size):
            print("End of Database.")
            return True, ""
        else:
            value = self.databaseList[self.count]
            self.count += 1
            return False,value

    def printDB(self):
        print(self.databaseList)

    def deleteAllData(self):
        self.cur.execute("DELETE FROM instructions")
        self.conn.commit()



