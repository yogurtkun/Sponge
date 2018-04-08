import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "code")))

import main
import account, post, message
import random

'''
Add fake data to database for testing and demo

This script should only be executed once after reseting database
'''

users = []
sellerPosts = []
buyerPosts = []

reviews = []
messages = []

users.append({"username": "MaxWilson", "email": "mw2333@sponge.com", "password": "1234", "zipcode":" 10001"})
users.append({"username": "IreneNash", "email": "in2333@sponge.com", "password": "1234", "zipcode":" 10002"})
users.append({"username": "CarlLyman", "email": "cl2333@sponge.com", "password": "1234", "zipcode":" 10003"})
users.append({"username": "system", "email": "system@sponge.com", "password": "1234", "zipcode":" 10000"})

sellerPosts.append({"title": "A brand new handbag", "category":"Beauty", "price":800, "location": "New York", "image": "bag.jpg", "description": "I just bought a handbag. But its color is different from what I expected. So I want to sell it to someone else. This bag is brand new and never used outside. its original price is $1000. I can give a discount. PM me if you want:)"})
sellerPosts.append({"title": "Macbook pro 15 inch 2016", "category": "Electronics", "price" : 666, "location": "Seattle", "image": "mbp.jpg", "description": "This mbp has been used for two years but still in good condition. Not a good choice for gaming but enough for browsing websites and writing documents. Prefer local transaction. Online transaction is acceptable only if the buyer has good credit history."})

buyerPosts.append({"title": "Need a cheap ipad air", "category": "Electronics", "price": 100, "location": "Los Angeles", "image": "ipad.jpg", "description": "I need a used ipad for studying. I don't want to bring laptop to school every day cuz it's too heavy. It's ok if your ipad is not in good condition as long as it can function well. PM me for detail if you are interested."})

with main.app.app_context():
    # add users
    for user in users:
        account.registerUser(user["username"], user["email"], user["password"], user["zipcode"])
        message.sendMessage(receiver=user["username"], content="Hello, "+user["username"] + ". Welcome to sponge!")

    # add posts
    for item in sellerPosts:
        image = open(os.path.join("image", item["image"]), "r")
        post.createPost(item["title"], item["description"], item["category"], item["price"], item["location"], image.read(), random.choice(users)["username"], "Seller")
        image.close()
    for item in buyerPosts:
        image = open(os.path.join("image", item["image"]), "r")
        post.createPost(item["title"], item["description"], item["category"], item["price"], item["location"], image.read(), random.choice(users)["username"], "Buyer")
        image.close()