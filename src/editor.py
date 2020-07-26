from aqt.gui_hooks import (
    editor_did_load_note,
)

def get_hider_js(id: int):
    return f"""
        document.body.querySelector("#name{id}").style.display = "none"
        document.body.querySelector("#f{id}").style.display = "none"
    """

def get_const_js(id: int):
    return f"""
        document.body.querySelector("#f{id}").setAttribute("contenteditable", false);
    """

def hide_noteid_fields(editor):
    flds = editor.note.model()['flds']

    for id, fld in enumerate(flds):
        if 'meta' in fld and fld['meta'] == 'noteid':
            editor.web.eval(get_hider_js(id) if editor.addMode else get_const_js(id))


def init_editor():
    editor_did_load_note.append(hide_noteid_fields)
