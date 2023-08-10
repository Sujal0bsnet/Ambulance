import sqlite3
import os
import user
databaseName ="firstaid.db"
def createTable():
    con= sqlite3.connect(databaseName)
    cur = con.cursor()
    try:
        cur.executescript('''
        CREATE TABLE if not exists user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username text not null,
        password text not null,
        isAdmin int not null default 0 );
        INSERT INTO user (username, password,isAdmin) VALUES ('admin','admin',1);
        
        CREATE TABLE if not exists booking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name text not null,
        address text,
        number integer,
        quantity integer,
        createdBy text not null                  
        );                  
        ''')
        con.commit()
        con.close()

    except sqlite3.Error as ex:
        
        cur.close()
        con.close()
        os.remove(databaseName)
    except:
        
        cur.close()
        con.close()
        os.remove(databaseName)
    

def createDatabaseIfNotExists():
    if(os.path.exists(databaseName)):
        pass    
    else :
        createTable()

createDatabaseIfNotExists()        


def createUser(username, password):
    if(len(username.strip())==0 or len(password.strip())==0):
        raise Exception("Username or passowrd cannot be empty")
    con= sqlite3.connect(databaseName)
    cur = con.cursor()   
    cur.execute("SELECT id From user WHERE username = ? LIMIT 1",[username]) 
    
    isAlreadyExist=cur.fetchone()
    if(isAlreadyExist is not None):
        raise Exception("Username already exists")
    cur.execute("INSERT INTO user (username,password) VALUES (?,?)",[username,password])
    con.commit()
    con.close()

def loginUser(username,password):    
    con= sqlite3.connect(databaseName)
    cur = con.cursor()   
    cur.execute("SELECT username,isAdmin From user WHERE username = ? and password=? LIMIT 1",[username,password]) 
    userData=cur.fetchone()
    if(userData is None):
        raise Exception("Username or password if not correct")
    user.username=tuple(userData)[0]
    user.isAdmin=tuple(userData)[1]
    con.close()
    return userData

def addbooking(name,address,number,quantity,username):
    con= sqlite3.connect(databaseName)
    cur = con.cursor()   
    cur.execute("INSERT INTO booking (name,address,number,quantity,createdBy) VALUES(?,?,?,?,?) ",[name,address,number,quantity,username]) 
    con.commit()
    con.close()

def updatebooking(id,name,address,number,quantity):
    con= sqlite3.connect(databaseName)
    cur = con.cursor()   
    cur.execute("UPDATE  booking SET name=?,address=?,number=?,quantity=? WHERE id = ?",[name,address,number,quantity,id]) 
    con.commit()
    con.close()


def deletebooking(id):
    con= sqlite3.connect(databaseName)
    cur = con.cursor()   
    cur.execute("DELETE FROM booking WHERE id = ?",[id]) 
    con.commit()
    con.close()

   

def getbookingListForUser(username):
    con= sqlite3.connect(databaseName)
    cur = con.cursor()   
    cur.execute("SELECT * FROM booking where createdBy = ?", [username])
    data = cur.fetchall()
    con.close()
    return list(data)
    



def getbookingListForAdmin():
    con= sqlite3.connect(databaseName)
    cur = con.cursor()   
    cur.execute("SELECT * FROM booking")
    data = cur.fetchall()
    con.close()
    return list(data)    



