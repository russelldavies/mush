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

from google.appengine.ext import db
import pygpw

class Url(db.Model):
  # The model for the URL
  url = db.LinkProperty(required=True)
  shortcode = db.StringProperty()
  creation_time = db.DateTimeProperty(auto_now_add=True)
  hitcount = db.IntegerProperty(default = 0)
  referrers = db.StringListProperty()

def generate(url):
  # Generate initial shortcode
  shortcode = pygpw.generate(1, 8, 'trigraph').pop()

  # Keep generating new shortcodes until there is a unique one
  while (Url.gql("WHERE shortcode = :1 LIMIT 1", shortcode)).count(1) > 0:
    shortcode = pygpw.generate(1, 8, 'trigraph').pop()

  # Create new URL entity and store
  #referrer = self.request.environ['HTTP_REFERER'] \
  #  if 'HTTP_REFERER' in self.request.environ else  None
  #new = Url(url = url, shortcode = shortcode, hitcount = 1)
  new = Url(url = url, shortcode = shortcode)
  new.put()

  return shortcode

def get_shortcode(url):
  # Query for entity based on url. If found return shortcode
  # otherwise generate shortcode
  query = Url.gql("WHERE url = :1 LIMIT 1", url)
  if query.count(1) > 0:
    return query.fetch(1)[0].shortcode
  else:
    return generate(url)
        
def get_url(shortcode):
  # Query for entity based on shortcode and return corresponding URL
  # or return nothing if no record
  query = Url.gql("WHERE shortcode = :1 LIMIT 1", shortcode)
  if query.count(1) > 0:
      return query.fetch(1)[0].url
  return None

def update_hitcount(shortcode):
  url_query = Url.gql("WHERE shortcode = :1 LIMIT 1", shortcode)
  url_result = url_query.fetch(1)
  url = url_result[0]
  hits = url.hitcount
  hits += 1
  url.hitcount = hits
  url.put()
