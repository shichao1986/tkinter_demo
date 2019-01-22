#coding:utf-8

# 本例程基于python2.7.13

import Tkinter
import ttk
import tkMessageBox
import web
import ctypes
import sys
import json
import threading

urls = (
    '/write/barcode', 'WriteBarcode'
)

app = web.application(urls, globals())

class WriteBarcode:
    def __init__(self):
        # self.pt = BarcodePrinter()
        pass

    def GET(self, *args, **kwargs):
        return 'hello world!'

    def POST(self, *args, **kwargs):
        '''

        :param args:
        :param kwargs:
        :return:

        payload:
        {"textcode":"aaa", "text_x":10, "text_y":5,"barcode":{"data1":"123","data2":"asdf"}, "bar_x":30,"bar_y":20}
        '''
        payload = json.loads(web.data())
        MyAPP.logout(payload)
        try:
            if payload.get('textcode', None):
                text_data = payload['textcode']
                text_x = payload.get('text_x', 10)  # default text x is 10
                text_y = payload.get('text_y', 2)  # default text y is 5
                # self.pt.text(text_data, i_x=text_x, i_y=text_y)

            if payload.get('barcode', None):
                bar_data = json.dumps(payload['barcode'])
                bar_x = payload.get('bar_x', 30)  # default text x is 10
                bar_y = payload.get('bar_y', 12)  # default text y is 5
                # self.pt.qrcode(bar_data, i_x=bar_x, i_y=bar_y)

            # self.pt.print_out()
        except Exception as e:
            MyAPP.logout(e)
            MyAPP.logout('print barcode failed!')

        return 'OK'

APP_WINDOW = '600x400+200+200'
APP_TITLE = 'wei.py服务端'


def func(server='127.0.0.1', port=8080, api='/write/barcode'):
    urls = (api, 'WriteBarcode')
    app = web.application(urls, globals())
    app.run()

class MyWeb(threading.Thread):
    def __init__(self, server='127.0.0.1', port=8080, api='/write/barcode'):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.server=server
        self.port=port
        self.api=api
        self.app = None
        self.is_stoped = False
        self.initialized = False

    def init_app(self):
        if self.app is None:
            urls = (self.api, 'WriteBarcode')
            if len(sys.argv) == 1:
                sys.argv.append('{}:{}'.format(self.server, self.port))
            elif len(sys.argv) == 2:
                sys.argv[1] = '{}:{}'.format(self.server, self.port)
            self.app = web.application(urls, globals())

    def run(self):
        try:
            while not self.is_stoped:
                self.app.run()
        except Exception as e:
            MyAPP.logout('e')
            MyAPP.logout('Server start failed!')
            return

        MyAPP.logout('Server stoped!')

    def start(self):
        self.init_app()
        self.is_stoped = False
        if not self.initialized:
            threading.Thread.start(self)
            self.initialized = True
        else:
            pass

    def stop(self):
        self.is_stoped = True
        self.app.stop()
        self.app = None

class MyAPP(Tkinter.Frame):
    @classmethod
    def logout(cls, logstr=''):
        cls.loghandler.insert(Tkinter.END, '\n{}'.format(logstr))
        # 此处可以增加判断鼠标焦点是否在文档的最末尾，如果在最末尾或者无焦点则将执行yview_moveto
        # 否则不执行，这样做是为了便于阅读log
        cls.loghandler.yview_moveto(1)

    def _start_web(self):
        server = self.entry_server.get()
        if server.lower() == 'localhost':
            server = '127.0.0.1'
        port = self.entry_port.get()
        api = self.entry_api.get()
        if self.web_t is None:
            self.web_t = MyWeb(server=server, port=port, api=api)
        self.web_t.start()

        self.btn_start.config(state=Tkinter.DISABLED)
        self.btn_end.config(state=Tkinter.NORMAL)
        self.entry_server.config(state=Tkinter.DISABLED)
        self.entry_port.config(state=Tkinter.DISABLED)
        self.entry_api.config(state=Tkinter.DISABLED)
        self.__class__.logout('Start Web server at {}:{}, api is {}'.format(server, port, api))

    def _end_web(self):
        MyAPP.logout('Stop Server...')

        if self.web_t is not None:
            self.web_t.stop()
            self.web_t = None

        self.btn_start.config(state=Tkinter.NORMAL)
        self.btn_end.config(state=Tkinter.DISABLED)
        self.entry_server.config(state=Tkinter.NORMAL)
        self.entry_port.config(state=Tkinter.NORMAL)
        self.entry_api.config(state=Tkinter.NORMAL)



    def __init__(self):
        self.app = Tkinter.Tk()
        Tkinter.Frame.__init__(self, master=self.app)
        self.app.geometry(APP_WINDOW)
        self.app.title(APP_TITLE)
        # self.app.iconbitmap(APP_LOGO)
        self.web_t = None

        # 标签
        self.title_server = Tkinter.Label(self.app, text='Server')
        self.title_server.config(font='Helvetica -15 bold', fg='blue')
        self.title_server.place(x=50, y=20, anchor="center")

        self.title_port = Tkinter.Label(self.app, text='Port')
        self.title_port.config(font='Helvetica -15 bold', fg='blue')
        self.title_port.place(x=350, y=20, anchor="center")

        self.title_api = Tkinter.Label(self.app, text='API')
        self.title_api.config(font='Helvetica -15 bold', fg='blue')
        self.title_api.place(x=50, y=60, anchor="center")

        # 输入框
        default_server = Tkinter.StringVar()
        default_server.set('localhost')
        self.entry_server = Tkinter.Entry(self.app, textvariable=default_server)
        self.entry_server.place(x=90, y=10, width=200)

        default_port = Tkinter.IntVar()
        default_port.set(8080)
        self.entry_port = Tkinter.Entry(self.app, textvariable=default_port)
        self.entry_port.place(x=390, y=10, width=50)

        default_api = Tkinter.StringVar()
        default_api.set('/write/barcode')
        self.entry_api = Tkinter.Entry(self.app, textvariable=default_api)
        self.entry_api.place(x=90, y=50, width=200)

        # 按钮
        self.btn_start = Tkinter.Button(self.app, text='启动Server', command=self._start_web)
        self.btn_start.place(x=145, y = 100)
        self.btn_start.config(state=Tkinter.NORMAL)

        self.btn_end = Tkinter.Button(self.app, text='终止Server', command=self._end_web)
        self.btn_end.place(x=345, y=100)
        self.btn_end.config(state=Tkinter.DISABLED)

        # 消息
        self.message_log0 = Tkinter.Text(self.app, background='gray', borderwidth=1)
        self.message_log0.place(x=30, y=150, width=558, height=220)

        self.message_log = Tkinter.Text(self.app, background='gray', borderwidth=1)
        self.message_log.place(x=30, y= 150, width=540, height=220)
        setattr(self.__class__, 'loghandler', self.message_log)

        # 消息框滚动条
        self.scrollbar_msg = Tkinter.Scrollbar(self.message_log0)
        self.scrollbar_msg.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
        # 绑定消息框和scrollbar
        self.message_log['yscrollcommand'] = self.scrollbar_msg.set
        self.scrollbar_msg['command'] = self.message_log.yview

if __name__ == '__main__':
    ap = MyAPP()
    ap.mainloop()