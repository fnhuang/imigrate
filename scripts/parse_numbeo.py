import csv
import requests
from bs4 import BeautifulSoup
import sys

imigrate = "C:/Users/fnatali/OneDrive/iMigrate/"

def get_country_index():
    country_index_dict = {}

    reader = open(imigrate + "country_code.csv", "r")
    csvreader = csv.DictReader(reader)

    for row in csvreader:
        cname = row["country numbeo"]
        cabbr = row["country code"]

        country_index_dict[cname] = cabbr

    reader.close()

    return country_index_dict

def get_numbeo_index():
    country_index_dict = get_country_index()

    url = "https://www.numbeo.com/quality-of-life/rankings.jsp"

    ccdict = {}

    resp = requests.get(url).text
    soup = BeautifulSoup(resp, 'html.parser')
    atags = soup.find_all("td", {"class": "cityOrCountryInIndicesTable"})

    for atag in atags:
        if len(atag.text) > 0:
            arrs = atag.text.split(",")
            city = ""
            country = ""
            if len(arrs) > 2:
                country = arrs[2].strip().lower()
                city = arrs[0].strip().lower() + " " + arrs[1].strip().lower()
            else:
                country = arrs[1].strip().lower()
                city = arrs[0].strip().lower()
                if city == "hong kong":
                    country = "china"

            cc = city + "," + country_index_dict[country]
            #next_td_tag = atag.parent.findNext("td")
            next_td_tag = atag.findNext("td")
            value = float(next_td_tag.text)

            ccdict[cc] = value

    reader = open(imigrate + "numbeo_values.csv","r")
    csv_reader = csv.DictReader(reader)

    writer = open(imigrate + "temp.csv","w",newline="")
    csv_writer = csv.writer(writer)
    csv_writer.writerow(["city","country","cost of living index","property prices index",
                         "health care index","crime index","quality of life index"])

    for row in csv_reader:
        city = row["city"]
        country = row["country"]
        cc = city + "," + country
        value = -1
        try:
            value = ccdict[cc]
        except KeyError:
            pass

        values = list(row.values())
        values.append(value)
        csv_writer.writerow(values)
    reader.close()
    writer.close()


def get_country_numbeo():
    country_index_dict = get_country_index()
    url = "https://www.numbeo.com/quality-of-life/rankings.jsp"

    countries = set([])

    resp = requests.get(url).text
    soup = BeautifulSoup(resp, 'html.parser')
    atags = soup.find_all("td", {"class": "cityOrCountryInIndicesTable"})

    for atag in atags:
        if len(atag.text) > 0:
            arrs = atag.text.split(",")
            if len(arrs) > 2:
                country = arrs[2].strip().lower()
            else:
                country = arrs[1].strip().lower()
            if country not in country_index_dict.keys():
                countries.add(country)

    for country in countries:
        print(country)

def load_country_continent():
    cou_con = {}
    reader = open("country_continent.csv")
    csvreader = csv.DictReader(reader)

    for row in csvreader:
        country = row['country']
        continent = row['continent']

        cou_con[country] = continent

    reader.close()

    return cou_con

def get_our_cities():
    cou_con = load_country_continent()

    writer = open("our_cities.csv","w",newline="")
    csvwriter = csv.writer(writer)
    csvwriter.writerow(["city","country"])

    countries_included = ["jpn","twn","kor","sgp","rus","can"]
    continents_included = ["w europe","n europe","aus and nzl"]

    reader = open("teleport_cities.csv")
    csvreader = csv.DictReader(reader)

    for row in csvreader:
        country = row['country']
        city = row['city']
        continent = cou_con[country]
        #print(city)

        if continent in continents_included or country in countries_included:
            csvwriter.writerow(row.values())

    reader.close()
    writer.close()

def get_unique_countries():
    reader = open("teleport_cities.csv")
    csvreader = csv.DictReader(reader)

    countries = set()

    for row in csvreader:
        country = row['country']
        countries.add(country)

    reader.close()

    for country in countries:
        print(country)

if __name__ == "__main__":
    get_numbeo_index()