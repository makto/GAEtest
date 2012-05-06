#!/usr/bin/env python

import os
import re

from google.appengine.ext.webapp import template
from google.appengine.ext import db
import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('Hello, Udacity!')

        
class Rot13Handler(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'rot13.html')
        self.response.out.write(template.render(path, {}))
    
    def post(self):
        raw_text = self.request.get('text')
        trans_text = []
        
        for letter in raw_text:
            ord_of_letter = ord(letter)
            if 90 >= ord_of_letter >= 65:
                new_ord = ord_of_letter + 13
                if new_ord > 90:
                    new_ord = new_ord % 90 + 64
                new_letter = chr(new_ord)
            elif 122 >= ord_of_letter >= 97:
                new_ord = ord_of_letter + 13
                if new_ord > 122:
                    new_ord = new_ord % 122 + 96
                new_letter = chr(new_ord)
            else:
                new_letter = letter
            trans_text.append(new_letter)
        
        paras = {'trans_text' : ''.join(trans_text)}
        
        path = os.path.join(os.path.dirname(__file__), 'rot13.html')
        self.response.out.write(template.render(path, paras))

        
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
class SignupHandler(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'signup.html')
        self.response.out.write(template.render(path, {}))
        
    def post(self):
        path = os.path.join(os.path.dirname(__file__), 'signup.html')
        
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        
        error_username = ''
        error_password = ''
        error_email = ''
        error_verify = ''
        if not USER_RE.match(username):
            error_username = "That's not a valid username."
        if not PASSWD_RE.match(password):
            error_password = "That wasn't a valid password."
        elif password != verify:
            error_verify = "Your passwords didn't match."
        if ( email ) and ( not EMAIL_RE.match(email) ):
            error_email = "That's not a valid email."
        
        error_and_raw = {'error_username' : error_username,
                    'error_password' : error_password,
                    'error_email' : error_email,
                    'error_verify' : error_verify,
                    'raw_username' : username,
                    'raw_email' : email}
        
        if error_username or error_password or error_email or error_verify:
            self.response.out.write(template.render(path, error_and_raw))
        else:
            self.redirect('/welcome/?username=%s' % username)

        
class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.out.write("Welcome, %s" % username)
    
class Blog(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    datetime = db.DateTimeProperty(auto_now_add = True)

class BlogHandler(webapp2.RequestHandler):
    def get(self):
        blogs = db.GqlQuery("select * from Blog order by datetime desc")
        path = os.path.join(os.path.dirname(__file__), 'blog.html')
        self.response.out.write(template.render(path, {'posts' : blogs}))
    
    
class CreatePostHandler(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'blog_create.html')
        self.response.out.write(template.render(path, {}))
    
    def post(self):
        path = os.path.join(os.path.dirname(__file__), 'blog_create.html')
        subject = self.request.get('subject')
        content = self.request.get('content')
        if not ( subject and content ):
            self.response.out.write(template.render(path, 
                {'subject_raw' : subject, 'content_raw' : content, 'error' : 'no blank!'}))
        else:
            new_post = Blog(subject = subject, content = content)
            tmp = new_post.put()
            self.redirect('/blog/%d' % tmp.id())


class EntryHandler(webapp2.RequestHandler):
    def get(self, post_id):
        path = os.path.join(os.path.dirname(__file__), 'blog_entry.html')
        post = Blog.get_by_id(int(post_id))
        self.response.out.write(template.render(path, {'post' : post}))


app = webapp2.WSGIApplication([
            ('/', MainHandler),
            ('/rot13/', Rot13Handler),
            ('/signup/', SignupHandler),
            ('/welcome/', WelcomeHandler),
            ('/blog', BlogHandler),
            ('/blog/newpost', CreatePostHandler),
            ('/blog/(\d+)', EntryHandler)
        ], debug=True)
