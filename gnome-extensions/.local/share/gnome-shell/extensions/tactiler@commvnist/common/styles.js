const DEFAULT_TEXT_COLOR = "rgba(128,128,255,1.0)";
const DEFAULT_BORDER_COLOR = "rgba(128,128,255,0.5)";
const DEFAULT_BACKGROUND_COLOR = "rgba(128,128,255,0.1)";
export class Styles {
    textColor;
    borderColor;
    backgroundColor;
    textSize;
    borderSize;
    constructor(textColor, borderColor, backgroundColor, textSize, borderSize) {
        this.textColor = textColor;
        this.borderColor = borderColor;
        this.backgroundColor = backgroundColor;
        this.textSize = textSize;
        this.borderSize = borderSize;
    }
    static fromSettings(settings) {
        const textColor = settings.get_string("text-color") ?? DEFAULT_TEXT_COLOR;
        const borderColor = settings.get_string("border-color") ?? DEFAULT_BORDER_COLOR;
        const backgroundColor = settings.get_string("background-color") ?? DEFAULT_BACKGROUND_COLOR;
        const textSize = settings.get_int("text-size");
        const borderSize = settings.get_int("border-size");
        return new Styles(textColor, borderColor, backgroundColor, textSize, borderSize);
    }
}
