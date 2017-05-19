# LPG Fixer v1.2

## What does it do?
* Removes extra whitespace.
* Removes hidden quotes that you see when you copy from Excel and paste into MindTap.
* Replaces double quotes `"` in CNow asset titles with a pair of single quotes `''` that look the same in MindTap.
* Replaces m-dashes `—` and n-dashes `–` with regular dashes `-`.
* Replaces some other special characters in CNow asset titles.

## How do I run it?
* Click [here](/lpg/lpg-fixer/exe/lpg-fixer.exe) and download the file into the folder with the LPG.
* Double click the file to run it.
* When prompted, paste the name of the LPG file including the XLSX extension (e.g. `Spielvogel_10e_LPG_2016_10.20.16.xlsx`) into the console window. To paste it into the console window, press `Alt` + `Space`, then press `E` and then press `P`.
* Wait until you see `All set! Press ENTER to exit...` on the screen and press `Enter` to close the window.

## What's new in 1.2?
* Fixed a minor bug where non-string cells resulted in the script not working.

## Source
You can view the source code [here](/lpg/lpg-fixer/source/lpg-fixer.py).
