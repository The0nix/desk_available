import tkinter
import requests
from PIL import Image, ImageTk

CHECK_INTERVAL = 5
CHECK_TIMEOUT = 5
API_URL = 'http://localhost:8080/getcome'

UNAVAILABLE_MESSAGE = 'Не могу достучаться до интернета. Не знаю, придёт ли сегодня Тамерлан :('
UNKNOWN_MESSAGE = 'Тамерлан ещё сам не понял, придёт ли он сегодня'
WONT_COME_MESSAGE = 'Тамерлан сегодня не придёт. Место свободно'
WILL_COME_MESSAGE = 'Тамерлан сегодня придёт {when}'


class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
    def toggle_geom(self, event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom


def check_api() -> str:
    try:
        r =  requests.get(API_URL, timeout=CHECK_TIMEOUT)
        data = r.json()
        if str(data) == 'unknown':
            return UNKNOWN_MESSAGE
        if not data['will_come']:
            return WONT_COME_MESSAGE
        return WILL_COME_MESSAGE.format(when=data['come_time'])
    except requests.RequestException:
        return UNAVAILABLE_MESSAGE


if __name__ == '__main__':
    root = tkinter.Tk()
    app = FullScreenApp(root)
    root.configure(background='black')

    text_label = tkinter.Label(
        root,
        text='',
        compound='center',
        bg='black',
        fg='white',
        font=("Courier", 44)
    )
    text_label.place(relx=.5, rely=.5,anchor=tkinter.CENTER)

    def update_label():
        text = check_api()
        text_label.config(text=text)
        root.after(CHECK_INTERVAL * 1000, update_label)
    update_label()

    root.mainloop()
