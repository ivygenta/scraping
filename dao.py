# -*- coding: utf-8 -*-
import mysql.connector

def insertsql(commentlist):
 try:
  cnn = mysql.connector.connect(host='xxxxx',
                                  port=3306,
                                  db='websc',
                                  user='xxx',
                                  passwd='xxx')

  cur = cnn.cursor()

  for cm in commentlist:
   cur.execute("INSERT INTO posts (post) VALUES ("+'\''+cm+'\''+")")
   cnn.commit()

  cur.close()
  cnn.close()

 except (mysql.connector.errors.ProgrammingError) as e:
     print (e)