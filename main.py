from flask import Flask, request

from search import search

app = Flask(__name__)


@app.route('/')
def main():
    """ Main page """
    user = request.args.get('user')
    watchers = request.args.get('watchers', type=int, default=0)
    return search(user, watchers)


if __name__ == '__main__':
    app.run()
