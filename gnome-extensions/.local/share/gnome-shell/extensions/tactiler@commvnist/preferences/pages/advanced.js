import GObject from "gi://GObject";
import Gio from "gi://Gio";
import Adw from "gi://Adw?version=1";
import { createColorInput } from "../inputs/color.js";
import { createNumberInput } from "../inputs/number.js";
const TILE_COLORS = [
    { id: "text-color", desc: "Text color" },
    { id: "border-color", desc: "Border color" },
    { id: "background-color", desc: "Background color" },
];
const TILE_SIZES = [
    { id: "text-size", desc: "Text size" },
    { id: "border-size", desc: "Border size" },
    { id: "gap-size", desc: "Gap size" },
];
const GRID_SIZES = [
    { id: "grid-cols", desc: "Columns", min: 1, max: 7 },
    { id: "grid-rows", desc: "Rows", min: 1, max: 5 },
];
export const AdvancedPage = GObject.registerClass(class AdvancedPage extends Adw.PreferencesPage {
    constructor(settings) {
        super({
            title: "Advanced",
            icon_name: "preferences-other-symbolic",
            name: "Advanced",
        });
        this.add(createTileAppearanceGroup(settings));
        this.add(createGridSizeGroup(settings));
        this.add(createBehaviorGroup(settings));
    }
});
function createTileAppearanceGroup(settings) {
    const group = new Adw.PreferencesGroup({
        title: "Tile Appearance",
    });
    TILE_COLORS.forEach((color) => {
        group.add(createColorRow(settings, color.id, color.desc));
    });
    TILE_SIZES.forEach((size) => {
        group.add(createNumberRow(settings, size.id, size.desc));
    });
    return group;
}
function createGridSizeGroup(settings) {
    const group = new Adw.PreferencesGroup({
        title: "Grid Size",
    });
    GRID_SIZES.forEach((size) => {
        group.add(createNumberRow(settings, size.id, size.desc, size.min, size.max));
    });
    return group;
}
function createBehaviorGroup(settings) {
    const group = new Adw.PreferencesGroup({
        title: "Behavior",
    });
    group.add(createSwitchRow(settings, "maximize", "Maximize window when possible"));
    group.add(createSwitchRow(settings, "debug", "Log debug information to journal"));
    return group;
}
function createColorRow(settings, id, title) {
    const input = createColorInput(settings, id);
    const row = new Adw.ActionRow({
        title,
        activatable_widget: input,
    });
    row.add_suffix(input);
    return row;
}
function createNumberRow(settings, id, title, min = 0, max = 1000) {
    const input = createNumberInput(settings, id, min, max);
    const row = new Adw.ActionRow({
        title,
        activatable_widget: input,
    });
    row.add_suffix(input);
    return row;
}
function createSwitchRow(settings, id, title) {
    const row = new Adw.SwitchRow({
        title,
    });
    settings.bind(id, row, "active", Gio.SettingsBindFlags.DEFAULT);
    return row;
}
