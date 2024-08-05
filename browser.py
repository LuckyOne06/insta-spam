from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from fake_useragent import UserAgent

user_agent = UserAgent().random
while "Iphone" not in user_agent and "Android" not in user_agent and "iPhone" not in user_agent:
    user_agent = UserAgent().random

print(user_agent)
options = webdriver.ChromeOptions()
options.add_argument(r"") #--user-data-dir=C:\Users\YOUR PC NAME\AppData\Local\Google\Chrome\User Data
options.add_argument(r'') #--profile-directory=Profile 2
options.add_argument(f'user-agent={user_agent}')


driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)
