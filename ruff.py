# import requests

# def get_token(username, password):
    
#     endpoint = "https://smhri.com/oeccrm/api/user/login/"

#     request = requests.post(endpoint, data={"username":username, "password":password})
    
#     if request.status_code == 200:
#         print(type(request.status_code))
#         return request.json()
#     else:
#         raise Exception
        

# print(get_token('fly', 'anant@123'))
# import pickle

# with open("fly.pkl", 'rb') as file:
#     name = pickle.load(file)

# print((name['token']['access']))
import ast

x = ['[1,2,3]']
converted_list = ast.literal_eval(x[0])


x = ['[1,2,3]']
