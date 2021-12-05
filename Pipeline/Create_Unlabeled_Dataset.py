from bs4 import BeautifulSoup
import pandas as pd
import os
import dask
import dask.dataframe
from math import ceil
import re

"""
1. take a url as input and make it into a bs4 soup object
"""
from urllib.request import urlopen

def make_soup(url):
    # print('in make_soup')

    html = urlopen(url, timeout = 4).read()
    # print(html)
    return BeautifulSoup(html, "lxml")

"""
2. take a soup object and find all the links on the page
"""
def find_links(soup):
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    return links

"""
3. take a soup object and find all the text on the page
"""
def find_text(soup):
    text = soup.get_text()
    return text

"""
4. take a soup object and find all the images on the page
"""
def find_images(soup):
    images = []
    for image in soup.find_all('img'):
        images.append(image.get('src'))
    return images

"""
5. take a soup object and find all the tables on the page
"""
def find_tables(soup):
    tables = []
    for table in soup.find_all('table'):
        tables.append(table)
    return tables

"""
6. take a soup object and find all the forms on the page
"""
def find_forms(soup):
    forms = []
    for form in soup.find_all('form'):
        forms.append(form)
    return forms

"""
7. take a soup object and find all the headings on the page
"""
def find_headings(soup):
    headings = []
    for heading in soup.find_all(re.compile('^h[1-6]$')):
        headings.append(heading)
    return headings

"""
8. take a soup object and find all the paragraphs on the page
"""
def find_paragraphs(soup):
    paragraphs = []
    for paragraph in soup.find_all('p'):
        paragraphs.append(paragraph)
    return paragraphs

"""
9. take a soup object and find all the divs on the page
"""
def find_divs(soup):
    divs = []
    for div in soup.find_all('div'):
        divs.append(div)
    return divs

"""
10. take a soup object and find all the spans on the page
"""
def find_spans(soup):
    spans = []
    for span in soup.find_all('span'):
        spans.append(span)
    return spans

"""
11. take a soup object and find all the list items on the page
"""
def find_list_items(soup):
    list_items = []
    for list_item in soup.find_all('li'):
        list_items.append(list_item)
    return list_items

"""
12. take a soup object and find all the unordered list on the page
"""
def find_unordered_lists(soup):
    unordered_lists = []
    for unordered_list in soup.find_all('ul'):
        unordered_lists.append(unordered_list)
    return unordered_lists

"""
13. take a soup object and find all the ordered list on the page
"""
def find_ordered_lists(soup):
    ordered_lists = []
    for ordered_list in soup.find_all('ol'):
        ordered_lists.append(ordered_list)
    return ordered_lists

"""
14. take a soup object and find all the h1-h6 on the page
"""
import re
def find_headings(soup):
    headings = []
    for heading in soup.find_all(re.compile('^h[1-6]$')):
        headings.append(heading)
    return headings

"""
15. take a soup object and find all the paragraphs on the page
"""
def find_paragraphs(soup):
    paragraphs = []
    for paragraph in soup.find_all('p'):
        paragraphs.append(paragraph)
    return paragraphs

"""
16. Given a list of URLs, extract the paragraphs and return a pandas DataFrame
"""
def create_df(urls, save_directory, filename = 'Unlabeled_Data'):
    print("in create_df")
    df = pd.DataFrame()
    save_directory = os.path.normpath(save_directory)
    filename = filename + '.csv'
    save_path = os.path.join(save_directory, filename)
    start_index = 0
    if os.path.exists(save_path):
        df = pd.read_csv(save_path)
        start_index = len(df)

    for i, url in enumerate(urls):
        if i < start_index:
            pass
        else:
            if i%1000 == 0:
                print('index checkpoint:', i)
                df.to_csv(save_path)
                print('Dataframe Saved')
            try:
                soup = make_soup(url)
                paragraphs = find_paragraphs(soup)
                paragraphs_list = [p.text for p in paragraphs]
                tuples_list = [(url, i, p) for i,p in enumerate(paragraphs_list)]
                for tup in tuples_list:
                    df=df.append(pd.Series(tup, index= ['url','paragraph_index', 'paragraph_text']), ignore_index=True)

            except:
                print('error at index', i, url)
                pass

    return df

def df_batch(policy_df, index_range):
    df = pd.DataFrame()
    batch = policy_df.iloc[index_range[0]: index_range[1]]
    df['URL'] = batch['URL']
    df['Policy ID'] = batch['ID']
    df['paragraphs'] = batch['URL'].apply(fetch_policies)

    return df

def clean_text(text):
    text = text.replace('/n', '')
    text = text.replace(r'\n', '')
    text = text.replace(r'\xa0 &', '')
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    return text

def clean_urls(source):
    try:
        s = source.split("'Final URL': '")[1].split("'}")[0]
    except:
        s = source.split("'Original URL': '")[1].split("',")[0]
    return s

def fetch_policies(url):
    try:
        soup = make_soup(url)
        paragraphs = find_paragraphs(soup)
        paragraphs = [clean_text(p.text) for p in paragraphs if len(p.text.split())>3]
        return paragraphs
    except:
        return 'ERROR'

def create_batched_df(policy_df, save_directory, batch_size = 100, filename = 'Unlabeled_Data', max_batches = float('inf')):
    save_directory = os.path.normpath(save_directory)
    filename = filename + '.csv'
    save_path = os.path.join(save_directory, filename)

    if os.path.exists(save_path):
        df = pd.read_csv(save_path)
        start_index = max(df['Policy ID'])
    else:
        df = pd.DataFrame(columns = ['URL', 'Policy ID', 'paragraphs'])
        start_index = 0

    num_batches = ceil((len(policy_df) - start_index)/batch_size)
    if num_batches > max_batches:
        num_batches = max_batches

    for i in range(num_batches):
        end_index = start_index + batch_size
        batch = df_batch(policy_df, (start_index, end_index))
        df = df.append(batch, ignore_index = True)
        df.to_csv(save_path)
        print('Saved Batch', i)
        print(' -- index: ['+str(start_index), ':', str(end_index) + ']')
        start_index = end_index
        end_index = end_index + batch_size
    return df




def create_docs(urls, save_directory):
    log_file = os.path.join(save_directory, 'log.csv')
    try:
        log = pd.read_csv(master_doc)
    except:
        log = pd.DataFrame(columns=['Completed'])

    urls = pd.Series(urls)
    urls = list(urls[~urls.isin(log['Completed'])])

    for i, url in enumerate(urls):
        try:
            soup = make_soup(url)
            paragraphs = find_paragraphs(soup)
            paragraphs_list = [p.text for p in paragraphs]
            for idx, par in enumerate(paragraphs_list):
                if len(par.split()) > 2:
                    name = 'policy_index_'+str(i) + '_paragraph_' + str(idx) +'.txt'
                    filepath = os.path.join(save_directory, name)
                    if not os.path.exists(filepath):
                        with open (filepath, 'w+') as destination:
                            destination.write(par)

        except:
            print('error at index', i, url)
            pass
        log.append({'Completed': url}, ignore_index = True)
        log.to_csv(log_file)


def create_dask_df(urls):
    df = dask.dataframe.DataFrame(columns = ['Policy Index', 'URL', ])

    return df



if __name__ == '__main__':
    path_to_policy_urls_csv = os.path.normpath('../Data/policy_urls/april_2018_policies.csv')
    batch_size = 1000
    #load the privacy policies URL csv file
    df_policies = pd.read_csv(path_to_policy_urls_csv)
    #clean policy source document
    df_policies['URL'] = df_policies['Policy Sources'].apply(clean_urls)

    df = create_batched_df(df_policies, '../Data/Unlabeled_Data', batch_size = batch_size)

