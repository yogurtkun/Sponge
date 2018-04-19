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
users.append({"username": "Jessica", "email": "jessica@sponge.com", "password": "1234", "zipcode":" 10025"})
users.append({"username": "Johnson", "email": "johnson@sponge.com", "password": "1234", "zipcode":" 10025"})
users.append({"username": "yjc", "email": "yjc@123.com", "password": "1234", "zipcode":" 10025"})
users.append({"username": "system", "email": "system@sponge.com", "password": "1234", "zipcode":" 10000"})

sellerPosts.append({"title": "A brand new handbag", "category":"Beauty", "price":800, "location": "New York", "image": "bag.jpg", "description": "I just bought a handbag. But its color is different from what I expected. So I want to sell it to someone else. This bag is brand new and never used outside. its original price is $1000. I can give a discount. PM me if you want:)"})
sellerPosts.append({"title": "Macbook pro 15 inch 2016", "category": "Electronics", "price" : 666, "location": "Washington", "image": "mbp.jpg", "description": "This mbp has been used for two years but still in good condition. Not a good choice for gaming but enough for browsing websites and writing documents. Prefer local transaction. Online transaction is acceptable only if the buyer has good credit history."})
sellerPosts.append({"title": "Yamaha digial piano", "category": "Music", "price" : 750, "location": "Arizona", "image": "piano.jpg", "description": "I bought this piano 4 years ago, and I am considering to buy a grand piano. Though this piano has used for 4 years, it still in good condition. The official price is $1500."})
sellerPosts.append({"title": "Ducal Chest of Drawer", "category": "Furniture", "price" : 99, "location": "Texas", "image": "drawer.jpg", "description": "I am about to leave this city, and the drawer is not easy to move. The drawer has been used for 3 years, but still in good condition. The price is negotiable because I prefer buyer come and pick it up. Please let me know if you are interested."})
sellerPosts.append({"title": "Air conditioner", "category": "Furniture", "price" : 139, "location": "Texas", "image": "air.jpg", "description": "I am about to leave this city and want to sell this air conditioner. It has been used for 1 years, but still in good condition. I clean it every month, so you don't need to worry about cleanliness.Please let me know if you are interested."})
sellerPosts.append({"title": "Drone", "category": "Electronics", "price" : 500, "location": "Texas", "image": "dji.jpg", "description": "I buy the dji drone for my son. However, it seems like that he is not old enough to play it. The drone is in well condition. It can continuous fly for nearly 4 hour. Prefer face to face."})
sellerPosts.append({"title": "Camera", "category": "Electronics", "price" : 200, "location": "Ohio", "image": "camera.jpg", "description": "A well preserved camera which has been used for 2 years. The brand is XXX."})

buyerPosts.append({"title": "Need a cheap ipad air", "category": "Electronics", "price": 100, "location": "California", "image": "ipad.jpg", "description": "I need a used ipad for studying. I don't want to bring laptop to school every day cuz it's too heavy. It's ok if your ipad is not in good condition as long as it can function well. PM me for detail if you are interested."})
buyerPosts.append({"title": "Want a mountain bike", "category": "Outdoor", "price": 250, "location": "New Jersey", "image": "bike.jpg", "description": "My previous mountain bike has some unfixable damage, such that I want to buy a new mountain bike. I don't need a really new bike, but please make sure your bike is safe to ride. Your bike should be the same style as the image attached."})
buyerPosts.append({"title": "Want a limited edition shoes", "category": "Clothing", "price": 1000, "location": "Iowa", "image": "shoes.jpg", "description": "I forgot the date of release. And when I remember, it is out of stock in all the stores. If anyone has this shoes, I would like to provide a competitive price."})
buyerPosts.append({"title": "Want a second-hand book", "category": "Books", "price": 10, "location": "New York", "image": "book.jpg", "description": "A course I recently take asks me to buy a book about spark. I prefer the book in better condition without any draft on it. BTW, prefer to deal face to face."})
buyerPosts.append({"title": "Want a second-hand GPU", "category": "Electronics", "price": 1000, "location": "New York", "description": "I want a XXX' GPU to play games. It will be better if it has been used less than 1 year."})

with main.app.app_context():
    # add users
    for user in users:
        if user['username'] == 'system':
            users.remove(user)
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