from .field_dialog import init_field_dialog
from .addcards import init_addcards
from .editor import init_editor
from .addon_manager import init_addon_manager

def init():
    init_field_dialog()
    init_addcards()
    init_editor()
    init_addon_manager()
