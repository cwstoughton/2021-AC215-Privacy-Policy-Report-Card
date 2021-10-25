from bs4 import BeautifulSoup
import pandas as pd


"""
1. take a url as input and make it into a bs4 soup object
"""
from urllib.request import urlopen

def make_soup(url):
    # print('in make_soup')
    html = urlopen(url).read()
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
def create_df(urls):
    print("in create_df")
    df = pd.DataFrame()
    for i, url in enumerate(urls):
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


if __name__ == '__main__':
    path_to_policy_urls_csv = './Data/policy_urls/april_2018_policies.csv'
    num_policies_to_extract = 100
    # load the privacy policies URL csv file
    df_policies = pd.read_csv(path_to_policy_urls_csv)
    # print(df_policies.head(5))

    # select 10 urls for demo
    df_policies = df_policies.iloc[:num_policies_to_extract]

    # extract urls of privacy policies
    # TODO: Needs to be modified to include all urls in the dataset. Currently just looks at the first "Final URL" of each row.
    urls = [item.split("'Final URL': '")[1].split("'}")[0] for item in df_policies['Policy Sources']]
    # print(urls)
    # Create a dataframe with the policy texts
    df = create_df(urls)
    print(df.head())
    print(f"DataFrame consists of {df.shape[0]} paragraphs from {num_policies_to_extract} policies.")

    # Save dataframe as csv file
    df.to_csv('policy_texts.csv')

