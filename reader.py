import psycopg2
from pprint import pprint

conn = psycopg2.connect(dbname='titanic', user='emyrzabekov', password='test01')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS passengers(
    id integer,
    survived integer,
    class integer,
    name text,
    sex varchar(50),
    age float,
    sibsp integer,
    parch integer,
    ticket varchar(255),
    fare numeric NULL,
    cabin varchar(255) NULL,
    embarked varchar(50)
)
""")
with open(r'titanic.txt', 'r') as f:
    next(f)
    cur.copy_from(f, 'passengers', sep='|')


def name_of_died():
    pogibli = "SELECT name FROM passengers WHERE survived = 0"
    # pprint(pogibli)
    cur.execute(pogibli)
    pogibshie = cur.fetchall()
    return pogibshie


def womens():
    jenshiny = "SELECT COUNT(*) FROM passengers WHERE sex = 'female' AND class = 1"
    cur.execute(jenshiny)
    all_womens = cur.fetchall()
    died_women = "SELECT COUNT(*) FROM passengers WHERE sex = 'female' AND class = 1 AND survived = 0"
    cur.execute(died_women)
    died_womens = cur.fetchall()
    for row in all_womens:
        count_all = row[0]
    for row in died_womens:
        count_died = row[0]
    died_percent = ((count_all - count_died) * 100) / count_all
    print(f'Процент выживших среди женщин первого класса: {died_percent} процента')

def men():
    cur.execute("SELECT COUNT(*) FROM passengers WHERE sex = 'male' AND class = 3 AND age < 20")
    man = cur.fetchall()
    for row in man:
        count_all = row[0]
    cur.execute("SELECT COUNT(*) FROM passengers WHERE sex = 'male' AND class = 3 AND age = 20 AND survived = 0")
    died_man = cur.fetchall()
    for row in died_man:
        count_died = row[0]
    died_percent = ((count_all - count_died) * 100) / count_all
    # print(count_died, count_all)
    print(f'Процент выживших среди Мужчин младше 20 лет третьего класса: {died_percent} процента')

def second_class():
    cur.execute("SELECT COUNT(*) FROM passengers WHERE class = 2 AND age > 30")
    sec_class = cur.fetchall()
    for row in sec_class:
        count_all = row[0]
    cur.execute("SELECT COUNT(*) FROM passengers WHERE class = 2 AND age > 30 AND survived = 0")
    died_sec_class = cur.fetchall()
    for row in died_sec_class:
        count_died = row[0]
    died_percent = ((count_all - count_died) * 100) / count_all
    # print(count_died, count_all)
    print(f'Процент выживших среди Пассажиров второго класса старше 30 лет: {died_percent} процента')

def women_cherbourg():
    cur.execute("SELECT COUNT(*) FROM passengers WHERE class = 2 AND embarked = 'C'")
    wo_cher = cur.fetchall()
    for row in wo_cher:
        count_all = row[0]
    cur.execute("SELECT COUNT(*) FROM passengers WHERE class = 2 AND embarked = 'C' AND survived = 0")
    died_wo_cher = cur.fetchall()
    for row in died_wo_cher:
        count_died = row[0]
    died_percent = ((count_all - count_died) * 100) / count_all
    # print(count_died, count_all)
    print(f'Процент выживших среди Женщин второго класса, севшие на борт в порту Cherbourg: {died_percent} процента')

def bro_or_sis():
    cur.execute("SELECT COUNT(*) FROM passengers WHERE sibsp > 0")
    bro_sis = cur.fetchall()
    for row in bro_sis:
        count_all = row[0]
    cur.execute("SELECT COUNT(*) FROM passengers WHERE sibsp > 0 AND survived = 0")
    died_bro_sis = cur.fetchall()
    for row in died_bro_sis:
        count_died = row[0]
    died_percent = ((count_all - count_died) * 100) / count_all
    # print(count_died, count_all)
    print(f'Процент выживших среди Пассажиров имевших на борту братьев или сестёр: {died_percent} процента')

def vozrast_pogibshih():
    cur.execute("SELECT COUNT(*) FROM passengers WHERE survived = 0")
    all_died = cur.fetchall()
    for row in all_died:
        count_all = row[0]
    cur.execute("SELECT SUM(age) FROM passengers WHERE survived = 0")
    all_died_age = cur.fetchall()
    for row in all_died_age:
        count_died = row[0]
    sredniy_vozrast = count_died / count_all
    # print(count_died, count_all)
    print(f'Средний возраст погибших людей: {sredniy_vozrast}')

def port():
    cur.execute("SELECT COUNT(*) FROM passengers WHERE embarked = 'C'")
    all_c = cur.fetchall()
    for row in all_c:
        count_allc = row[0]
    cur.execute("SELECT COUNT(*) FROM passengers WHERE embarked = 'Q'")
    all_q = cur.fetchall()
    for row in all_q:
        count_allq = row[0]
    cur.execute("SELECT COUNT(*) FROM passengers WHERE embarked = 'S'")
    all_s = cur.fetchall()
    for row in all_s:
        count_alls = row[0]
    cur.execute("SELECT COUNT(*) FROM passengers WHERE embarked = 'C' AND survived = 1")
    all_survive_c = cur.fetchall()
    for row in all_survive_c:
        count_survive_c = row[0]
    cur.execute("SELECT COUNT(*) FROM passengers WHERE embarked = 'Q' AND survived = 1")
    all_survive_q = cur.fetchall()
    for row in all_survive_q:
        count_survive_q = row[0]
    cur.execute("SELECT COUNT(*) FROM passengers WHERE embarked = 'S' AND survived = 1")
    all_survive_s = cur.fetchall()
    for row in all_survive_s:
        count_survive_s = row[0]
    percent_survive_c = (count_survive_c * 100) / count_allc
    percent_survive_q = (count_survive_q * 100) / count_allq
    percent_survive_s = (count_survive_s * 100) / count_alls
    if percent_survive_c < percent_survive_q:
        if percent_survive_c < percent_survive_s:
            if percent_survive_q < percent_survive_s:
                print("Порт, люди с которого, имели наибольший шанс выжить 'Southampton'")
            else:
                print("Порт, люди с которого, имели наибольший шанс выжить 'Queenstown'")
        else:
            print("Порт, люди с которого, имели наибольший шанс выжить 'Queenstown'")
    elif percent_survive_c > percent_survive_q:
        if percent_survive_c > percent_survive_s:
            print("Порт, люди с которого, имели наибольший шанс выжить 'Cherbourg'")
        elif percent_survive_c < percent_survive_s:
            print("Порт, люди с которого, имели наибольший шанс выжить 'Southampton'")


    # print(percent_survive_c, percent_survive_q, percent_survive_s)
    # print(f'Средний возраст погибших людей: {percent_survive_s}')


# начало вашего кода




print(name_of_died())
womens()
men()
second_class()
women_cherbourg()
bro_or_sis()
vozrast_pogibshih()
port()

conn.commit()
cur.close()
conn.close()
