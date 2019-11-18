'''
    This program is text scraping program from some Web pages.
    Author: NR
    2019/11/01
'''
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import urllib.request
import time
import datetime
import re
import argparse

# When via proxy
#proxies = {'http': '0.0.0.1'}
#proxy = urllib.request.ProxyHandler(proxies)

class TextExtraction:
    def __init__(self):
        self.dic_rules = {
            'TOKYO':[{'url':'http://www.metro.tokyo.jp/tosei/hodohappyo/ichiran.html',
                    1:['div',('id','tmp_contents')],
                }
            ],
            'OSAKA':[{'url':'https://www.finra.org/whats-new',
                    1:['div',('class','box_list')],
                },
            ],
            'AICHI':[{'url':'https://www.pref.aichi.jp/',
                    1:['div',('id','main_body')],
                },
            ]
        }
    
    def get_soup(self, url, html_parser="html.parser", need_user_agent=False):
        time.sleep(1)
        opener = urllib.request.build_opener()          # (proxy)← When via proxy
        
        if need_user_agent :                            # When sending a user agent
            # win
            # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
            # mac
            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
            opener.addheaders = [('User-agent',user_agent)]
        
        html = opener.open(url)
        soup = BeautifulSoup(html, html_parser)

        return soup

    def get_selenium(self, url, html_parser="lxml", invisible=False):
        time.sleep(1)
        options = Options()

        if invisible:
            options.add_argument('--headless')

        driver = webdriver.Chrome(chrome_options=options) # executable_path='',← when specifying the chrome driver path.
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located)
        driver.implicitly_wait(5)
        try:
            dummy_element = driver.find_element_by_css_selector("dummy_selector_bummy") # search for something dare that doesn't exist
        except:
            print('selector search finish')
        
        soup = BeautifulSoup(driver.page_source, html_parser)
        driver.close()

        return soup

    def get_text(self, soup, site_name):
        try:
            dic_param = self.dic_rules[site_name]
            
        except:
            print('site name is not defined')
        else:
            text = ''
            soup_mg = ''

            for j in range(len(dic_param)):
                soup_tmp = soup

                for i in range(1,len(dic_param[j])):
                    if len(dic_param[j][i]) > 1:
                        soup_tmp = soup_tmp.find(dic_param[j][i][0], attrs={dic_param[j][i][1][0] : dic_param[j][i][1][1]})
                        
                    else:
                        soup_tmp = soup_tmp.find(dic_param[j][i][0])

                    if soup_tmp is None:
                        break
                
                if soup_tmp is not None:
                    soup_mg = soup_mg + soup_tmp.text

            if soup_mg != '':
                text_sep = soup_mg.split('\n')
                text_tmp = [a for a in text_sep if a != ''] 

                for i in range(len(text_tmp)):
                    text_tmp[i] = text_tmp[i].strip()
                    if i != 0  and text_tmp[i] != '':
                        text += '\n'
                    text += text_tmp[i]
                text = re.sub(r' {2,}','\n',text)   # replace two or more spaces with \n
            #    text = re.sub(r' +\n','\n',text)   # other line feed codes
                ext = re.sub(r'\n{2,}','\n',text)   # replace two or more \n with one \n

        return text

    def csv_out(self, df_out, out_csv_path, sort_columns, write_mode='w'):
        df_out = df_out[sort_columns]
        df_out.to_csv(out_csv_path, index=False, sep=',', mode=write_mode)
        return

if __name__ == '__main__':

    # specify arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--site', help='Specifies the web site name to be scrape.', type=str, nargs='*')
    parser.add_argument('-w', '--write', help='Set csv write mode. w is overwrite, a is append', choices=['w','a'], default='w')
    parser.add_argument('-ad', '--add', help='Specify the input file of the past date with a minus number.', type=int)

    args = parser.parse_args()

    # set csv write mode
    write_mode = args.write
    
    # set site name
    select_site = []
    if args.site is not None:
        select_site = args.site
    
    today = now_datetime = datetime.datetime.now()
    now_str = now_datetime.strftime('%Y%m%d %H:%M:%S')
    
    if args.add is not None:                        # when use the past date input files.
        today = today + datetime.timedelta(days= args.add)

    today = today.strftime('%Y%m%d')
    
    # set file path
    in_file = './data/in_data_{}.csv'.format(today)
    out_file = r'./data/out_text.csv'
    
    # scraping
    try:
        #df_in = pd.read_excel(in_file)             # When the read file type is Excel
        df_in = pd.read_csv(in_file)
    except:
        print('input file is not found.')
    else:
        df_out = pd.DataFrame()
        Te = TextExtraction()

        for index, row in df_in.iterrows():
            site_name = row['site_name']

            if select_site != [] and site_name not in select_site: 
                continue

            link = row['link']
            soup = Te.get_soup(link, html_parser='lxml', need_user_agent=True )
            #soup = Te.get_selenium(link, html_parser="lxml", invisible=False)  # when use selenium
            
            if soup is None:
                continue
            
            text = Te.get_text(soup, site_name)

            date = row['date']
            dic = {
                'site_name': site_name,
                'link': link,
                'text': text,
                'date': date,
                'date_loaded': now_str,
            }
            df_out = df_out.append(dic, ignore_index=True)
            
        if len(df_out) != 0:
            sort_columns = ['site_name','link','text','date_loaded','date']
            Te.csv_out(df_out, out_file, sort_columns, write_mode)




                