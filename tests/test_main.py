# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys
import os.path
import re
import json
from flask import Flask, jsonify
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'code')))


import main
import unittest
import account, post, message
import schema

class MainTest(unittest.TestCase):
    """This class uses the Flask tests app to run an integration test against a
    local instance of the server."""

    def setUp(self):
        self.app = main.app.test_client()
        self.app.get("/logout")
        with main.app.app_context():
            post.deleteSellerPostByUser("testUser")
            post.deleteBuyerPostByUser("testUser")
            account.deleteUser("testUser")


    #def test_hello_world(self):
    #    rv = self.app.get('/')
    #    print(rv.data)
    #    assert("hello" in rv.data.lower())

    def test_database_connection(self):
        with main.app.app_context():
            db = main.schema.db
            res = str(db.session.execute("select * from test").first())
            assert(res == '(1, 1)')
            print "database connection pass\n"

    def test_registerUser(self):
        with main.app.app_context():
            user = {"username":"testUser", "password":"1234", "email":"test@domain.com", "zipcode":"10026"}
            rv = self.app.post("/registerUser", data=user, follow_redirects=True)
            assert b'User exists!' not in rv.data
            assert account.searchUser("testUser")
            rv = self.app.post("/registerUser", data=user, follow_redirects=True)
            assert b'User exists!' in rv.data
            print "user registration pass\n"


    def test_loginUser(self):
        with main.app.app_context():
            account.registerUser("testUser", "test@domain.com", "1234", "10025")
            user = {"username":"testUser", "password":"1234"}
            rv = self.app.post("/loginUser", data=user, follow_redirects=True)
            assert b'Wrong password!' not in rv.data
            assert b'User doesn\'t exist!' not in rv.data
            user = {"username":"testUser", "password":"666"}
            rv = self.app.post("/loginUser", data=user, follow_redirects=True)
            assert b'Wrong password!' in rv.data
            account.deleteUser("testUser")
            user = {"username":"testUser", "password":"1234"}
            rv = self.app.post("/loginUser", data=user, follow_redirects=True)
            assert b'User doesn\'t exist!' not in rv.data
            print "user login pass\n"

    def test_userPortal(self):
        with main.app.app_context():
            # user portal display
            user = {"username":"testUser", "password":"1234", "email":"test@domain.com", "zipcode":"10025"}
            rv = self.app.get('/portal')
            assert b"portal" not in rv.data
            self.app.post("/registerUser", data = user)
            self.app.get("/logout")
            rv = self.app.get('/portal')
            assert b"portal" not in rv.data
            self.app.post("/loginUser", data = user)
            rv = self.app.get('/portal')

            # user portal update
            update = {"username":user['username'], "zipcode":"10027"}
            rv = self.app.post('/updateUser', data=update)
            assert(rv.data == 'Success')


            #self.app.post("/loginUser", data=user, follow_redirects=True)
            #postdata = {"title":"test", "description":"wanna sell test", "category":"Books"}
            #self.app.post("/NewSellerPost", data=postdata, follow_redirects=True)
            #rv = self.app.post("/getPostsByUser/" + user["username"])
            #print rv.data
            print "user portal pass\n"


    def test_createPost_getPost(self):
        with main.app.app_context():
            account.registerUser("testUser", "test@domain.com", "1234", "10025")
            user = {"username":"testUser", "password":"1234"}
            self.app.post("/loginUser", data=user, follow_redirects=True)
            postdata = {"title":"test", "description":"wanna sell test", "category":"Books"}
            rv = self.app.post("/NewSellerPost", data=postdata, follow_redirects=True)
            assert b"postId=" in rv.data
            postdata = {"title":"test", "description":"wanna buy test", "category":"Books"}
            rv = self.app.post("/NewBuyerPost", data=postdata, follow_redirects=True)
            assert b"postId=" in rv.data
            print "seller and buyer post creating and viewing details pass\n"


    def test_postList(self):
        with main.app.app_context():
            account.registerUser("testUser", "test@domain.com", "1234", "10025")
            user = {"username":"testUser", "password":"1234"}
            self.app.post("/loginUser", data=user, follow_redirects=True)
            postdata = {"title":"test_sellerpost", "description":"wanna sell test", "category":"Books"}
            self.app.post("/NewSellerPost", data=postdata, follow_redirects=True)
            postdata = {"title":"test_buyerpost", "description":"wanna buy test", "category":"Books"}
            self.app.post("/NewBuyerPost", data=postdata, follow_redirects=True)
            self.app.get('/logout')
            rv = self.app.post('/postlist/seller')
            assert 'test_sellerpost' in rv.data
            rv = self.app.post('/postlist/buyer')
            assert 'test_buyerpost' in rv.data
            print 'post list pass\n'


    def test_favorite(self):
        with main.app.app_context():
            account.registerUser("testUser", "test@domain.com", "1234", "10025")
            user = {"username":"testUser", "password":"1234"}
            self.app.post("/loginUser", data=user, follow_redirects=True)
            postdata = {"title":"test", "description":"wanna sell test", "category":"Books"}
            rv = self.app.post("/NewSellerPost", data=postdata, follow_redirects=True)
            res = re.findall("postId=\d+#", rv.data)
            assert len(res) == 1
            postId = res[0][7:-1]
            postdata = {"postId":postId, "postType":"Seller"}
            rv = self.app.post("/favorite", data=postdata, follow_redirects=True)
            assert "Adding to favorites succeeded!" == rv.data
            rv = self.app.post("/deleteFavorite", data=postdata, follow_redirects=True)
            assert "Deleting a favorite item succeeded!" == rv.data
            print "Adding and deleting favorite posts pass\n"


    def test_order(self):
        with main.app.app_context():
            account.registerUser("testUser", "test@domain.com", "1234", "10025")
            user = {"username":"testUser", "password":"1234"}
            self.app.post("/loginUser", data=user, follow_redirects=True)
            postdata = {"title":"test", "description":"wanna sell test", "category":"Books"}
            rv = self.app.post("/NewSellerPost", data=postdata, follow_redirects=True)
            res = re.findall("postId=\d+#", rv.data)
            assert len(res) == 1
            postId = res[0][7:-1]
            postdata = {"postId":postId, "transactionType":"Face to Face"}
            rv = self.app.post("/checkout", data=postdata, follow_redirects=True)
            assert "Placeing order succeeded!" == rv.data
            print "Place order pass\n"

    def test_message(self):
        with main.app.app_context():
            account.registerUser("testSender", "tests@domain.com", "1234", "10025")
            account.registerUser("testReceiver", "testr@domain.com", "1234", "10025")
            message.sendMessage(sender="testSender", receiver="testReceiver", title="message_title", content="message_content")
            assert "message_title" in  json.dumps(message.getMessages(sender="testSender", receiver="testReceiver"))
            assert "message_content" in  json.dumps(message.getMessagesByUser("testSender"))
            assert "message_content" in json.dumps(message.getMessagesByUser("testReceiver"))
            account.deleteUser("testSender")
            account.deleteUser("testReceiver")
            print "message test pass"


    def test_post_review(self):
        with main.app.app_context():
            account.registerUser("testUser", "test@domain.com", "1234", "10025")
            user = {"username":"testUser", "password":"1234"}
            self.app.post("/loginUser", data=user, follow_redirects=True)

            # test seller post review
            data = {"title":"test", "description":"wanna sell test", "category":"Books"}
            rv = self.app.post("/NewSellerPost", data=data, follow_redirects=True)
            res = re.findall("postId=\d+#", rv.data)
            assert len(res) == 1
            postId = res[0][7:-1]
            data = {"postType":"Seller", "postId":postId, "title":"Review test title", "content":"Review test content"}
            rv = self.app.post("/addPostReview", data=data, follow_redirects=True)
            assert "Review succeeded!" in rv.data
            res = re.findall("reviewId=\d+", rv.data)
            assert len(res) == 1
            reviewId = res[0][9:]
            data = {"postType":"Seller", "reviewId":reviewId}
            rv = self.app.post("/delPostReview", data=data, follow_redirects=True)
            assert "Deleting review succeeded!" == rv.data
            #test buyer post review
            data = {"title":"test", "description":"wanna buy test", "category":"Books"}
            rv = self.app.post("/NewBuyerPost", data=data, follow_redirects=True)
            res = re.findall("postId=\d+#", rv.data)
            assert len(res) == 1
            postId = res[0][7:-1]
            data = {"postType":"Buyer", "postId":postId, "title":"Review test title", "content":"Review test content"}
            rv = self.app.post("/addPostReview", data=data, follow_redirects=True)
            assert "Review succeeded!" in rv.data
            res = re.findall("reviewId=\d+", rv.data)
            assert len(res) == 1
            reviewId = res[0][9:]
            data = {"postType":"Buyer", "reviewId":reviewId}
            rv = self.app.post("/delPostReview", data=data, follow_redirects=True)
            assert "Deleting review succeeded!" == rv.data

            print "post review test pass"




if __name__ == '__main__':
    unittest.main()
