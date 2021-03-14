"""
This file contains functions that
scrape the detailed occupation data from the BLS website.
"""


import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import numpy as np
from re import search


def get_occupation_links():
    """
    Parses the URL into the BeautifulSoup format
    and gets the URLs to the detailed data for each occupation.
    Then it writes those urls into a CSV file.
    """
    URL = ("https://www.bls.gov/ooh/occupation-finder.htm?"
           "pay=&education=&training=&newjobs=&growth=&submit=GO/")
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')

    occupations = []

    table = soup.find('table', attrs={'id': 'occfinder'})

    table_body = table.find('tbody')

    for row in table_body.findAll('tr'):
        occupation = {}
        occupation['occupation_name'] = row.strong.text
        occupation['url'] = "https://www.bls.gov" + row.a['href']
        occupation['2019 Median Pay'] = np.nan
        occupation['Typical Entry-Level Education'] = np.nan
        occupation['Work Experience in a Related Occupation'] = np.nan
        occupation['On-the-job Training'] = np.nan
        occupation['Number of Jobs, 2019'] = np.nan
        occupation['Job Outlook, 2019-29'] = np.nan
        occupation['Employment Change, 2019-29'] = np.nan
        occupations.append(occupation)

    filename = 'occupation_links.csv'
    with open(filename, 'w', newline='') as f:
        w = csv.DictWriter(f, ['occupation_name', 'url', '2019 Median Pay',
                               'Typical Entry-Level Education',
                               'Work Experience in a Related Occupation',
                               'On-the-job Training', 'Number of Jobs, 2019',
                               'Job Outlook, 2019-29',
                               'Employment Change, 2019-29'])
        w.writeheader()
        for occupation in occupations:
            w.writerow(occupation)


def expand_occupation_data(occupation_URL):
    """
    Returns detailed occupation data
    specified by occupation_URL as a DataFrame.
    """
    if search('about', occupation_URL):
        data = {
            '2019 Median Pay': [np.nan],
            'Typical Entry-Level Education': [np.nan],
            'Work Experience in a Related Occupation': [np.nan],
            'On-the-job Training': [np.nan],
            'Number of Jobs, 2019': [np.nan],
            'Job Outlook, 2019-29': [np.nan],
            'Employment Change, 2019-29': [np.nan],
            'url': [occupation_URL]
        }

        return pd.DataFrame(data).set_index('url')

    r = requests.get(occupation_URL)
    df_list = pd.read_html(r.text)
    df = df_list[0]
    df = df.pivot_table(columns=df.columns[0],
                        values=df.columns[1], aggfunc='first')
    df.insert(6, 'url', occupation_URL)

    return df.set_index('url')


def main():
    """
    Loops through all the links in occupation_links.csv
    to get the detailed data for all occupations and adds it to a DataFrame.
    The DataFrame is then written into a csv file.
    """
    get_occupation_links()

    occupation_df = pd.read_csv('occupation_links.csv', encoding="ISO-8859-1")
    occupation_df = occupation_df.set_index('url')
    link_list = occupation_df.index.tolist()

    counter = 0

    for link in link_list:
        occupation_df.update(expand_occupation_data(link))

        print("Success!" + " " + str(counter))
        counter += 1

    occupation_df.to_csv('occupation_data.csv')


if __name__ == '__main__':
    main()
