# import the modules 
import praw 
import requests
import json

# initialize with appropriate values 
client_id = "Client Id here" 
client_secret = "Client Secret" 
username = "Account Username" 
password = "Account Password" 
user_agent = "User Agent" 
  
# creating an authorized reddit instance 
reddit = praw.Reddit(client_id = client_id,  
                     client_secret = client_secret,  
                     username = username,  
                     password = password, 
                     user_agent = user_agent) 

print('Started...')

while True:
    try:
        inbox = reddit.inbox.unread(limit=None) #getting all mentions

        for item in inbox: #iterating through all mentions
            if item.was_comment and item.new:
                if 'u/firstpostfinder' in item.body.lower():
                    stripped = item.body.replace('u/FirstPostFinder', '')
                    if '\me' in stripped: #if the user wants to see their own post
                        try: #request data from PushShift API for mention in interation
                            data = requests.get(f'https://api.pushshift.io/reddit/search/submission/?author={item.author.name}&sort=asc&size=10')
                            assert data.status_code == 200
                            data = json.loads(data.content)
                            FirstPostName = data['data'][0]['title']
                            FirstPostLink = data['data'][0]['full_link']
                            # mentioning
                            item.reply(f'The first post by {item.author.name} is: \n >*{FirstPostName}* \n\n and it can be found here: \n >{FirstPostLink} \n *** \n ^If ^you ^find ^any ^bugs/issue ^please ^contact ^my ^[Creator](https://www.reddit.com/user/Jackhammer_YOUTUBE). \n ^Please ^upvote ^this ^comment ^to ^help ^improve ^this ^bot.')
                            print(item.author.name)
                            item.mark_read()
                        except IndexError as e:
                            print(e)
                            item.reply(f'I could not find any posts by u/{item.author.name} \n *** \n ^If ^you ^find ^any ^bugs/issue ^please ^contact ^my ^[Creator](https://www.reddit.com/user/Jackhammer_YOUTUBE). \n ^Please ^upvote ^this ^comment ^to ^help ^improve ^this ^bot.')
                            item.mark_read()

                    elif '\sub' in stripped: #if the user wants to see post of a subreddit comment was mentioned in
                        try:
                            subredditName = item.parent().subreddit.display_name
                            data = requests.get(f'https://api.pushshift.io/reddit/search/submission/?&sort=asc&size=10&subreddit={subredditName}')
                            assert data.status_code == 200
                            data = json.loads(data.content)
                            FirstPostName = data['data'][0]['title']
                            FirstPostLink = data['data'][0]['full_link']
                            item.reply(f'The first post in {subredditName} is: \n >*{FirstPostName}* \n\n and it can be found here: \n >{FirstPostLink} \n *** \n ^If ^you ^find ^any ^bugs/issue ^please ^contact ^my ^[Creator](https://www.reddit.com/user/Jackhammer_YOUTUBE). \n ^Please ^upvote ^this ^comment ^to ^help ^improve ^this ^bot.')
                            print(item.author.name)
                            item.mark_read()
                        except IndexError as e:
                            print(e)
                            item.reply(f'I could not find any posts in r/{subredditName} \n *** \n ^If ^you ^find ^any ^bugs/issue ^please ^contact ^my ^[Creator](https://www.reddit.com/user/Jackhammer_YOUTUBE). \n ^Please ^upvote ^this ^comment ^to ^help ^improve ^this ^bot.')
                            item.mark_read()

                    elif '\sub' not in stripped and '\me' not in stripped and '\\u/' in stripped: #if the user wants to see another user's post
                        WordList = stripped.split(' ')
                        for word in WordList:
                            if '\\u/' in word:
                                try:
                                    Name = word.replace('\\u/', '')
                                    Name = Name.replace('\\' , '')
                                    data = requests.get(f'https://api.pushshift.io/reddit/search/submission/?&sort=asc&size=10&author={Name}')
                                    assert data.status_code == 200
                                    data = json.loads(data.content)
                                    FirstPostName = data['data'][0]['title']
                                    FirstPostLink = data['data'][0]['full_link']
                                    item.reply(f'The first post by {Name} is: \n >*{FirstPostName}* \n\n and it can be found here: \n >{FirstPostLink} \n *** \n ^If ^you ^find ^any ^bugs/issue ^please ^contact ^my ^[Creator](https://www.reddit.com/user/Jackhammer_YOUTUBE). \n ^Please ^upvote ^this ^comment ^to ^help ^improve ^this ^bot.')
                                    item.mark_read()
                                    print("Success")
                                except IndexError as e:
                                    print(e)
                                    item.reply(f'I could not find any posts by u/{Name} \n *** \n ^If ^you ^find ^any ^bugs/issue ^please ^contact ^my ^[Creator](https://www.reddit.com/user/Jackhammer_YOUTUBE). \n ^Please ^upvote ^this ^comment ^to ^help ^improve ^this ^bot.')
                                    item.mark_read()

                    elif '\sub' not in stripped and '\me' not in stripped and '\\r/' in stripped: #if the user wants to see another subreddit's post
                        WordList = stripped.split(' ')
                        for word in WordList:
                            if '\\r/' in word:
                                try:
                                    Name = word.replace('\\r/', '')
                                    Name = Name.replace('\\' , '')
                                    data = requests.get(f'https://api.pushshift.io/reddit/search/submission/?&sort=asc&size=10&subreddit={Name}')
                                    assert data.status_code == 200
                                    data = json.loads(data.content)
                                    FirstPostName = data['data'][0]['title']
                                    FirstPostLink = data['data'][0]['full_link']
                                    item.reply(f'The first post in {Name} is: \n >*{FirstPostName}* \n\n and it can be found here: \n >{FirstPostLink} \n *** \n ^If ^you ^find ^any ^bugs/issue ^please ^contact ^my ^[Creator](https://www.reddit.com/user/Jackhammer_YOUTUBE). \n ^Please ^upvote ^this ^comment ^to ^help ^improve ^this ^bot.')
                                    item.mark_read()
                                    print("Success")
                                except IndexError as e:
                                    print(e)
                                    item.reply(f'I could not find any posts in r/{Name} \n *** \n ^If ^you ^find ^any ^bugs/issue ^please ^contact ^my ^[Creator](https://www.reddit.com/user/Jackhammer_YOUTUBE). \n ^Please ^upvote ^this ^comment ^to ^help ^improve ^this ^bot.')
                                    item.mark_read()
        
    except Exception as e:
        print(e)
                                
print('Execution Stopped...')