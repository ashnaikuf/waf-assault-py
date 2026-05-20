from selenium import webdriver

import os
from dotenv import load_dotenv
load_dotenv()
driver = webdriver.Chrome() # Or Firefox, Edge, etc.
TARGET_URL = os.getenv("TARGET_URL")
driver.get(TARGET_URL)

# Interact with elements, wait for content to load, etc.
driver.quit()
