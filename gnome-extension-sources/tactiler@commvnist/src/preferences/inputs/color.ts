import Gio from "gi://Gio";
import Gtk from "gi://Gtk?version=4.0";
import Gdk from "gi://Gdk?version=4.0";

const DEFAULT_COLOR = "rgba(128,128,255,1.0)";

export function createColorInput(settings: Gio.Settings, id: string): Gtk.Button {
    let rgba = parseColor(settings.get_string(id));

    const button = new Gtk.Button({
        label: "Choose...",
        valign: Gtk.Align.CENTER,
        visible: true,
    });
    updateTooltip(button, rgba);

    button.connect("clicked", () => {
        const dialog = Gtk.ColorChooserDialog.new("Choose Color", null);
        dialog.set_modal(false);
        dialog.set_resizable(true);
        dialog.set_destroy_with_parent(false);
        dialog.set_default_size(720, 520);
        dialog.set_use_alpha(true);
        dialog.set_rgba(rgba);

        dialog.connect("response", (_dialog, response) => {
            if (response === Gtk.ResponseType.OK || response === Gtk.ResponseType.ACCEPT) {
                rgba = dialog.get_rgba();
                settings.set_string(id, rgba.to_string() ?? DEFAULT_COLOR);
                updateTooltip(button, rgba);
            }

            dialog.destroy();
        });

        dialog.present();
    });

    return button;
}

function parseColor(value: string | null): Gdk.RGBA {
    const rgba = new Gdk.RGBA();
    if (!rgba.parse(value ?? DEFAULT_COLOR)) {
        rgba.parse(DEFAULT_COLOR);
    }
    return rgba;
}

function updateTooltip(button: Gtk.Button, rgba: Gdk.RGBA): void {
    button.set_tooltip_text(rgba.to_string() ?? DEFAULT_COLOR);
}
