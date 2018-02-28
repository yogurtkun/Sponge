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
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'code')))


import main
import unittest
import db

class MainTest(unittest.TestCase):
    """This class uses the Flask tests app to run an integration test against a
    local instance of the server."""

    def setUp(self):
        self.app = main.app.test_client()

    def test_hello_world(self):
        rv = self.app.get('/')
        print(rv.data)
        assert("hello" in rv.data.lower())

    def test_configuration(self):
        assert(main.connect_db() == '(1, 1)')

    def test_registerUser(self):
        user = {"username":"testUser", "password":"1234", "email":"test@domain.com", "zipcode":"10026"}
        rv = self.app.post("/registerUser", form=user, follow_redirects=True)
        assert b'User exists!' not in rv.data
        assert db.searchUser("testUser")
        rv = self.app.post("/registerUser", form=user, follow_redirects=True)
        assert b'User exists!' in rv.data
        db.deleteUser("testUser")



if __name__ == '__main__':
    unittest.main()