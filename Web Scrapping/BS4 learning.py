import pprint

from bs4 import BeautifulSoup
import requests

# website_html = requests.get("https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=").text
# soup = BeautifulSoup(website_html,"lxml")
# jobs = soup.find("li",class_="clearfix job-bx wht-shd-bx")
# company  = jobs.find("h3",class_="joblist-comp-name").text.replace(" ","").strip()
# skills = jobs.find("span",class_="srp-skills").text.replace(" ","").strip().split(",")
# print(skills)

# website_html = requests.get("https://coinmarketcap.com/").text
# soup = BeautifulSoup(website_html,"lxml")
# jobs = soup.findAll("p",class_="coin-item-symbol")
# # company  = jobs.find("h3",class_="joblist-comp-name").text.replace(" ","").strip()
# # skills = jobs.find("span",class_="srp-skills").text.replace(" ","").strip().split(",")
# print(len(jobs))

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
url ='https://coinmarketcap.com/'
driver.get(url)
elements1 = driver.find_elements(By.CLASS_NAME,"coin-item-symbol")
stable = ["USDT","BUSD","USDC","TUSD","FDUSD","USDD","USDP","USTC"]
top100 = [e.text for e in elements1 if e.text not in stable]

print(top100)
print(len(top100))

