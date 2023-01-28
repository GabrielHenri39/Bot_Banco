#importasao
import sqlite3
import os
from config.config1 import DIR_DATA_BASE


class Banco :
  
    
  def __init__(self,id:int, server:str,vale=0, material='Bz',pix=None):
    self.__id=int(id)
    self.__vale = vale
    self.__material = material
    self.__pix=f'{self.__id}_{server}'
    self.__pix_tre=pix
    self.__server = server
    self.__id_server= f"{self.__id}_{server}"
    self.con =sqlite3.connect(DIR_DATA_BASE)
    self.con.execute("PRAGMA foreign_keys = ON;")
    self.cun = self.con.cursor()
    self.create_tables()
    
  def create_tables(self):
    self.cun.execute("""
      CREATE TABLE IF NOT EXISTS server(
      id INTEGER PRIMARY KEY autoincrement,
      serve text,
      id_server text
      );
      """)
    self.cun.execute("""CREATE TABLE IF NOT EXISTS conta(
          Bz INTEGER(1000) default 0,
          Ag INTEGER(10000) default 0,
          Au INTEGER(100000)  default 0,
          Pt INTEGER  default 0,
          pix text,
          cid INTEGE,
          FOREIGN KEY(cid) REFERENCES server(id));""")
          
          
  def  __get_id_server(self):
    self.cun.execute("select id_server from server where serve = ?",(self.__server,))
    id_server =self.cun.fetchall()
    self.con.commit()
    return id_server

 
  def abrir_conta(self):
    try:
      id_server=self.__get_id_server()
      
      if  not id_server:
        self.cun.execute("""INSERT INTO server VALUES(NULL,?,?)""",(self.__server,self.__id_server))
        self.con.commit()
        cid=self.cun.lastrowid
        sql=("INSERT INTO  conta(pix,cid) VALUES(?,?)")
        valou =(self.__pix,cid)
        self.cun.execute(sql,valou)
        self.con.commit()
        return f" conta criada com sucesso seu pix é {self.__pix}"
 
      return f" já tem uma conta no esse servidor: {self.__server}"
      
    except sqlite3.Error as ERRO :
      return f""" deu erro no banco de dado {ERRO} contratar suporte """  
 
  def consuta(self):
    id_server = self.__get_id_server()
    if not id_server:
    
      return f"Você não tem uma conta aqui nos {self.__server}"
    elif self.__id_server == id_server[0][0]:
      self.cun.execute("select id from server where id_server=?",(id_server[0][0],))
      cid = self.cun.fetchall()
      self.con.commit()
      self.cun.execute("""
      select Bz,Ag,Au,Pt from conta where cid=?""",(cid[0][0],))
      salto = self.cun.fetchall()
      self.con.commit()
      
      return salto 
     
     
if __name__ == '__main__':
    banco=Banco(id=53,server="556")
    msm =banco.abrir_conta()
    print(msm)
  
  