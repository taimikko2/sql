import os
import sqlite3

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
    Ohjelma suorittaa tuhat kertaa kyselyn, jossa haetaan elokuvien määrä vuonna x. Jokaisessa kyselyssä x valitaan satunnaisesti väliltä 1900–2000. 

Toteuta ohjelma niin, että kaikki rivit lisätään saman transaktion sisällä (esimerkiksi alussa komento BEGIN ja lopussa komento COMMIT), jotta rivien lisääminen ei vie liikaa aikaa.

Elokuvien määrän laskemisessa käytä kyselyä, jossa haetaan COUNT(*) ehtoon täsmäävistä riveistä.

Suorita ohjelman avulla kolme testiä seuraavasti:

    Tauluun ei lisätä kyselyitä tehostavaa indeksiä.
    Tauluun lisätään kyselyitä tehostava indeksi ennen rivien lisäämistä.
    Tauluun lisätään kyselyitä tehostava indeksi ennen kyselyiden suoritusta. 
'''

db.execute("CREATE TABLE Elokuvat (\
	id INTEGER PRIMARY KEY, \
	nimi TEXT,
	vuosi INTEGER)");
	
def create_tables():
	