import os
import sqlite3
import random
import time

# poistaa tietokannan alussa (kätevä moduulin testailussa)
os.remove("movies.db")

db = sqlite3.connect("movies.db")
db.isolation_level = None

'''
Tee ohjelma, jonka avulla voidaan suorittaa tietokannan tehokkuustesti. Tehokkuustestin osat ovat:

    Ohjelma luo taulun Elokuvat, jossa on sarakkeet id, nimi ja vuosi.
    Ohjelma lisää tauluun miljoona riviä.
		Jokaisen elokuvan nimeksi valitaan satunnainen merkkijono, jossa on 8 merkkiä,
		ja vuodeksi valitaan satunnainen kokonaisluku väliltä 1900–2000.
    
    Ohjelma suorittaa tuhat kertaa kyselyn, jossa haetaan elokuvien määrä vuonna x. 
    Jokaisessa kyselyssä x valitaan satunnaisesti väliltä 1900–2000.

Toteuta ohjelma niin, että kaikki rivit lisätään saman transaktion sisällä
(esimerkiksi alussa komento BEGIN ja lopussa komento COMMIT), jotta rivien lisääminen ei vie liikaa aikaa.

Elokuvien määrän laskemisessa käytä kyselyä, jossa haetaan COUNT(*) ehtoon täsmäävistä riveistä.

Suorita ohjelman avulla kolme testiä seuraavasti:

    Tauluun ei lisätä kyselyitä tehostavaa indeksiä.
    Tauluun lisätään kyselyitä tehostava indeksi ennen rivien lisäämistä.
    Tauluun lisätään kyselyitä tehostava indeksi ennen kyselyiden suoritusta.
'''

def random_nimi():
  return "".join(random.choices("abcdefhijklmnopqrstuvwxyzåäöABCDEFHIJKLMNOPQRSTUVWXYZÅÄÖ", k=8))
  
def add_rows():
  alku = time.time()
  db.execute("BEGIN;")
  for i in range(10**6): 
    nimi = random_nimi()
    vuosi = random.randint(1900, 2000)
    db.execute("INSERT INTO Elokuvat (nimi, vuosi) VALUES (?,?);", [nimi, vuosi])
  db.execute("COMMIT;")
  loppu = time.time()
  return(loppu-alku)

def kysely():
  # Ohjelma suorittaa tuhat kertaa kyselyn, jossa haetaan elokuvien määrä vuonna x. 
  # Jokaisessa kyselyssä x valitaan satunnaisesti väliltä 1900–2000.
  alku = time.time()
  for i in range(1000):
    vuosi = random.randint(1900, 2000)
    db.execute("SELECT COUNT(*) FROM Elokuvat WHERE vuosi = ?",[vuosi])
  loppu = time.time()
  return(loppu-alku)
    
def luo_tietokanta():
  alku = time.time()
  db.execute("CREATE TABLE Elokuvat (\
    id INTEGER PRIMARY KEY, \
    nimi TEXT, 	vuosi INTEGER)")
  loppu = time.time()
  return(loppu-alku)

def lisaa_indeksi():
  alku = time.time()
  db.execute("CREATE INDEX idx_vuosi ON Elokuvat (vuosi);");
  loppu = time.time()
  return(loppu-alku)

print("testi 1: Tauluun ei lisätä kyselyitä tehostavaa indeksiä.");
print("tietokannan luonti ilman indeksiä",luo_tietokanta())
print("rivien lisääminen ilman indeksiä", add_rows())
print("kysely ilman indeksiä",kysely())
print("katso tietokannan koko")
'''
print("testi 2: Tauluun lisätään kyselyitä tehostava indeksi ennen rivien lisäämistä.")
print("tietokannan luonti ilman indeksiä",luo_tietokanta())
print("indeksin lisääinen ennen dataa",lisaa_indeksi())
print("rivien lisääminen indeksillä", add_rows())
print("kysely indeksin kanssa",kysely())
print("katso tietokannan koko")

print("testi 3: Tauluun lisätään kyselyitä tehostava indeksi ennen kyselyiden suoritusta. ")
print("tietokannan luonti ilman indeksiä",luo_tietokanta())
print("rivien lisääminen ilman indeksiä", add_rows())
print("indeksin lisääminen ennen kyselyä",lisaa_indeksi())
print("kysely indeksin kanssa",kysely())
print("katso tietokannan koko")
'''