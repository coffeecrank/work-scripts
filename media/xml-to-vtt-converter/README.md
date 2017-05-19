# XML to VTT converter (standalone version) v1.4

## What does it do?
* Converts ADB.XML closed captions into VTT closed captions.
* Identidies badly formatted ADB.XML files (e.g. missing tags) and puts them into a separate subfolder.
* Formats all data stamps following this format mask: `XX:XX:XX.XXX`

## How do I run it?
* Click [here](/media/xml-to-vtt-converter/exe/xml-to-vtt-converter.exe) and download the file into the folder with ADB.XML files.
* Double click the file to run it.
* If some of the files are badly formatted, you'll see a subfolder `badly-formatted-xml` appear containing these files.
* Wait until the console window closes and don't close it yourself.

## What's new in 1.4?
* Added support for didderent time stamp formats.

## Source
You can view the source code [here](/media/xml-to-vtt-converter/source/xml-to-vtt-converter.py).