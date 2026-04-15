const MIN_GRID_COLUMNS = 1;
const MAX_GRID_COLUMNS = 7;
const MIN_GRID_ROWS = 1;
const MAX_GRID_ROWS = 5;
export class Layout {
    cols;
    rows;
    gapsize;
    constructor(cols, rows, gapsize) {
        this.cols = cols;
        this.rows = rows;
        this.gapsize = gapsize;
    }
    static prefix(n) {
        // For legacy reasons, layout 1 does not have a prefix
        if (n === 1) {
            return "";
        }
        return `layout-${n}-`;
    }
    static fromSettings(settings, n) {
        const num_cols = clamp(settings.get_int("grid-cols"), MIN_GRID_COLUMNS, MAX_GRID_COLUMNS);
        const num_rows = clamp(settings.get_int("grid-rows"), MIN_GRID_ROWS, MAX_GRID_ROWS);
        const cols = [];
        const rows = [];
        const prefix = Layout.prefix(n);
        for (let col = 0; col < num_cols; col++) {
            cols.push(settings.get_int(`${prefix}col-${col}`));
        }
        for (let row = 0; row < num_rows; row++) {
            rows.push(settings.get_int(`${prefix}row-${row}`));
        }
        const gapsize = settings.get_int("gap-size");
        return new Layout(cols, rows, gapsize);
    }
}
function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
}
