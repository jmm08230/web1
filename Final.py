# -*- coding: utf-8 -*-
import MySQLdb #코드 작성에 필요한 라이브러리 삽입
import requests
from bs4 import BeautifulSoup
import sys
import os
import hashlib
import pymysql

if __name__ == "__main__": 
    
    
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    #크롤링 할 주소로 접속할 때 사용하는 header에 대해서 작성
    req = requests.get('http://softproj.xn--h32bi4v.xn--3e0b707e/',
                       headers=header)
    #데이터를 크롤링할 주소
    html = req.text
    parse = BeautifulSoup(html, 'html.parser')
    
    hashvalues = parse.find_all("div", {"class": "hash_info"}) #웹 페이지의 구성 중 div  태그에서도 class가 hash_info로 구성된 데이터들을 hashvalues에 저장
    sizes = parse.find_all("div", {"class": "hash_info"}) #웹 페이지의 구성 중 div 태그에서도 class가 hash_info로 구성 된 데이터들을 sizes에 저장 
    
    hashvalue = [] #hashvalue의 값을 담을 배열
    size = [] #size의 값을 담을 배
    
    for h in hashvalues:
        hashvalue.append(h.find('div', {"class": "md5"}).text) #웹 페이지의 구성 중에서도 div 태그 중 class가 md5인 데이터들의 text만 골라서 저장

    for s in sizes:
        size.append(s.find('div', {"class": "volume"}).text) #웹 페이지의 구성 중에서도 div 태그 중 class가 volume인 데이터들의 text만 골라서 저장
    items = [item for item in zip(hashvalue, size)]
    
conn = MySQLdb.connect( #MySQL에 JMS user로 접속
    user="JMS",
    passwd="1234",
    host="localhost",
    db="MD5"
    )

cursor = conn.cursor() #cursor 객체 생성
cursor.execute("DROP TABLE IF EXISTS Team13") 

cursor.execute("CREATE TABLE Team13 (`virus` int, hashvalue text, size int)") #cursor를 통해서 위에서 작성한 sql문 실행

i=1

for item in items:
    cursor.execute(
        f"INSERT INTO Team13 VALUES({i},\"{item[0]}\",\"{item[1]}\")") #테이블에 크롤링한 값 추가
    i += 1

conn.commit() #sql 변경내용 저장

conn.close() #sql과의 연결 끊기

con = pymysql.connect( #MySQL에 JMS user로 접속
    host='localhost',
    user='JMS',
    password='1234',
    db='MD5',
    charset='utf8'
    )

cur=con.cursor() #cursor를 통해서 데이터 베이스의 정보를 rows에 저장

sql="SELECT * FROM Team13" #실행할 sql문 작성
cur.execute(sql) #cursor를 통해서 위에서 작성한 sql문 실행

rows = cur.fetchall() #cursor를 통해서 데이터 베이스의 정보를 rows에 저장
print(rows)

con.close() #sql과의 연결 끊기

VirusDB = [ #VirusDB에 rows 데이터를 저장
    rows
    ]
vdb = [] #가공한 데이터를 저장할 배열 생성

def MakeVirusDB() :
    for db in rows:
        for k in db:
            print(k)
            vdb.append(k)      #row의 데이터(리스트형태)를 각자 배열의 원소로 만듦
        
    for k in vdb :
        print(k)
        
def SearchVDB(fmd5) :
    for t in vdb :
        if t == fmd5 :
            return True  #vdb의 원소들에 대해서 반복을 시행하는데 t == fmd5이면 True를 반환
        
    return False, ' '


if __name__ == '__main__' :
    MakeVirusDB()
    
    
    if len(sys.argv) != 2 : #검사할 인자가 주어지지 않으면 아래의 문구 출력
        print ('Usage : antivirus.py [file]')
        sys.exit(0) #검사할 인자 주어지지 않으면 프로그램을 멈춤
        
        
    fname = sys.argv[1] #검사할 인자(파일)이 주어지면 fname에 저장
    print(fname)
        
        
        
    fp = open(fname, 'rb')  #인자로 주어진 파일을 바이너리로 읽음
    buf = fp.read()
    fp.close()
        
    m = hashlib.md5()
    m.update(buf)
    fmd5 = m.hexdigest() #주어진 파일의 md5값
    
    print(fmd5)
        
    ret = SearchVDB(fmd5)
    if ret == True :
            print ('%s :Virus' % (fname))
            os.remove(fname)
    else :
            print ('%s : Not Virus' % fname)