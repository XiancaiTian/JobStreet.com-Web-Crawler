import requests # data scraping
from bs4 import BeautifulSoup # HTML parser
import pandas as pd


""" get all position <a> tags by a list of key words
<a> tag example:
<a class="position-title-link" id="position_title_3" href="https://www.jobstreet.com.sg/en/job/data-analyst-python-sas-sqlbank-35k-to-5k-gd-bonus5-days-west-6111488?fr=21" 
target="_blank" title="View Job Details - Data Analyst (Python / SAS / SQL)(BANK / $3.5K to $5K + GD BONUS / 5 Days / West)" data-track="sol-job" data-job-id="6111488" 
data-job-title="Data Analyst (Python / SAS / SQL)(BANK / $3.5K to $5K + GD BONUS / 5 Days / West)" data-type="organic" data-rank="3" data-page="1" data-posting-country="SG">
<h2 itemprop="title">Data Analyst (Python / SAS / SQL)(BANK / $3.5K to $5K + GD BONUS / 5 Days / West)</h2></a>"""
def linksByKeys(keys):
    ## keys: a list of strings
    ## return a dictionary of links

    links_dic = {}
    # scrape key words one by one
    for key in keys:
        print('Scraping ',key,' ...')
        links_dic[key] = linksByKey(key)
        print('{} positions found searching with: {}'.format(len(links_dic[key]),key))
    return links_dic


""" get all position <a> tags by a single key word, called by linksByKeys """
def linksByKey(key):
    ## key: a string
    ## return a list of links

    # parameters passed to  http get/post function
    base_url = 'https://www.jobstreet.com.sg/en/job-search/job-vacancy.php'
    pay_load = {'key':'','area':1,'option':1,'pg':None,'classified':1,'src':16,'srcr':12}
    pay_load['key'] = key
    # page number
    pn = 1
    position_links = []
    loaded = True
    while loaded:
        print('Loading page {} ...'.format(pn))
        pay_load['pg'] = pn
        r = requests.get(base_url,params=pay_load)
        # extract position <a> tags
        soup = BeautifulSoup(r.text,'html.parser')
        links = soup.find_all('a',{'class':'position-title-link'})
        # if return nothing, means the function reach the last page, return results
        if not len(links):
            loaded = False
        else:
            position_links += links
            pn += 1
    return position_links


""" process the information of a position <a> tag
<a> tag example:
<a class="position-title-link" id="position_title_3" href="https://www.jobstreet.com.sg/en/job/data-analyst-python-sas-sqlbank-35k-to-5k-gd-bonus5-days-west-6111488?fr=21" 
target="_blank" title="View Job Details - Data Analyst (Python / SAS / SQL)(BANK / $3.5K to $5K + GD BONUS / 5 Days / West)" data-track="sol-job" data-job-id="6111488" 
data-job-title="Data Analyst (Python / SAS / SQL)(BANK / $3.5K to $5K + GD BONUS / 5 Days / West)" data-type="organic" data-rank="3" data-page="1" data-posting-country="SG">"""
def parseLinks(links_dic):
    ## links_dic: a dictionary of links
    ## print final results to .csv file

    for key in links_dic:
        jobs = []
        for link in links_dic[key]:
            jobs.append([key] + parseLink(link))
        # transfrom the result to a pandas.DataFrame
        result = pd.DataFrame(jobs,columns=['key_word','job_id','job_title','country','job_link','company','company_region','company_industry','company_size','experence_requirement','working_location','description'])
        # add a column denoting if the position is posted by a recuriter company
        result['postedByHR'] = result.company_industry.apply(lambda x:True if x and x.find('Human Resources')>-1 else False)
        # save result, 
        file_name = key+'.csv'
        result.to_csv(file_name,index=False)


""" process a single position <a> tag, extract the information, called by parseLinks """
def parseLink(link):
    ## link: single position <a> tag
    ## return a single position

    # unique id assigned to a position
    job_id = link['data-job-id'].strip()
    # job title
    job_title = link['data-job-title'].strip()
    # posted country
    country = link['data-posting-country'].strip()
    # the web address towards to the post detail page
    job_href = link['href']
    # go to post detail page, and fetch information
    other_detail = getJobDetail(job_href)
    return [job_id,job_title,country,job_href] + other_detail


""" extract details from post detail page """
def getJobDetail(job_href):
    ## job_href: a post url
    ## retun post details from the detail page

    print('Scraping ',job_href,'...')
    r = requests.get(job_href)
    soup = BeautifulSoup(r.text,'html.parser')
    # company who post the position, very often is a recuriter company
    company_name = soup.find('div',{'id':'company_name'}).text.strip() if soup.find('div',{'id':'company_name'}) else None
    # years of working experience required
    years_of_experience= soup.find('span',{'id':'years_of_experience'}).text.strip() if soup.find('span',{'id':'years_of_experience'}) else None
    # location of the company
    company_location = soup.find('span',{'id':'single_work_location'}).text.strip() if soup.find('span',{'id':'single_work_location'}) else None
    # industry of the company who post the position, very often is a recuriter company
    company_industry = soup.find('p',{'id':'company_industry'}).text.strip() if soup.find('p',{'id':'company_industry'}) else None
    # size of the company who post the position
    company_size = soup.find('p',{'id':'company_size'}).text.strip() if soup.find('p',{'id':'company_size'}) else None
    # the working location
    job_location = soup.find('p',{'id':'address'}).text.strip() if soup.find('p',{'id':'address'}) else None
    # job description, which contains information about job scope, requirements and sometimes a brief introduction about the comapny
    job_description = soup.find('div',{'id':'job_description'}).text.strip() if soup.find('div',{'id':'job_description'}) else None
    return [company_name,company_location,company_industry,company_size,years_of_experience,job_location,job_description]

def main():
    
    # a list of positions to scrape
    key_words = ['data scientist']
    s = requests.session()
    links_dic = linksByKeys(key_words)
    parseLinks(links_dic)

if __name__ == '__main__':
	main()
