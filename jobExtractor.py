import concurrent.futures
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import time
import concurrent
import asyncio

def extract_content(base_url, count, limit = 20):
    class_name = "title "

    mobile_pattern = r'\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}'
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    with open(f"collected_data_{count}.csv","w") as f:
        f.write('email,phone,company_name,title,link\n')

    for i in range(1, limit + 1):
        driver = Chrome()
        url = base_url + "-" + str(i) + "?experience=2"
        driver.get(url)
        time.sleep(2)

        cards = driver.find_elements(By.CLASS_NAME, class_name)
        print("length of cards on page: ",len(cards))
        for card in cards:
            page_url = card.get_attribute('href')
            if not page_url:
                continue

            driver2 = Chrome()
            driver2.get(page_url)
            time.sleep(2)
            try:
                job_title_xpath = "/html/body/div[1]/div/main/div[1]/div[1]/section[1]/div[1]/div[1]/header/h1"
                company_name_xpath = "/html/body/div[1]/div/main/div[1]/div[1]/section[1]/div[1]/div[1]/div/a"

                jd_section_xpath = "/html/body/div/div/main/div[1]/div[1]/section[2]"

                about_section_xpath = "/html/body/div[1]/div/main/div[1]/div[1]/section[3]"

                job_title = driver2.find_element(By.XPATH, job_title_xpath).text
                company_name = driver2.find_element(By.XPATH, company_name_xpath).text

                jd_text = driver2.find_element(By.XPATH, jd_section_xpath).text
                about_text = driver2.find_element(By.XPATH, about_section_xpath).text

                complete_text = jd_text + '\n' + about_text

                mobno = re.search(mobile_pattern, complete_text)
                if mobno:
                    temp_phone = set([x.group() for x in re.finditer(mobile_pattern, complete_text, re.MULTILINE|re.IGNORECASE)])
                    mob_number = '||'.join(temp_phone)
                else:
                    mob_number = ''
                emailobj = re.search(email_pattern, complete_text)
                if emailobj:
                    temp_mail = set([x.group() for x in re.finditer(email_pattern, complete_text, re.MULTILINE|re.IGNORECASE)])
                    email = '||'.join(temp_mail)
                else:
                    email = ''
                
                if email:
                    with open(f"collected_data_{count}.csv","a") as f:
                        f.write(f"{email},{mob_number},{company_name}, {job_title}, {page_url}\n")
                elif mob_number:
                    with open(f"collected_data_{count}.csv","a") as f:
                        f.write(f"{email},{mob_number},{company_name}, {job_title}, {page_url}\n")
            
            except:
                print(f"error in {page_url}")

    return True

def runner(url_list, name_list, limits):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Submit tasks for each URL
        futures = [executor.submit(extract_content, url, name, limit) for url, name, limit in zip(url_list, name_list, limits)]
        
        # Wait for all tasks to complete
        concurrent.futures.wait(futures)

        # You can process results here if needed
        for future in futures:
            try:
                # If extract_content returns anything, you can get it here
                result = future.result()
                # Process result if needed
            except Exception as e:
                print(f"An error occurred: {e}")
    
    return True



# base_urls = ["https://www.naukri.com/sales-executive-jobs-in-noida", "https://www.naukri.com/sales-executive-jobs-in-gurgaon"]
# runner(base_urls, ['noida', 'gurgaon'])
