import sqlite3
import os
import user
databaseName ="project.db"
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
        create table if not exists hospital (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name text not null                         
        );
        INSERT INTO hospital (id, name) VALUES (1,'Om Hospital'),
                          (2,'Grande Hospital'),
                          (3,'Man Mohan Hospital'),
                          (4,'Norvic Hospital'),
                          (5,'Bir Hospital');

        CREATE TABLE if not exists appointment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name text not null,
        age integer not null,
        address text,
        phonenumber integer,
        date integer,
        time integer,
        createdBy text not null,
        hospitalId integer not null,
                          
        FOREIGN KEY ('createdBy')  REFERENCES 'hospital'('username'),
        FOREIGN KEY ('hospitalId')  REFERENCES 'hospital'('id'));                  
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

def addAppointment(name,age,address,phonenumber,date,time,hospitalid,username):
    con= sqlite3.connect(databaseName)
    cur = con.cursor()   
    cur.execute("INSERT INTO appointment (name,age,address,phonenumber,date,time,hospitalId,createdBy) VALUES(?,?,?,?,?,?,?,?) ",[name,age,address,phonenumber,date,time,hospitalid,username]) 
    con.commit()
    con.close()

def updateAppointment(id, name,age,address,phonenumber,date,time):
    con= sqlite3.connect(databaseName)
    cur = con.cursor()   
    cur.execute("UPDATE  appointment SET name=?,age=?,address=?,phonenumber=?,date=?,time=? WHERE id = ?",[name,age,address,phonenumber,date,time,id]) 
    con.commit()
    con.close()

def deleteAppointment(id):
    con= sqlite3.connect(databaseName)
    cur = con.cursor()   
    cur.execute("DELETE FROM appointment WHERE id = ?",[id]) 
    con.commit()
    con.close()

   

def getAppointmentListForUser(hospitalId,username):
    con= sqlite3.connect(databaseName)
    cur = con.cursor()   
    cur.execute("SELECT * FROM appointment where hospitalId = ? and createdBy = ?",[hospitalId,username])
    data = cur.fetchall()
    con.close()
    return list(data)
    



def getAppointmentListForAdmin(hospitalId):
    con= sqlite3.connect(databaseName)
    cur = con.cursor()   
    cur.execute("SELECT * FROM appointment where hospitalId = ?",[hospitalId])
    data = cur.fetchall()
    con.close()
    return list(data)    



