import requests

user_name = input("Enter the github user name: ")
request = requests.get(f'https://api.github.com/users/{user_name}/repos')

with open('git_hub.json','wb') as f:
     f.write(request.content)
