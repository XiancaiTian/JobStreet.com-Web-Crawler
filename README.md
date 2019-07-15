# jobstreet crawler

This is a simple web crawler written in Python.
Before running the script, please install **requests**, **BeautifulSoup** and **pandas** modules first.


### Packages installation guidelines

run the following command in terminal

	pip install requests

	pip install BeautifulSoup

	pip install pandas


### Running the crawler

1) Download jobstreet_crawler.py file from the repo.

2) Change the **key_words** parameters to a list of job roles you want to crawl, e.g., key_words = ['data scientist', 'java developer']

3) Run the following command in terminal, after crawling a .csv file will be generated for each key word (a sample output file can be found under the repo as well):

		python jobstreet_crawler.py

Notice: this script doesn't require any of your jobstreet.com account information
