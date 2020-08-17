from faker import Faker
import random
import time

import sqlite3
from numba import jit

con = sqlite3.connect('test3.db')
 
cursorObj = con.cursor()

def createDataBase():
    try:
        cursorObj.execute('''CREATE TABLE table1
                         ('SN'         TEXT    NOT NULL,
                         'id'         TEXT    NOT NULL,
                         'Name'         TEXT    NOT NULL,
                         'Birthday'         TEXT    NOT NULL,
                         'Gender'         TEXT    NOT NULL,
                         'Comment'         TEXT    NOT NULL,
                         'OcularParameters'         TEXT    NOT NULL,
                         'Physician'         TEXT    NOT NULL,
                         'Diagnosis'         TEXT    NOT NULL,
                         'Address'         TEXT    NOT NULL,
                         'PhoneNumber'         TEXT    NOT NULL,
                         'EMail'         TEXT    NOT NULL,
                         'NextVisit'         TEXT    NOT NULL,
                         'EMRID'         TEXT    NOT NULL);''')
        print("database created!")
    except:
        print("database already exist")

def generateFakeData( fakeDataNumber ):
    fake = Faker()
    gender = ["M","F"]
    data = []
    counter = 1
    for i in range( 1, fakeDataNumber ) :
        genderSeed = random.randint(0,1)

#         print("SN:", counter)
#         print("Id:", counter)
#         print("Name:", fake.name())
#         print("Birthday:",fake.date())
#         print("Gender:", gender[genderSeed])
#         print("Comment:",fake.text())
#         print("OcularParameters:",fake.word())
#         print("Physician:",fake.word())
#         print("Diagnosis:",fake.word())
#         print("Address:",fake.address())
#         print("PhoneNumber:", fake.phone_number())
#         print("EMail:", fake.email())
#         print("NextVisit:",fake.date())
#         print("EMRID:",fake.word())
        data.append([counter,counter,fake.name(),fake.date(),gender[genderSeed],fake.text(),fake.word(),fake.word(),fake.word(),fake.address(),fake.phone_number(),fake.email(),fake.date(),fake.word()])
        #print(data)
        counter+=1

    #print(data)

    q = """INSERT INTO table1(SN,id,Name,Birthday,Gender,Comment,OcularParameters,Physician,Diagnosis,Address,PhoneNumber,EMail,NextVisit,EMRID) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
    cursorObj.executemany(q,data)
    con.commit()    
    con.close()
    print("Fake Data generated!")

if __name__ == '__main__':
    tStart = time.time()
    createDataBase()
    fakeDataNumber = 100000
    generateFakeData( fakeDataNumber )
    tEnd = time.time()
    print("It takes ", round (tEnd - tStart, 2) , " seconds to generate ", fakeDataNumber, " fake data.")
    