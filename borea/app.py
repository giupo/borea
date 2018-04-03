#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import coloredlogs
import json
import tornado.ioloop
import tornado.web

from tornado import gen, locks

log = logging.getLogger(__name__)


class Users(object):
    def __init__(self):
        self.lock = locks.Lock()
        self._users = set([])
        
    @gen.coroutine
    def add(self, name):
        with (yield self.lock.acquire()):
            self._users.update([name])

    @property
    @gen.coroutine
    def users(self):
        with (yield self.lock.acquire()):
            return list(self._users)

    @gen.coroutine
    def remove(self, name):
        with (yield self.lock.acquire()):
            self._users = self._users - set([name])


class MainHandler(tornado.web.RequestHandler):

    @gen.coroutine
    def get(self, name=None):
        if name:
            yield self.application.users.add(name)

        users = yield self.application.users.users
        self.finish(json.dumps(users))
        self.set_header('Content-Type', 'application/json')


class RemoveHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self, name):
        yield self.application.users.remove(name)
        users = yield self.application.users.users
        self.finish(json.dumps(users))
        self.set_header('Content-Type', 'application/json')


def make_app():
    app = tornado.web.Application([
        (r"/(.*)/remove", RemoveHandler),
        (r"/(.*)", MainHandler),
        (r"/", MainHandler),
    ])

    app.users = Users()
    return app


def main():
    coloredlogs.install(level=logging.DEBUG)
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
