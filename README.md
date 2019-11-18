# scraping_multi_text

## Description
"scraping_multi_text" is code that scrapes and retrieves text from several different web pages with python.<br>
The scraping part is one abstract function that scrapes the source code of different web pages.

## Requirement
Python 3.6.9

## Installation
pip install beautifulsoup4<br>
pip install selenium

## Usage
The file named in_data_yyyymmdd.csv in the data folder is the input data file.<br>
For yyyymmdd, specify an 8-digit date.<br>
The date specified in the argument or the current date if not specified.

In a terminal, go to the same level directory as scraping_text.py and use the following command:
  
python scraping_text.py

#### Explanation of arguments
python scraping_text.py -s TOKYO -w w -ad -8

-s (or --site) is specify the site_name of the data to be output from the input data.

-w (or --write) is when outputting a CSV file, it is overwritten or appended. w is overwriting, a is appending.

-ad (or --add) is pecify the date of the past input file. <br>
Specify the number of days before the current day with a number with a minus number.

