# Convert a list of URLs to a list of text
def get_text(urls):
    """
    Given a list of URLs, return a list of text
    """
    text = []
    for url in urls:
        text.append(get_text_from_url(url))
    return text

def get_text_from_url(url):
    """
    Given a URL, return the text from that URL
    """
    import requests
    response = requests.get(url)
    return response.text



# Take a pdf file and re-create it using markdown
def convert_pdf(filename):
    """
    Given a filename, convert the file to markdown
    """
    import os
    import pdf2txt
    import markdown
    import re
    # Get the text from the pdf
    text = pdf2txt.get_string(filename)
    # Remove all the newlines
    text = re.sub(r'\n', ' ', text)
    # Remove all the punctuation
    text = re.sub(r'[^A-Za-z0-9 ]', '', text)
    # Remove all the spaces
    text = re.sub(r'\s+', ' ', text)
    # Convert to markdown
    text = markdown.markdown(text)
    # Write to a new file
    filename = filename.split('.')[0] + '.md'
    with open(filename, 'w') as f:
        f.write(text)



