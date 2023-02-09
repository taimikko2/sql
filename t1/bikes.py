import sqlite3

db = sqlite3.connect("bikes.db")
db.isolation_level = None


def distance_of_user(user):
    # ilmoittaa käyttäjän ajaman yhteismatkan. (2 pistettä)
    # print(db.execute("SHOW TABLEWS;").fetchone()[0]);
    return db.execute("SELECT IFNULL(SUM(distance), 0) FROM Trips t, Users u WHERE t.user_id=u.id AND u.name=?;", [user]).fetchone()[0]


def speed_of_user(user):
    # ilmoittaa käyttäjän keskinopeuden (km/h) kaikilla matkoilla kahden desimaalin tarkkuudella. (3 pistettä)
    return db.execute("SELECT round(sum(distance/1000.0)/sum(duration/60.0), 2) \
        FROM Trips t, Users u WHERE t.user_id=u.id AND u.name=?;", [user]).fetchone()[0];
    

def duration_in_each_city(day):
    # ilmoittaa jokaisesta kaupungista, kauanko pyörillä ajettiin annettuna päivänä. (4 pistettä)
    duration = db.execute("SELECT DISTINCT c.name, sum(t.duration) \
                          FROM Trips t, Cities c, Stops s \
                          WHERE t.from_id=s.id AND s.city_id=c.id AND t.day=? \
                          GROUP BY c.name;", [day]).fetchall()
    return duration


def users_in_city(city):
    # ilmoittaa, montako eri käyttäjää pyörillä on ollut annetussa kaupungissa. (3 pistettä)
    return db.execute("SELECT COUNT(DISTINCT t.user_id)\
                FROM Cities c, Trips t, Stops s\
                WHERE t.from_id = s.id AND s.city_id = c.id AND c.name = ?;", [city]).fetchone()[0]


def trips_on_each_day(city):
    # ilmoittaa jokaisesta päivästä, montako matkaa kyseisenä päivänä on ajettu. (4 pistettä)
    count = db.execute("SELECT DISTINCT t.day, COUNT(t.id)\
                FROM Trips t, Stops s, Cities c \
                WHERE t.from_id=s.id AND s.city_id=c.id AND c.name=? \
                GROUP BY t.day; ", [city]).fetchall()
    return count


def most_popular_start(city):
    # ilmoittaa kaupungin suosituimman aloitusaseman matkalle sekä matkojen määrän. (4 pistettä)
    start = db.execute("SELECT DISTINCT s.name, COUNT(*)\
                FROM Cities c, Trips t, Stops s\
                WHERE t.from_id = s.id AND s.city_id = c.id AND c.name = ?\
                GROUP BY s.name\
                ORDER BY count(*) DESC\
                LIMIT 1;", [city]).fetchall()[0];
    return start

'''
Testi 1: 2 pistettä
Testi 2: 3 pistettä
Testi 3: 4 pistettä
Testi 4: 3 pistettä
Testi 5: 4 pistettä
Testi 6: 4 pistettä
'''