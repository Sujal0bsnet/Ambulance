import sqlite3
import os
import user
databaseName ="CustomerSupport.db"
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
        
        CREATE TABLE if not exists customer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name text not null,
        address text,
        number integer,
        query integer,
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

def addcustomer(name,address,number,query,username):
    con= sqlite3.connect(databaseName)
    cur = con.cursor()   
    cur.execute("INSERT INTO customer (name,address,number,query,createdBy) VALUES(?,?,?,?,?) ",[name,address,number,query,username]) 
    con.commit()
    con.close()

def updatecustomer(id,name,address,number,query):
    con= sqlite3.connect(databaseName)
    cur = con.cursor()   
    cur.execute("UPDATE  customer SET name=?,address=?,number=?,query=? WHERE id = ?",[name,address,number,query,id]) 
    con.commit()
    con.close()


def deletecustomer(id):
    con= sqlite3.connect(databaseName)
    cur = con.cursor()   
    cur.execute("DELETE FROM customer WHERE id = ?",[id]) 
    con.commit()
    con.close()

   

def getcustomerListForUser(username):
    con= sqlite3.connect(databaseName)
    cur = con.cursor()   
    cur.execute("SELECT * FROM customer where createdBy = ?", [username])
    data = cur.fetchall()
    con.close()
    return list(data)
    



def getcustomerListForAdmin():
    con= sqlite3.connect(databaseName)
    cur = con.cursor()   
    cur.execute("SELECT * FROM customer")
    data = cur.fetchall()
    con.close()
    return list(data)    



