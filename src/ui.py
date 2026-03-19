from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, DataTable, Static, Label, Input, Button, LoadingIndicator
from textual.binding import Binding
from textual.screen import Screen, ModalScreen
from textual import work

class AddJobDetailModal(ModalScreen):
    """ Modal screen for showing job details """

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]

    def __init__(self, sql_engine, job_id):
        super().__init__()
        self.sql_engine = sql_engine
        self.job_id = job_id

    def compose(self) -> ComposeResult:
        yield Container(
            Vertical(
                Label(str(self.job_id), id="modal_title"),
                LoadingIndicator(id="loading_indicator"),
                Horizontal(
                    Label("Job Title:"),
                    Label("", id="job_title"),
                    id="job_title_container",
                ),
                Horizontal(
                    Label("Company:"),
                    Label("", id="company_name"),
                    id="company_container"
                ),
                Horizontal(
                    Label("Location:"),
                    Label("", id="location"),
                    id="location_container"
                ),
                id="modal_content"
            ),
            id="modal_dialog"
        )
        yield Footer()

    def on_mount(self) -> None:
        #self.query_one('#guid_input', Input).focus()
        self._load_job_detail()

    @work(thread=True)
    def _load_job_detail(self) -> None:
        data = self.sql_engine.get_job(self.job_id)

        self.app.call_from_thread(self._populate_form, data)

    def _populate_form(self, data) -> None:
        self.query_one('#loading_indicator', LoadingIndicator).display = False

        if data is None:
            self.query_one('#modal_title', Label).update(
                f"View Job #{self.job_id}  not found"
            )
            return

        self.query_one("#job_title", Label).update(data.title)
        self.query_one("#company_name", Label).update(data.company)
        self.query_one("#location", Label).update(data.location)

    def action_cancel(self) -> None:
        self.dismiss(None)

class ResourceView(Screen):
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("a", "show_detail", "Show Job Details"),
    ]

    def __init__(self, resouce_type: str, sql_engine, request_handler):
        super().__init__()
        self.resource_type = resouce_type
        self.sql_engine = sql_engine
        self.request_handler = request_handler

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Vertical(
                DataTable(id="job_table"),
                id="left_panel"
            ),
            id="main_container"
        )
        yield Footer()

    def on_mount(self) -> None:
        job_table = self.query_one("#job_table", DataTable)
        job_table.cursor_type = "row"
        job_table.zebra_stripes = True
        job_table.focus()

        self.setup_job_table(job_table)
        self.load_job_data(job_table)

    def setup_job_table(self, table: DataTable) -> None:
        """Setup episode table columns"""
        table.add_columns(
            "Id",
            "Title", 
            "company", 
            "location", 
            "Link", 
            "list_date"
        )

    def load_job_data(self, table: DataTable) -> None:
        data = self.sql_engine.get_jobs()
        for item in data:
            table.add_row(*item)


    def action_show_detail(self) -> None:
        """Show detail modal"""

        def handle_request(request):
            pass

        job_table = self.query_one('#job_table', DataTable)

        if job_table.has_focus:
            row_key = job_table.cursor_row
            row = job_table.get_row_at(row_key)

            id = row[0]
            
            self.app.push_screen(AddJobDetailModal(self.sql_engine, id), handle_request)


    def action_quit(self) -> None:
        self.app.exit()

