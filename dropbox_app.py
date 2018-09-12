"""
Joshua Tanke - Dropbox App submission
9/9/18
"""

import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
from dropbox import DropboxOAuth2FlowNoRedirect
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import json
import os
import sys


# retrieve the app's credentials
json_data = open("credentials.json").read()
credentials = json.loads(json_data)
APP_KEY = credentials['APP_KEY']
APP_SECRET = credentials['APP_SECRET']

dbx = None

# Allows user to generate an auth token
def authorize_user():

    auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
    authorize_url = auth_flow.start()
    print("1. Go to: " + authorize_url)
    print("2. Click \"Allow\" (you might have to log in first).")
    print("3. Copy the authorization code.")
    auth_code = input("Enter the authorization code here: ").strip()

    try:
        oauth_result = auth_flow.finish(auth_code)
    except Exception as e:
        print('Error: {}'.format(e))
        exit(1)
        
    global dbx
    dbx = dropbox.Dropbox(oauth_result.access_token)

# validates the folder name string
def is_valid_folder_name(name):
    return re.match("^[A-Za-z0-9_-]*$", name) and name != ''

# uploads an image url to a given folder
def upload_data(folder_name, file_name, url):

    try:
        path = '/' + folder_name + '/' + file_name
        dbx.files_save_url(path, url)
    except ApiError as err:
        print(err)


# drives the logic of the program
def driver():

    authorize_user()

    # creates a google image search query
    query = input("Enter an image search: ")
    query = query.split()
    query ='+'.join(query)
    url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    
    # creates a new folder in dropbox 
    folder_name = input("Enter a folder name: ")
    folders = [folder.name.lower() for folder in dbx.files_list_folder('').entries]
    while folder_name.lower() in folders or not is_valid_folder_name(folder_name):
        folder_name = input("That name is taken or invalid. Enter new a folder name: ")
    print('Creating dropbox folder...')
    dbx.files_create_folder_v2('/' + folder_name)

    print('Launching Chrome...')
    # launches the chrome webdriver
    browser = webdriver.Chrome()
    browser.get(url)

    # scrolls down the page to load more images
    print('Loading images...')
    for _ in range(1000):
        browser.execute_script("window.scrollBy(0,10000)")

    # uncomment the following lines for more images but less reliability
    # browser.find_element_by_id('smb').click()
    # for _ in range(10000):
    #     browser.execute_script("window.scrollBy(0,10000)")

    # scrapes the images and uploads them to dropbox 
    print('Uploading images to dropbox...')
    counter = 0
    for x in browser.find_elements_by_xpath('//div[contains(@class,"rg_meta")]'):
        counter += 1
        img_url = json.loads(x.get_attribute('innerHTML'))["ou"]
        file_name = query + '_' + str(counter) + '.jpg'
        upload_data(folder_name, file_name, img_url)

        sys.stdout.write("\rImages uploaded: %d" % counter)
        sys.stdout.flush()
    print('\nDone.')

    browser.close()



if __name__ == "__main__":
    driver()




