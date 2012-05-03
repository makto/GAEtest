#!/usr/bin/env python
#

import cgi
import os

from google.appengine.ext.webapp import template
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

app = webapp2.WSGIApplication([
            ('/', MainHandler),
            ('/rot13/', Rot13Handler)
        ], debug=True)
