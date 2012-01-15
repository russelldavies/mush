#
# Copyright 2011 Russell Davies
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy 
# of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required 
# by applicable law or agreed to in writing, software distributed under the 
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS 
# OF ANY KIND, either express or implied. See the License for the specific 
# language governing permissions and limitations under the License.
#

import cgi
import datetime
import urllib
import wsgiref.handlers
import os

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

from url import *

def server_hostname():
  # Get hostname of server
  if os.environ.get('HTTP_HOST'): 
    return os.environ['HTTP_HOST'] 
  else: 
    return os.environ['SERVER_NAME'] 

class MainHandler(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, None))

class ShortcodeHandler(webapp.RequestHandler):
  def post(self):
    # Get url from index.html input form
    url = self.request.get('url')
    shortcode = get_shortcode(url)
    host = server_hostname()

    template_values = {
      'shortcode': shortcode,
      'url': url,
      'host': host,
    }

    path = os.path.join(os.path.dirname(__file__), 'shortened.html')
    self.response.out.write(template.render(path, template_values))

class StatsHandler(webapp.RequestHandler):
  def get(self):
    query = Url.all()

    template_values = {
        'urls': query,
        'host': server_hostname(),
      }

    path = os.path.join(os.path.dirname(__file__), 'stats.html')
    self.response.out.write(template.render(path, template_values))

class RedirectHandler(webapp.RequestHandler): 
  def get(self, shortcode):
    url = get_url(shortcode)
    if url:
      # Update hitcount and redirect
      update_hitcount(shortcode)
      self.redirect(url)
    else:
      self.response.out.write("Error: there is no match for that URL.")

def main():
  application = webapp.WSGIApplication( [('/', MainHandler),
                                         ('/shorten', ShortcodeHandler),
                                         ('/stats', StatsHandler),
                                         ('/(.*)', RedirectHandler)],
                                         debug=True)

  run_wsgi_app(application)

if __name__ == '__main__':
  main()
