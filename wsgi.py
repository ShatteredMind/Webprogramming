import os
import sys

top = "<div class='top'>Middleware TOP</div>"
bottom =  "<div class='botton'>Middleware BOTTOM</div>"

def simple_app(environ, start_response):
    
    path = '.' + environ['PATH_INFO']
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    if not os.path.isfile(path):
        path = './index.html'
    file = open(path,'r')
    page = file.read()
    file.close()
    start_response(status, headers)
    page = page.encode('utf-8')
    return [page]

class Middleware(object):
    def __init__(self, simple_app):
        self.simple_app = simple_app

    def __call__(self, environ, start_response):
        page = self.simple_app(environ, start_response)[0]

        page = page.decode("utf-8")
        result = ""
        result += page[:page.rfind("<body>")]
        result += top
        result += page[page.rfind("<body>"):page.find("</body>")]
        result += bottom
        result += page[page.find("</body>"):]
        return [result.encode("utf-8")]

    
if __name__ == '__main__':
    try:
        from wsgiref.simple_server import make_server
        simple_app = Middleware(simple_app)
        _server = make_server('localhost', 8080, simple_app)
        print ("Serving localhost on port 8080...")
        _server.serve_forever()
    except KeyboardInterrupt:
        print('See you around')