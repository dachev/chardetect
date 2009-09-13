import chardet
import cgi
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch 

class MainPage(webapp.RequestHandler):
  def get(self):
    #self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write("""
      <!doctype html>
      <html>
        <head>
          <style>
            html, body {
              width:100%;
              height:100%;
              padding:0;
              margin:0;
              text-align:center;
            }
            
            form {
              position:absolute;
              top:50%;
              left:50%;
              width:600px;
              height:100px;
              margin:-150px 0 0 -300px;
              padding: 75px 0 0 0;
              border:1px solid #AAA;
              background-color:#DDD;
            }

            #urlFormUrl {
              width:250px;
            }
          </style>
        </head>
        <body>
          <form id="urlForm" action="api/detect">
            <label for="urlFormUrl">url of the resource to detect:</label>
            <input id="urlFormUrl" type="text" name="url" value="http://" />
            <input type="submit" value="detect">
          </form>
        </body>
      </html>
    """)

class DetectPage(webapp.RequestHandler):
  def get(self):
    #self.response.headers['Content-Type'] = 'text/plain'
    url = cgi.escape(self.request.get('url'))

    try:
      response = urlfetch.fetch(url)
      result   = chardet.detect(response.content)
    except Exception, e:
      self.response.out.write({'status':'error', 'message':e.message})
      return

    result['status'] = 'success'
    self.response.out.write(result)
    

application = webapp.WSGIApplication(
    [
      ('/', MainPage),
      ('/api/detect', DetectPage)
    ],
    debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
