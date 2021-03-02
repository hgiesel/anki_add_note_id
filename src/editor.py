from re import sub

from aqt.gui_hooks import editor_will_load_note

from .utils import keep_setting_keyword

def get_hider_js(id: int):
    return f'getEditorField(`{id}`).style.display = "none"; '

def get_const_js(id: int):
    return f'document.body.querySelector(`#f{id}`).setAttribute("contenteditable", false); '

def hide_noteid_fields_and_fix_content(js, note, editor):
    flds = note.model()['flds']
    newjs = js

    keep = editor.mw.col.get_config(keep_setting_keyword, False)

    for fid, fld in enumerate(flds):
        if 'meta' in fld and fld['meta'] == 'noteid':
            newjs += '; '
            newjs += get_hider_js(fid) if editor.addMode else get_const_js(fid)

            # fix noteid in case it was changed by accident or created on mobile
            if not editor.addMode and not keep:
                fld_name = fld['name']
                newjs = sub(f'"{fld_name}", ".*?"', f'"{fld_name}", "{note.id}"', newjs)


    return newjs

def init_editor():
    editor_will_load_note.append(hide_noteid_fields_and_fix_content)
