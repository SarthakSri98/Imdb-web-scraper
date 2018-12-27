from bs4 import BeautifulSoup
import urllib.request as urllib
import csv
from halo import Halo

csvfile = csv.writer(open('imdb.csv', 'w'))
csvfile.writerow(["Name", "Year of release", "Rating", "Genre", "imdb Url", "votes"])
pages = int(input("enter number of pages to scrap:"))
url = 'http://www.imdb.com/search/title?genres=action'
i = 1
while pages > 0:
    request = urllib.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0')
    myurlopener = urllib.build_opener()
    myurl = myurlopener.open(request)
    spinner = Halo(text="Processing Page", spinner="dots")
    spinner.start()
    myurldata = myurl.read()
    soup = BeautifulSoup(myurldata, 'lxml')
    for choice in soup.find_all('div', class_='lister-item-content'):
        name = choice.a.text.encode('utf-8')
        imdburl = choice.a.get('href').encode('utf-8')
        if not imdburl.startswith(b'http://www.imdb.com'):
            imdburl = "http://www.imdb.com" + str(imdburl, "utf-8")
        year = choice.find('span', class_='lister-item-year').text.encode('utf-8')
        try:
            rating = choice.find('div', class_='ratings-imdb-rating').get('data-value').encode('utf-8')
        except AttributeError:
            rating = "NA"
        genre = choice.find('span', class_='genre').text.encode('utf-8')
        try:
            votes = choice.find('span', {"name": 'nv'}).text.encode('utf-8')
        except AttributeError:
            votes = "NA"
        csvfile.writerow([name, year, rating, genre, imdburl, votes])
    url = soup.find('a', class_="lister-page-next").get('href')
    if not url.startswith("http://www.imdb.com/search/title"):
        url = ("http://www.imdb.com/search/title" + url)
    spinner.stop()
    pages = pages - 1
    print("\nPage Number " + str(i) + " complete")
    i = i + 1
print("Scraping Complete")
