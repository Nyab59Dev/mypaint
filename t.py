from lib.gibindings import Gdk

# keymap = Gdk.Keymap.get_default()
# disp = Gdk.Display.get_default()
#" disp = Gdk.Display.open_default_libgtk_only()
display_manager = Gdk.DisplayManager.get()
disp = display_manager.get_default_display()
keymap = Gdk.Keymap.get_for_display(disp)
print(keymap.get_entries_for_keycode(65))
print(disp.get_n_monitors())
print(disp.get_name())
print(keymap)

# disps = Gdk.DisplayManager().list_displays()
# print(dir(disp))

bound, keyval, effective_group, level, consumed_modifiers = (
    keymap.translate_keyboard_state(
        65,
        0,
        1
    ))

print(f'keyval : {keyval}')