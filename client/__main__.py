import requests
import tkinter
from collections.abc import Mapping
from typing import Any

import click
import yaml


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


def check_api(config: Mapping[str, Any]) -> str:
    try:
        r =  requests.get(config['API_URL'], timeout=config['CHECK_TIMEOUT'])
        data = r.json()
        if str(data) == 'unknown':
            return config['UNKNOWN_MESSAGE']
        if not data['will_come']:
            return config['WONT_COME_MESSAGE']
        return config['WILL_COME_MESSAGE'].format(when=data['come_time'])
    except requests.RequestException:
        return config['UNAVAILABLE_MESSAGE']


@click.command()
@click.argument('config_file', type=click.File())
def main(config_file):
    config = yaml.safe_load(config_file)

    root = tkinter.Tk()
    app = FullScreenApp(root)
    root.configure(background='black')

    text_label = tkinter.Label(
        root,
        text='',
        compound='center',
        bg='black',
        fg='white',
        font=("Courier", config['FONT_SIZE'])
    )
    text_label.place(relx=.5, rely=.5,anchor=tkinter.CENTER)

    def update_label():
        text = check_api(config)
        text_label.config(text=text)
        root.after(config['CHECK_INTERVAL'] * 1000, update_label)
    update_label()

    root.mainloop()



if __name__ == '__main__':
    main()
