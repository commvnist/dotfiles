import Adw from "gi://Adw?version=1";
import Gio from "gi://Gio";
import Gdk from "gi://Gdk?version=4.0";
import Gtk from "gi://Gtk?version=4.0";
import { ExtensionPreferences } from "resource:///org/gnome/Shell/Extensions/js/extensions/prefs.js";

import { LayoutPage } from "./preferences/pages/layout.js";
import { AdvancedPage } from "./preferences/pages/advanced.js";
import { KeyboardShortcutsPage } from "./preferences/pages/keyboardShortcuts.js";

export default class TactilePreferences extends ExtensionPreferences {
    fillPreferencesWindow(window: Adw.PreferencesWindow) {
        const settings: Gio.Settings = this.getSettings();
        const provider = new Gtk.CssProvider();
        const display = Gdk.Display.get_default();

        provider.load_from_path(this.dir.get_path() + "/prefs.css");

        if (display) {
            Gtk.StyleContext.add_provider_for_display(display, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION);
        }

        window.add(new LayoutPage(settings, 1));
        window.add(new LayoutPage(settings, 2));
        window.add(new LayoutPage(settings, 3));
        window.add(new LayoutPage(settings, 4));
        window.add(new KeyboardShortcutsPage(settings));
        window.add(new AdvancedPage(settings));

        window.set_modal(false);
        window.set_transient_for(null);
        window.set_destroy_with_parent(false);
        window.set_default_size(760, 560);
        window.set_resizable(true);
    }
}
