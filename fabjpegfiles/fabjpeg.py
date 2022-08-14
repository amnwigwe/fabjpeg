from email import header
from urllib.parse import urlencode
import requests
import json
import tweepy
import os
from datetime import datetime
import time
import pytz

while True:
    # DATE
    country_time_zone = pytz.timezone('Asia/Seoul')
    country_time = datetime.now(country_time_zone)
    korean_date = country_time.strftime("%y%m%d")
    korean_time = country_time.strftime("%-I:%M:%S %p")
    print(country_time.strftime("%y%m%d"), country_time.strftime("%I:%M:%S%p"))

    # API KEYS
    FABJPEG_TWITTER_API_KEY = 'jnLAvuQgqChXL24HrN688eAOz'
    FABJPEG_TWITTER_API_SECRET = '5QiW480Cf3D5dSNIinAMFvARo4KWIx4lIxig5WiCU1g7IeahNT'

    FABJPEG_ACCESS_TOKEN = '1538224687125241864-5IWuxFO1NN9Qhl4IgOTc8NB1tRiZ95'
    FABJPEG_ACCESS_TOKEN_SECRET = 's3GYjwmvVcmZI9KW7dNuV9DYYJrFrwmFWDtSkC4G5pDMR'

    FABJPEG_CLIENT_ID = 'ZlVka1k0LU91SVo3TEZLWGRCM1E6MTpjaQ'
    FABJPEG_CLIENT_SECRET = 'wiSMs9L5RFyD8pIVJgAnN9loAy23I1gqGdm1AXi8EL-l5-REAK'

    fab_user_agent = 'fab|android|playstore|1.2.1|10|Android SDK built for x86|google|en|US'
    API_URL = 'https://vip-fab-api.myfab.tv/fapi'
    login_endpoint = '/2/signin'
    artist_endpoint = '/2/groups/1'

    email = '14theopensource@gmail.com'
    pw = 'lufallyares123!A'

    data_object = {
        'email': email,
        'password': pw
    }

    data_encoded = urlencode(data_object)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'user-agent': fab_user_agent
    }

    resultado = requests.post(API_URL + login_endpoint, data = data_encoded, headers=headers)

    # def get_artists_endpoint():
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'user-agent': fab_user_agent
    # }
    #     return headers

    # (don't think I need the get artists endpoint function?)

    resultado = requests.get(API_URL + artist_endpoint, data = data_encoded, headers=headers)
    #print(json.dumps(resultado.json(), indent=4))

    # FOR WRITING THE JSON OBJECT INTO LOONA_PROFILES.JSON
    jsonString = json.dumps(resultado.json(), indent=4)
    jsonFile = open("loona_profiles.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

    json_object = json.loads(jsonString)
    #print(json_object["group"]["artistUsers"][0]["profileImage"])


    ###### FUNCTIONS FOR READING JSON OBJECT AND EXTRACTING IMAGE URLS
    def iterate_through_json_object():
        profile_image_links = []
        banner_image_links = []
        i = 0
        loona_list = json_object["group"]["artistUsers"]
        for i in range((len(loona_list))):
            profile_image_links.append(json_object["group"]["artistUsers"][i]["profileImage"])
            banner_image_links.append(json_object["group"]["artistUsers"][i]["artist"]["bannerImage"])
        return profile_image_links, banner_image_links
    #print(iterate_through_json_object())
    ### declaration of arrays for comparison at the end
    profile_image_array_list, banner_image_array_list = iterate_through_json_object()

    ###### FUNCTIONS FOR THE TWITTER API, POSTING WITH MEDIA
    def twitter_api():
        auth = tweepy.OAuthHandler(FABJPEG_TWITTER_API_KEY, FABJPEG_TWITTER_API_SECRET)
        auth.set_access_token(FABJPEG_ACCESS_TOKEN, FABJPEG_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        return api

    def tweet_new_photo(url, message):
        print("tweeting new photo")
        tweet1 = twitter_api()
        filename = 'temp.jpg'
        request = requests.get(url, stream=True)
        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            tweet1.update_status_with_media(message, filename) ## this is the call the posts the tweet, filename is the image
            os.remove(filename)
        else:
            print("error to upload photo")

    ### returns a string of which girl changed their pfp, according to the index of the image_array_list, as it is in order
    def girl_of_the_post(girl):
        string_girl = ""
        if (girl == 0):
            string_girl = "JHJ"
        elif (girl == 1):
            string_girl = "KHJ"
        elif (girl == 2):
            string_girl = "CHS"
        elif (girl == 3):
            string_girl = "IYJ"
        elif (girl == 4):
            string_girl = "WKH"
        elif (girl == 5):
            string_girl = "KJE"
        elif (girl == 6):
            string_girl = "JJS"
        elif (girl == 7):
            string_girl = "CYR"
        elif (girl == 8):
            string_girl = "HSY"
        elif (girl == 9):
            string_girl = "KJW"
        elif (girl == 10):
            string_girl = "PCW"
        else:
            string_girl = "SHJ"
        return string_girl

    #### while true is so it keeps running (i'll be using pythonanywhere so that it automatically runs)

    print("testing to run 25s")
    time.sleep(25) ## code waits 25 seconds before running
    resultado1 = requests.get(API_URL + artist_endpoint, data = data_encoded, headers=headers)
    #print(json.dumps(resultado.json(), indent=4))

    # FOR WRITING THE JSON OBJECT INTO LOONA_PROFILES.JSON
    jsonString1 = json.dumps(resultado1.json(), indent=4)
    jsonFile1 = open("loona_profiles.json", "w")
    jsonFile1.write(jsonString1)
    jsonFile1.close()

    json_object1 = json.loads(jsonString1)

    for i in range(12): # for each element in range 0-11
        if (profile_image_array_list[i] != json_object1["group"]["artistUsers"][i]["profileImage"]): #image array list the return from the function iterate_through_json_object
            url = json_object1["group"]["artistUsers"][i]["profileImage"]
            message = "[" + korean_date + "]" + "\n" + korean_time + " KST" + "\n" + girl_of_the_post(i) + " has uploaded a new profile picture!"
            tweet_new_photo(url, message) # function call for tweeting a photo + tweet
            print(url) #for testing

        if (banner_image_array_list[i] != json_object1["group"]["artistUsers"][i]["artist"]["bannerImage"]):
            url1 = json_object1["group"]["artistUsers"][i]["artist"]["bannerImage"]
            message1 = "[" + korean_date + "]" + "\n" + korean_time + " KST" + "\n" + girl_of_the_post(i) + " has uploaded a new banner image!"
            tweet_new_photo(url1, message1)
            print(url)
