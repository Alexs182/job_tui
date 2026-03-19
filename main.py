
from textual.app import App

from src.database import SQLHandler
from src.request import RequestHandler
from src.ui import ResourceView

from style.css import style

class TuiApp(App):
    CSS = style

    def __init__(self, sql_engine, request_handler):
        super().__init__()
        self.sql_engine = sql_engine
        self.request_handler = request_handler

    def on_mount(self) -> None:
        self.push_screen(ResourceView("home", self.sql_engine, self.request_handler))


def main():
    sql_engine = SQLHandler()
    request_handler = RequestHandler()

    app = TuiApp(sql_engine, request_handler)
    app.run()

    #data = RequestHandler().run()

    #for items in data:
    #    sql_engine.insert_job(items)



if __name__ == "__main__":
    main()