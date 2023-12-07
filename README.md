# Sheet-Music-Scanner

## Dependencies

All dependencies can be installed with pip. As for reading musicXML (.mxl) files pretty much any notation software will work; Musescore is free, open source, compatible with most systems, and more intuitive then others. 

- OpenCV
- numpy
- music21

## How to Use

`main.py` takes two arguments, the first is the path to the image of the sheet music, and the second is the title/name for the output. This should be done from the root dir of the project (Sheet-Music-Scanner), as relitive paths are used.

```sh
 $ python3 src/main.py "<image-path>" "<output-name>"
```

The output file will be located under the `data/music-xmls/` dir, and will be named `<output-name>.mxl`. There will also be some images created in the `data/images/` dir that will show some of the steps in the process. Those being: 
 - `rescaleOutput.png`
 - `removeLineOutput.png`
 - `testOutput.png`

### Provided Examples

Two examples are provided each with a 600dpi and 450dpi png stored under the `data/images/` dir, as well as the source for each stored under the `data/music-xmls/` dir. Note: `TemplateSheet` is not an example but is the original source of the templates used for template matching.
