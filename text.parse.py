from urllib.request import Request, urlopen
from bs4 import BeautifulSoup, SoupStrainer
import time
import subprocess

# http://www.8novels.net/classics/u6082.html

def read_html(url):
	html = urlopen(url).read()

	return html

def get_url(y):
	f = y.rfind('_')
	g = y.rfind('/')

	if f == -1:
		start1 = y.rfind('/') + 1
		end1 = y.find('.html')
		code = y[start1:end1]

	elif f !=-1 and (f < g):
		start1 = y.rfind('/') + 1
		end1 = y.find('.html')
		code = y[start1:end1]

	else:
		start1 = y.rfind('/') + 1
		end1 = y.rfind('_')
		code = y[start1:end1]

	start = y.find('www.')
	end = y.find(str(code))
	path = y[start:end]

	return path, code

def get_title(html):
	title_text = SoupStrainer("title")
	title_soup = str(BeautifulSoup(html, "html.parser", parse_only=title_text))

	title_start = title_soup.find('Read ') + 5
	title_end = title_soup.find(' online')
	title = title_soup[title_start:title_end]

	return title

def get_pages(html):
	page_text = SoupStrainer("ul", {'class':'pagelist'})
	page_soup = str(BeautifulSoup(html, "html.parser", parse_only=page_text))

	pages_start = page_soup.find('<ul class="pagelist"><li><a>') + 28
	pages_end = page_soup.find('pages:')
	pages = page_soup[pages_start:pages_end]

	return pages

def make_file(name):
	path = '/Users/annabelle_strong/Documents/Bin/Extracted Texts/'
	title = str(name)

	filename = str(path + title + ".txt")

	file = open(filename,"w")

	return file, filename

# Get full url
address = input("What's the url of the book you want to parse? ")

# Split url for page looping and processing
raw_url = get_url(address)
path = raw_url[0]
code = raw_url[1]

# Load webpage with full url
url = Request(address, headers={'User-Agent': 'Mozilla/5.0'})

# Parse page
setup_html = read_html(url)

# Get name of book
title = get_title(setup_html)

# Create .txt file
txt = make_file(title)
file = txt[0]
filename = str(txt[1])

# Get number of pages
pages = int(get_pages(setup_html))

# Loop through pages
for a in range(1, pages+1):
	if a != 1:
		# Load new url based on page number
		new_url = Request('http://' + str(path) + str(code) + '_' + str(a) +'.html', headers={'User-Agent': 'Mozilla/5.0'})
		# Read updated html
		html = read_html(new_url)
	else:
		html = setup_html

	# Filter paragraph text and parse page
	p = SoupStrainer("p")

	soup = BeautifulSoup(html, "html.parser", parse_only=p)

	# Remove all script and style elements
	for script in soup(["script", "style"]):
	    script.extract()    # rip it out

	# Remove copyright line
	for p in soup.find_all("p", {'class':'info'}):
	    p.decompose()

	# Extract text
	text = soup.get_text()

	# Write text to document
	file.write(text)

print("Text extraction complete.")

subprocess.call(["open", "-R", filename])
