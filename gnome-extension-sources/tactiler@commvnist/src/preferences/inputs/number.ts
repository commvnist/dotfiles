import Gio from "gi://Gio";
import Gtk from "gi://Gtk?version=4.0";

export function createNumberInput(
    settings: Gio.Settings,
    id: string,
    min: number = 0,
    max: number = 1000,
): Gtk.SpinButton {
    const spin = new Gtk.SpinButton({
        adjustment: new Gtk.Adjustment({
            lower: min,
            upper: max,
            step_increment: 1,
        }),
        numeric: true,
        valign: Gtk.Align.CENTER,
        width_chars: 6,
        visible: true,
    });
    settings.bind(id, spin, "value", Gio.SettingsBindFlags.DEFAULT);
    return spin;
}
