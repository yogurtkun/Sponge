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
from flask import Flask
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'code')))


import main
import unittest
import account, post
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
            assert b"Post Details" in rv.data
            postdata = {"title":"test", "description":"wanna buy test", "category":"Books"}
            rv = self.app.post("/NewBuyerPost", data=postdata, follow_redirects=True)
            assert b"Post Details" in rv.data
            print "seller and buyer post creating and viewing details pass\n"


    def test_postList(self):
        pass

            


if __name__ == '__main__':
    unittest.main()