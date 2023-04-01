from sqlitedict import SqliteDict
from panel import fit_data, Panel_template, Panel_update_template
from mergedeep import merge

panel_database = SqliteDict("panels.sqlite", tablename="panels", autocommit=True)

def get_panel(Id):
    if Id not in panel_database:
        return None
    else:
        return panel_database[Id]

def set_panel(data):
    Id = data['id']
    panel_database[Id] = fit_data(data, Panel_template)

def merge_panel(data):
    Id = data['id']
    if Id in panel_database:
        new_data = fit_data(data, Panel_update_template)
        panel_database[Id] = merge(panel_database[Id], new_data)
    else:
        set_panel(data)
