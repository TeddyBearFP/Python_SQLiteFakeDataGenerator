Python generate fake data for testing database syntax efficiency
===
    
date: 2020-02-14 12:05:16
---

# Python 產出假資料來測試資料庫語法的效率

## 前言
有時候我們需要一些測試資料，例如:要測試資料庫語法是否夠快速，那麼我們可以先寫一個 FakeDataGenerator 來產生包含 ( 名字、性別、生日、到訪日、地址、EMail、備註文字 ) 的測試資料

## fake2db
這邊我們使用的是 Python 有人提供的 fake2db 函式庫可以得到許多隨機特定格式資料。

### 安裝 fake2db
老樣子用 pip 安裝一下 fake2db
```python=
pip3 install fake2db
```

### 使用 fake2db
每次取得 faker 的函式回傳值皆會是函式隨機產生後回傳的每次不一樣

```python
from faker import Faker

fake = Faker()
print("Name:", fake.name())
print("date:",fake.date())
print("thisYearDate:",fake.date_time_this_year())
print("Comment:",fake.text())
print("word:",fake.word())
print("Address:",fake.address())
print("PhoneNumber:", fake.phone_number())
print("EMail:", fake.email())

#輸出結果如下
Name: Christine Kelley
date: 2006-12-24
thisYearDate: 2020-02-02 03:12:26
Comment: Illo fugiat non laudantium libero deleniti consequatur facere. Et esse voluptas dicta. Recusandae ducimus quos earum nesciunt. Similique autem inventore quisquam minus excepturi sint.
word: repellendus
Address: 61905 Linda Lodge
Lake Reginamouth, GA 71925
PhoneNumber: 00118138799
EMail: mbaxter@yahoo.com
```

利用以上特性讓我們來做測試資料吧


## FakeDataGenerator 實作
用 faker 函式創建假的會員資料

fakeDataNumber 填入欲產出的假資料數量
```python
from faker import Faker
import random
import time

import sqlite3

con = sqlite3.connect('member.db')
cursorObj = con.cursor()

def createDatabase():
    try:
        cursorObj.execute('''CREATE TABLE member
                         ('SN'         TEXT    NOT NULL,
                         'Name'        TEXT    NOT NULL,
                         'Gender'      TEXT    NOT NULL,
                         'Birthday'    TEXT    NOT NULL,
                         'Address'     TEXT    NOT NULL,
                         'PhoneNumber' TEXT    NOT NULL,
                         'EMail'       TEXT    NOT NULL,
                         'Comment'     TEXT    NOT NULL);''')
        print("member table created!")
    except:
        print("member table already exists.")

def generateFakeData( fakeDataNumber ):
    fake = Faker()
    data = []
    sn = 1
    gender = ["M", "F"]
    for i in range( 1, fakeDataNumber ) :
        if(sn%10000 == 0):
            print(sn)
        genderSeed = random.randint(0,1)
        data.append([sn,fake.name(),gender[genderSeed],fake.date(),fake.address(),fake.phone_number(),fake.email(),fake.text()])
        sn+=1

    q = """INSERT INTO member(SN,Name,Gender,Birthday,Address,PhoneNumber,EMail,Comment) VALUES(?,?,?,?,?,?,?,?)"""
    cursorObj.executemany(q,data)
    con.commit()  
    con.close()
    print("Fake Data generated!")

if __name__ == '__main__':
    tStart = time.time()
    createDatabase()
    fakeDataNumber = 1000
    generateFakeData( fakeDataNumber )
    tEnd = time.time()
    print("It takes ", round (tEnd - tStart, 2) , " seconds to generate ", fakeDataNumber, " fake data.")
```

執行結果
```
member table already exists.
Fake Data generated!
It takes  4.9  seconds to generate  1000  fake data.
```

![](https://i.imgur.com/kbYTaC6.png)

## 備註
1. 目前使用上來說 fake.date() 有機會在 faker 函式庫本身內部出錯 ( return 發生錯誤 )導致程式終止 OSError
2. fake.text() 因回傳的字串字數多，速度比較慢，會導致在大量產出時速度很慢，若只要一些 Text 的話，可以用 fake.word() 加減用


