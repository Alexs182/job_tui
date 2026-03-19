style = """
Screen {
    background: $surface;
}

#main_container {
    width: 100%;
    height: 100%;
    padding: 1;
}

#title {
    width: 100%;
    height: 3;
    content-align: center middle;
    background: $boost;
    margin-bottom: 1;
}

DataTable {
    height: 1fr;
    border: solid $primary;
}

DataTable > .datatable--header {
    background: $primary;
    color: $text;
    text-style: bold;
}

DataTable > .datatable--cursor {
    background: $secondary;
}

AddPodcastModal {
    align: center middle;
}

#modal_dialog {
    width: 60;
    height: auto;
    background: $surface;
    border: thick $primary;
    padding: 0;
}

#modal_content {
    width: 100%;
    height: auto;
    padding: 2;
}

#modal_title {
    width: 100%;
    height: 3;
    content-align: center middle;
    background: $boost;
    margin-bottom: 2;
}

Label {
    margin-top: 1;
    margin-bottom: 0;
}

Input {
    width: 100%;
    margin-bottom: 1;
}

#button_container {
    width: 100%;
    height: auto;
    align: center middle;
    margin-top: 2;
}

Button {
    margin: 0 1;
}
"""