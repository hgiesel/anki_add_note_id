from aqt import mw

from ..gui.custom.settings import Settings
from .utils import reduce_setting_keyword, copy_setting_keyword

def set_settings(reduce_note_id, copy_note_id):
    mw.col.set_config(reduce_setting_keyword, reduce_note_id)
    mw.pm.profile[copy_setting_keyword] = copy_note_id

def show_settings():
    dialog = Settings(mw, set_settings)

    reduce = mw.col.get_config(reduce_setting_keyword, False)
    copy = mw.pm.profile.get(copy_setting_keyword, False)

    dialog.setupUi(reduce, copy)

    return dialog.exec_()

def init_addon_manager():
    mw.addonManager.setConfigAction(__name__, show_settings)
