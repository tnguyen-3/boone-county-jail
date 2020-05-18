from bs4 import BeautifulSoup
import csv
import requests

f = open('inmate_list.csv', 'w', newline='')
writer = csv.writer(
    f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
writer.writerow(['name', 'height', 'weight', 'sex', 'eyes', 'hair', 'race',
    'age', 'city', 'state','case', 'charge_descrip', 'charge_status',
    'bail_amount','bond_type', 'court_date', 'court_time',
    'court_jurisdiction'])
home_url = 'https://report.boonecountymo.org/mrcjava/servlet/RMS01_MP.I00030s'
r = requests.get(home_url, headers={'user-agent': "I'm good people!!!"})
soup = BeautifulSoup(r.content, 'lxml')
inmate_href = soup.find('tbody', id='mrc_main_table').find('tr').find('a')['href']
inmate_url = 'https://report.boonecountymo.org/mrcjava/servlet/' + inmate_href
r = requests.get(inmate_url, headers={'user-agent': "I'm good people!!!"})
soup = BeautifulSoup(r.content, 'lxml')
mug_shot_divs = soup.find_all('div',{'class':'mugshotDiv'})
for div in mug_shot_divs:
    info_map = {
        'HEIGHT':None,
        'WEIGHT':None,
        'SEX':None,
        'EYES':None,
        'HAIR':None,
        'RACE':None,
        'AGE':None,
        'CITY':None,
        'STATE':None
    }
    name = div.find('div', {'class':'inmateName'}).text.strip()
    person_info = div.find('tbody', id='mrc_main_table')
    trs = person_info.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        header = tds[0].b.text.strip()
        value = tds[1].text.strip()
        info_map[header] = value

    height = info_map['HEIGHT']
    weight = info_map['WEIGHT']
    sex = info_map['SEX']
    eyes = info_map['EYES']
    hair = info_map['HAIR']
    race = info_map['RACE']
    age = info_map['AGE']
    city = info_map['CITY']
    state = info_map['STATE']

    personal_table = [name, height, weight, sex, eyes, hair, race, age, city, state]

    table_charges = div.find('table',
    {'class':'collapse centered_table shadow responsive'}).find_all('tr')[1:]

    for charge_row in table_charges:
        data_fields = charge_row.find_all('td')

        case = data_fields[0].text.strip()
        charge_descrip = data_fields[1].text.strip()
        charge_status = data_fields[2].text.strip()
        bail_amount = data_fields[3].text.strip()
        bond_type= data_fields[4].text.strip()
        court_date= data_fields[5].text.strip()
        court_time= data_fields[6].text.strip()
        court_jurisdiction= data_fields[7].text.strip()

        charge_table = [case, charge_descrip, charge_status, bail_amount,
            bond_type, court_date, court_time, court_jurisdiction]

        full_table= personal_table + charge_table

        writer.writerow(full_table)
        print(full_table)
