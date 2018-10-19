from bottle import redirect, response, request, template, route, run, default_app

import os

@route("/static/:path#.+#", name='static')
def test(path):
    return static_file(path, root='static')

@route('/')
def test():

    test = 'テストです！！'

    return template('templates/test', test=test)

if __name__ == '__main__':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
else:
    application = default_app()
