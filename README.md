# dotfiles

## quirks

### tempwatch

This is a function that is sourced in the .zshrc that *probably* only works on my laptop. It requires the `lm-sensors` package to be installed and configured.

After installing the package, run the following command, saying YES to everything >>

```
sensors-detect
```

Afterwards, call the function with `tempwatch` to view system temperatures and fan speeds.
