# scrapping the data from the website

from bs4 import BeautifulSoup
import json
from playwright.sync_api import sync_playwright
import re
import time

pattern = r"[a-zA-Z0-9_\.-]+@[a-zA-Z0-9_-]+\.(co\.in|com|co|in|org|biz|work|net)" ##$%&'*+/=?^_`{|}~-

pattern1 = r"(((\+91[\-\s]?)?0?[6-9]\d{9})|(\d{10}))"
# pattern1 = r"(\+91[\-\s]?)?0?[6-9]\d{9}"
pnum = 2 #page number for webaite

#variables to store the data (reference purpose only)
count = 0
skip = 0
dic = {"phone": [],"mail":[],"company_name":[],"title":[],"link":[]}

#create a csv file to store the data
if pnum == 2:
  with open('data2.csv', 'w') as f:
      f.write("email,phone,company_name,title,link\n")


#playwright session is started to scrape the data from url using playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=100)
    page = browser.new_page()
    page1 = browser.new_page()
    while pnum < 200:
      base_url = r"https://www.naukri.com/sales-executive-jobs-in-noida?k=sales%20executive&l=noida%2C%20gurugram%2C%20delhi%20%2F%20ncr&experience=2"
      # url = r"https://www.naukri.com/jobs-in-india-3?functionAreaIdGid=2&functionAreaIdGid=7&functionAreaIdGid=9&functionAreaIdGid=14&jobAge=3"
      url = r"https://www.naukri.com/sales-executive-jobs-in-noida-"+str(pnum)+r"?k=sales%20executive&l=noida%2C%20gurugram%2C%20delhi%20%2F%20ncr&experience=2"
      url2 = r"https://www.naukri.com/sales-executive-jobs-in-noida-"+str(pnum)
      url3= r"https://www.naukri.com/sales-executive-jobs-in-noida-"+str(pnum) #+r"?k=inside%20sales%2C%20inside%20sales%20executive&l=mumbai&nignbevent_src=jobsearchDeskGNB"
      page.goto(url3)
      # page.wait_for_timeout(4000)
      time.sleep(4)
      content = page.content()
      soup = BeautifulSoup(content, 'html.parser')
      jobs = soup.find_all('div', class_='cust-job-tuple layout-wrapper lay-2 sjw__tuple')
      # jobs= soup.find_all('div',class_= 'cust-job-tuple layout-wrapper lay-2 sjw__tuple' )
      print('length of jobs...',len(jobs))
      for job in jobs:
        post_link = job.div.a.attrs['href'] 
        page1.goto(post_link)
        print("link is...",post_link)
        page1.wait_for_timeout(4000)
        soup = BeautifulSoup(page1.content(), 'html.parser')
        #top -> job title #about -> company details
        top = soup.find('section', class_='styles_job-header-container___0wLZ')
        job_desc = soup.find('section', class_='styles_job-desc-container__txpYf')
        about = soup.find('section', class_='styles_about-company__lOsvW')
        try:
          new = top.text + job_desc.text + about.text
          # print(new)
          # extract the email and phone number from the new string
          temp_mail = set([x.group() for x in re.finditer(pattern,new,re.MULTILINE|re.IGNORECASE)])
          temp_phone = set([x.group() for x in re.finditer(pattern1,new,re.MULTILINE|re.IGNORECASE)])
          print("working on ==>", pnum, temp_mail, temp_phone)
          email = '||'.join(temp_mail)
          phone = '||'.join(temp_phone)
          if email != '' or phone != '':
            dic["phone"].append(phone)
            dic["mail"].append(email)
            title = top.find('h1', class_='styles_jd-header-title__rZwM1').text
            cn = top.find('div', class_='styles_jd-header-comp-name__MvqAI').a.text
            dic["company_name"].append(cn)
            dic["title"].append(title)
            dic["link"].append(post_link)
            # print(email,phone,cn,title)
            # update the csv file
            with open('data2.csv', 'a') as f:
                f.write(f"{email},{phone},{cn},{title},{post_link}\n")
        except:
          skip += 1
        count += 1

      pnum += 1
      # break #########
    page1.close()
    page.close()
    browser.close()

json_object = json.dumps(dic, indent = 4)
print(count,skip)
with open("data.json", "w") as outfile:
    outfile.write(json_object)

