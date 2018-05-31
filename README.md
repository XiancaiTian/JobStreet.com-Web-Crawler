# job street crawler

This is a web crawler written in Python. You will have to install request, BeautifulSoup and pandas before you can use it.


### Install requests

run the following command in terminal

	pip install requests

### Install BeautifulSoup

run the following command in terminal
	
	pip install BeautifulSoup

### Install pandas

run the following command in terminal
	
	pip install pandas


### Running the crawler

1) Download jobstreet_crawler.py file from the repo.

2) Change the **key_words** parameters to a list of job roles you want to crawl, e.g., key_words = ['data scientist', 'java developer']

3) Run the following in terminal, and a .csv file with crawled data will be generated for each key word:
	
python jobstreet_crawler.py

* runnning this script doesn't need any of your jobstreet.com account information

