import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os
import logging

html_dir=r"C:\Users\16193\My Drive\Back Up\The Internationalist Group\Political Economy\Lenin's Imperialism\Concentration of banking\date_pipeline_2.0\html_files"
csv_dir=r"C:\Users\16193\My Drive\Back Up\The Internationalist Group\Political Economy\Lenin's Imperialism\Concentration of banking\data_pipeline_2.0\csv_files"

#===================Quarterly Dates Generation Function================================
"Develops a list of quarterly end dates from a given start year up to the current year."
def generate_quarterly_dates(start_year):
    """Generates a list of quarterly end dates from a given start year up to the current year."""
    end_year = datetime.now().year  # Current year
    quarters = ["March 31,", "June 30,", "September 30,", "December 31,"]
    formatted_dates = []
    for year in range(start_year, end_year + 1):
        for quarter in quarters:
            formatted_dates.append(quarter + " " + str(year))
    return formatted_dates

generate_quarterly_dates(2003)

#===================Date to Quarter Conversion Function================================

'''Converts a date to a quarter.'''
def date_to_quarter(month, day):
    if month == 3 and day == 31:
        return 'Q1'
    elif month == 6 and day == 30:
        return 'Q2'
    elif month == 9 and day == 30:
        return 'Q3'
    elif month == 12 and day == 31:
        return 'Q4'
    else:
        return None
    
date_to_quarter(3, 31)

#===================Webscrape, Update and Rename Files Function================================

'''
Webscrapes the Federal Reserve website for large commercial bank data, updates the files, 
and renames them according to a specified format.
'''
def update_and_rename_files():
    """Downloads data, uploads to S3, and renames files according to a specified format."""
    URL = "https://www.federalreserve.gov/releases/lbr/"
    quarterly_dates = generate_quarterly_dates(2003)
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    all_links = soup.find_all('a', href=True)
    links = [(link['href'], link.text) for link in all_links if any(date in link.text for date in quarterly_dates)]

    for href, date in links:
        full_url = URL + href
        table_response = requests.get(full_url)
        filename = re.sub(r'\W+', '_', href) + ".html"
        date_obj = datetime.strptime(date, "%B %d, %Y")
        datenum = date_obj.strftime("%Y%m%d")
        quarter = date_to_quarter(date_obj.month, date_obj.day)
        new_filename = f'{datenum}_{quarter}_{date_obj.year}_large_commercial_banks.html'
        current_path = os.path.join(html_dir, filename) # Path to current file
        new_path = os.path.join(html_dir, new_filename) # Path to new file

        #Write the content of the respons to a file
        with open(new_path, 'w', encoding='utf-8') as f:
            f.write(table_response.text)

update_and_rename_files()

