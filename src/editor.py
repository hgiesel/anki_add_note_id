from re import sub

from aqt.gui_hooks import editor_will_load_note

from .utils import reduce_setting_keyword, reduce_value

def get_hider_js(id: int):
    return (
        f'document.body.querySelector(`#name{id}`).style.display = "none"; ' +
        f'document.body.querySelector(`#f{id}`).style.display = "none"; '
    )

def get_const_js(id: int):
    return f'document.body.querySelector(`#f{id}`).setAttribute("contenteditable", false); '

def hide_noteid_fields_and_fix_content(js, note, editor):
    flds = note.model()['flds']
    newjs = js

    reduce = editor.mw.col.get_config(reduce_setting_keyword, False)

    for fid, fld in enumerate(flds):
        if 'meta' in fld and fld['meta'] == 'noteid':
            # fix content
            fld_name = fld['name']
            noteid = note.id - reduce_value if reduce else note.id
            newjs = sub(f'"{fld_name}", ".*?"', f'"{fld_name}", "{noteid}"', newjs)

            # fix if noteid was not correctly set (e.g. created on mobile)
            newjs += '; '
            newjs += get_hider_js(fid) if editor.addMode else get_const_js(fid)

    return newjs

def init_editor():
    editor_will_load_note.append(hide_noteid_fields_and_fix_content)
