# Fonts for mmMCounter

## Accessible Font Options

mmMCounter supports system font selection for improved accessibility. While the application defaults to Arial, you can select any installed system font from the timer configuration dialog.

### Recommended: OpenDyslexic Font

**OpenDyslexic** is a free, open-source font designed to increase readability for readers with dyslexia. The typeface includes regular, bold, italic, and bold-italic styles.

#### Installation Instructions

##### Windows
1. Download OpenDyslexic from: https://opendyslexic.org/
2. Extract the ZIP file
3. Right-click on the `.otf` or `.ttf` font files
4. Select "Install" or "Install for all users"
5. Restart mmMCounter
6. Open timer settings and select "OpenDyslexic" from the font dropdown

##### macOS
1. Download OpenDyslexic from: https://opendyslexic.org/
2. Extract the ZIP file
3. Double-click the `.otf` or `.ttf` font files
4. Click "Install Font" in Font Book
5. Restart mmMCounter
6. Open timer settings and select "OpenDyslexic" from the font dropdown

##### Linux
1. Download OpenDyslexic from: https://opendyslexic.org/
2. Extract the ZIP file
3. Copy font files to `~/.local/share/fonts/` or `/usr/share/fonts/`
4. Run `fc-cache -f -v` to rebuild font cache
5. Restart mmMCounter
6. Open timer settings and select "OpenDyslexic" from the font dropdown

## Other Accessibility Considerations

- **Font Size**: Adjustable per timer (8-24pt recommended range)
- **High Contrast**: Use dark theme with light text for better visibility
- **Bold Text**: Enable bold option for increased legibility
- **Large Time Display**: Timer countdown uses 16pt bold by default

## License Note

OpenDyslexic is released under a Creative Commons Attribution 3.0 Unported License and the Bitstream Vera License. See https://opendyslexic.org/ for details.

mmMCounter does not bundle OpenDyslexic to keep the executable size small and respect font licensing. Users can install it separately as needed.
