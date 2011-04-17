import web

urls = (
    '/','index'
    )
app = web.application(urls, globals())

class index:
    def GET(self):
        return "Hey Dude"

if __name__ == '__main__':
    app.run()
