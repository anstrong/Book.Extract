from urllib.request import Request, urlopen
from bs4 import BeautifulSoup, SoupStrainer
from gooey import Gooey
from argparse import ArgumentParser

@Gooey(program_name="Book Extractor 1.0")

# https://www.8novels.net/classics/u6082.html

def main():
	parser = ArgumentParser()

	parser.add_argument('Book_Name', help="Name to save text as")
	parser.add_argument('Number_of_Pages', help="Number of pages over which the text is distributed")
	parser.add_argument('URL', help="URL of the text you want to parse")

	args = parser.parse_args()
	
	# Create .txt file
	file = open(str(args.Book_Name)+".txt","w") 
	
	# Get url
	y = str(args.URL)
	
	# Get number of pages
	x = int(args.Number_of_Pages)

	# Split url
	start = y.find('http://')
	end = y.find('index') + 5
	path = y[start:end]

	# Loop through pages
	for a in range(1, x+1):
		# Use split url to form complete url
		if a == 1:
			url = Request('http://' + str(path) + str(code) + '.html', headers={'User-Agent': 'Mozilla/5.0'})
		else:
			url = Request('http://' + str(path) + str(code) + '_' + str(a) +'.html', headers={'User-Agent': 'Mozilla/5.0'})

		# Read html
		html = urlopen(url).read()

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
	
main()






