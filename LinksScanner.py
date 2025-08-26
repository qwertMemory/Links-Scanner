import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from colorama import init, Fore
from sys import argv

#definition of color constants
RED = Fore.RED
ORANGE = "\033[38;5;214m"
GREEN = Fore.GREEN
CLOSE_FORMAT = "\033[0m"

#initializing colorama
init()

def get_page (url) :
	try :
		page = requests.get(url, 
			headers = {
			"User_Agent" : UserAgent().random,
			"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
			}).content.decode()
	except requests.exceptions.ConnectionError :
		raise SystemExit(RED + f"ERROR : can't connect to {url}")
	except requests.exceptions.MissingSchema :
		raise SystemExit(RED + f"ERROR : the url address ({url}) isn't valid (try to use : https://{url})")

	return page


class LinksScanner :

	def __init__ (self, url, args) :

		self.__tags = args
		self.__url = url

		#validation
		if not self.__url :
			raise SystemExit(RED + "ERROR : url is empty, exiting...\n")
		if not self.__tags :
			print(ORANGE + "WARNING : tags are empty, default value is a tag <a>\n")
			self.__tags = "a"

		self.__links = []
		self.__found_tags = []

	def start_scan (self) :
		
		page = get_page(self.__url)

		soup = BeautifulSoup(page, "lxml")

		attributes = ["href", "src", "meta", "action", "data"]
		for tag in self.__tags :
			
			arr_tag = soup.find_all(tag)

			for i in range(len(arr_tag)) :
				for att in attributes :
					try :
						#ignoring anchors and a root directory
						if arr_tag[i][att][0] != "#" and arr_tag[i][att] != "/":
							self.__links.append(arr_tag[i][att])
							self.__found_tags.append(arr_tag[i])
					except KeyError :
						pass

	def get_links (self) :
		return self.__links

	def get_tags (self) :
		return self.__found_tags

if __name__ == "__main__" :

	try :
		scanner = LinksScanner(argv[1], argv[2:])
	#if argv doesnt receive enough arguments
	except IndexError :
		raise SystemExit(RED + "ERROR : arguments are empty, exiting...\n")
	

	scanner.start_scan()

	links = scanner.get_links()
	tags = scanner.get_tags()

	print("\n<tag> | link in a tag\n")
	for i in range(len(links)) :

		print(GREEN + f"<{tags[i].name}> |", links[i])

	

