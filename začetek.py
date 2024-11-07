import requests
from bs4 import BeautifulSoup
import re
import csv


vsi_članki = []

#zanka za zbiranje podatkov iz spletne strani
for i in range(70):
    url = f"https://radiostudent.si/kultura?page={i}"
    izhod = requests.get(url)
    soup = BeautifulSoup(izhod.text, 'html.parser')

    #vsak članek posebej (naslov, avtorica, tip oddaje, datum)
    članki = soup.find_all('div', class_='views-item')  

    for članek in članki:
        naslov = članek.find('div', class_="field field--name-title field--type-string field--label-hidden").get_text(strip=True)  # Assuming titles are in <h2>

        avtor = članek.find('div', class_='field field--name-uid field--type-string field--label-hidden').get_text(strip=True)

        vzorec = r'field__item krovna-oddaja-tip-127 oddaja-level-2[^"]*'
        x = re.findall(vzorec, str(članek))

        tip_oddaje = članek.find('div', class_=x[0]).get_text(strip=True)

        datum = članek.find('div', class_='field field--name-field-v-etru field--type-datetime field--label-hidden field__item').get_text(strip=True)

        # Append data to the list
        vsi_članki.append((naslov, avtor, tip_oddaje, datum))

# csv datoteka
with open('radio_student_articles.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["naslov", "avtor", "tip_oddaje", "datum"])
    writer.writerows(vsi_članki)

print(f"Podatki, shranjeni v radio_student_articles.csv. Vsi članki: {len(vsi_članki)}")


