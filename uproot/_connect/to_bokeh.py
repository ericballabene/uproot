#!/usr/bin/env python

# Copyright (c) 2017, DIANA-HEP
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import numpy

class TH1Methods_bokeh(object):
    def __init__(self, hist):
        self._hist = hist

    def plot(self, *args, **kwds):
        import bokeh


import threading

class BokehCanvas(object):
    _ioloop = None
    _instance = None

    def __new__(cls, port=None, address=None):
        if cls._ioloop is None:
            from tornado.ioloop import IOLoop
            cls._ioloop = IOLoop.current()
            def go():
                if not cls._ioloop._running:
                    cls._ioloop.start()
            thread = threading.Thread(target=go)
            thread.daemon = True
            thread.start()

        if cls._instance is None:
            cls._instance = cls._new(port, address)

        elif port is not None and port != cls._instance._server.port:
            if not cls._instance._server._stopped:
                cls._instance._server.stop()
            cls._instance = cls._new(port, address)

        elif address is not None and address != cls._instance._server.address:
            if not cls._instance._server._stopped:
                cls._instance._server.stop()
            cls._instance = cls._new(port, address)

        return cls._instance

    @classmethod
    def _new(cls, port, address):
        import bokeh
        import bokeh.application
        import bokeh.application.handlers
        import bokeh.server.server

        self = object.__new__(cls)

        if port is None:
            port = 0
        if address is None:
            address = "0.0.0.0"

        def newwindow(doc):
            fig = bokeh.plotting.figure()
            fig.patch([], [], line_width=0)
            self._layout = bokeh.layouts.row(fig)
            doc.add_root(self._layout)
            self._doc = doc

        print "new server"
        app = bokeh.application.Application(bokeh.application.handlers.function.FunctionHandler(newwindow))
        self._server = bokeh.server.server.Server({"/": app}, port=port, address=address, io_loop=cls._ioloop)
        self._server.start()
        return self

    def __call__(self, plot):
        def update():
            print "update"
            self._layout.children[0] = plot
        self._doc.add_next_tick_callback(update)



from bokeh.plotting import figure

canvas = BokehCanvas(port=5000)

p = figure(plot_width=600, plot_height=600)
p.patch([6, 7, 8, 7, 3], [1, 2, 3, 4, 5], alpha=0.5, line_width=2)



    # def __init__(self, port=0, address="0.0.0.0"):
    #     self._port = port
    #     self._address = address
    #     super(BokehCanvas, self).__init__()
    #     self.daemon = True

    #     from tornado.ioloop import IOLoop
    #     self._loop = IOLoop.current()
    #     self.start()

    #     from bokeh.server.server import Server
    #     from bokeh.application import Application
    #     from bokeh.application.handlers.function import FunctionHandler
    #     from bokeh.plotting import figure
    #     from bokeh.layouts import row

    #     print "launch"

    #     self._doc = None

    #     def newwindow(doc):
    #         print "newwindow"
    #         fig = figure()
    #         fig.patch([], [], line_width=0)
    #         self._layout = row(fig)
    #         doc.add_root(self._layout)
    #         self._doc = doc

    #     server = Server({"/": Application(FunctionHandler(newwindow))},
    #                     port=self._port, address=self._address, io_loop=self._loop)

    #     print "server start"
    #     server.start()

    # @property
    # def plot(self):
    #     return self._layout.children[0]

    # @plot.setter
    # def plot(self, newplot):
    #     def update():
    #         self._layout.children[0] = newplot
    #     print "update"
    #     doc = self._doc
    #     if doc is not None:
    #         doc.add_next_tick_callback(update)

    # def run(self):
    #     print "loop thread"
    #     if not self._loop._running:
    #         self._loop.start()
