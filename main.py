#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
import webapp2
import re


form = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
</head>
    <h1>Signup</h1>
<form method="post">
    <label>
        Userame
        <input name="Username">%(params.error_username)s<br>
        <br>
    </label>

    <label>
        Password
        <input name="Password"><br>
        <br>
    </label>

    <label>
        Verify
        <input name="Verify"><br>
        <br>
    </label>

    <label>
        Email
        <input name="Email"><br>
        <br>
    </label>

    <input type="submit">
</form>
</html>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(form)

    def validate_username(self, Username):
        USERNAME_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        if USERNAME_RE.match(Username):
            return Username

    def validate_email(self, Email):
       # allow empty email field
        if not Email:
           return ""

        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        if EMAIL_RE.match(Email):
           return Email

    def validate_password(self, Password):
        PWD_RE = re.compile(r"^.{3,20}$")
        if PWD_RE.match(Password):
            return True
        return False






#def get(self):
#    self.render("user-signup.html")

    def post(self):
        have_error = False
        username = self.request.get('Username')
        password = self.request.get('Password')
        verify = self.request.get('Verify')
        email = self.request.get('Email')

        params = dict(username = username,
                      email = email)

        if not self.validate_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not self.validate_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not self.validate_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True


        if have_error == True:
            self.response.out.write(form.format({"params":params}))
        else:
            self.redirect('/welcome?Username=' + username)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('Username')
        self.response.out.write('Welcome, ' + username)

    def post(self):
        pass


app = webapp2.WSGIApplication([
    ('/', MainHandler), ("/welcome", WelcomeHandler)
], debug=True)
