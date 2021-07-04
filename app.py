# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
import speedtest

result_txt = None


class Application:

    def __init__(self):
        global result_txt
        import pprint
        # pprint.pprint(self.server_name())
        # pprint.pprint(self.server_url())
        self.window = Tk()
        result_txt = StringVar()
        result_txt.set("Pressine testar e aguarde.")

        self.window.geometry("480x320")
        # self.window.attributes("-fullscreen", 1)
        self.window.title('Nova Net - RaspTeste')
        self.window.resizable(FALSE, FALSE)
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        self.content = ttk.Frame(self.window, width=470, height=310, padding="3 3 12 12").grid(
            column=0, row=0, sticky=(N, W, E, S))

        self.result_frame = ttk.Frame(
            self.content, width=470, height=110).grid(column=0, row=2)
        self.action_frame = ttk.Frame(
            self.content, width=470, height=110).grid(column=0, row=3)

        self.result_label = ttk.Label(
            self.result_frame, textvariable=result_txt).grid(column=0, row=2)

        self.selection_label = ttk.Label(
            self.result_frame, text = "Selecione o servidor").grid(column=0, row=0)

        self.selected_server = StringVar()
        self.selection_combo = ttk.Combobox(
            self.result_frame, values=self.server_name(), textvariable=self.selected_server, justify="center")
        self.selection_combo.grid(column=0, row=1)
        # self.selection_combo.pack(fill='x', padx=5, pady=5)
        self.selection_combo.bind('<<ComboboxSelected>>', self.server_changed)

        self.button = ttk.Button(
            self.action_frame, text='Testar', command=self.do_test).grid(column=0, row=3)

        self.window.mainloop()

    def convert_to_mb(self, bits):
        self.result = float(bits) / 1000000
        return "{:.2f}".format(self.result)

    def get_servers(self):
        servers = []
        self.s = speedtest.Speedtest()
        servers = self.s.get_closest_servers(servers)

        return servers[0:5]

    def server_name(self):
        servers = self.get_servers()
        server_name = [server['sponsor'] for server in servers]
        return server_name

    def server_url(self, name):
        servers = self.get_servers()
        server_name = [server['url'] for server in servers if server['sponsor'] == name]
        return server_name

    def server_changed(self, event):
        server_name = self.selection_combo.get()
        server_url = self.server_url(server_name)
        print(server_url)
        return server_url

    def do_speedtest(self):

        self.threads = None

        self.s = speedtest.Speedtest()

        self.b_server = self.s.get_best_server()
        self.s.download(threads=self.threads)
        self.s.upload(threads=self.threads)
        self.s.results.share()
        self.results_dict = self.s.results.dict()

        self.results = {
            "server": self.b_server['sponsor'],
            "latency": self.b_server['latency'],
            "upload": self.results_dict['upload'],
            "download": self.results_dict['download']
        }

        return self.results

    def do_test(self):
        global result_txt

        result_txt.set("Aguarde...")

        results_dict = self.do_speedtest()

        if results_dict:
            result_txt.set("""
            Resultado

            Servidor: {}
            Latência: {}ms
            Upload: {}Mb/s
            Download: {}Mb/s
                    """.format(results_dict['server'], results_dict['latency'], self.convert_to_mb(results_dict['upload']), self.convert_to_mb(results_dict['download'])))


if __name__ == '__main__':
    Application()
