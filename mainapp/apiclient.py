import requests
import json

#list users which have no profile or are less than 20 characters long
def listuser():
    #using the url form the web api
    url = 'http://127.0.0.1:8000/api/members/'
    response = requests.get(url)
    json = response.json()
    # for each attricbute check whether the profile is blanc
    for attribute in json:
            if(attribute['profile'] == None):
                print(attribute['url'])
            else:
                    url = attribute['profile']
                    response = requests.get(url)
                    json = response.json()
                    if(len(json['text']) < 20):
                            print(json['text'])
#check public messages of users
def listmessage():
    url = 'http://127.0.0.1:8000/api/messages/'
        
    user_input = input("Enter username: ")
    username = "http://127.0.0.1:8000/api/members/"+user_input+"/"
        
    response = requests.get(url)
    json = response.json()
        
    for attribute in json:
        if((attribute['pm'] == True) & (attribute['user'] == username)):
                print(attribute['text'])
    else:
                print ("no public messages")

listuser()
listmessage()
