import requests 
from bs4 import BeautifulSoup
import csv
  
URL = "https://www.bls.gov/ooh/occupation-finder.htm?pay=&education=&training=&newjobs=&growth=&submit=GO/"
r = requests.get(URL) 
  
soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib

occupations = []
   
table = soup.find('table', attrs = {'id': 'occfinder'})

table_body = table.find('tbody')
   
for row in table_body.findAll('tr'):
    print(row)
    occupation = {} 
    occupation['occupation_name'] = row.strong.text 
    occupation['url'] = row.a['href']
    occupations.append(occupation) 
   
filename = 'occupation_links.csv'
with open(filename, 'w', newline='') as f: 
    w = csv.DictWriter(f,['occupation_name','url']) 
    w.writeheader() 
    for occupation in occupations: 
        w.writerow(occupation)