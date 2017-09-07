# Video Wrapper v1.1

## What does it do?
* Generates HTML "wrappers" for videos which you can use in CNow and any apps supporting <iframe></iframe> tags.
* Eliminates the need to manually create these HTML wrappers.

## How do I run it?
* Click [here](/media/video-wrapper/exe/video-wrapper.exe) and download the script into an empty folder.
* Click on [this link](/media/video-wrapper/exe/template.html) and download the HTML template into the same folder.
* Create a TXT file `videos.txt` in the same folder. In this file, each line should be a video name without extension (it can have `_med`, `_hi` or `_low` in the name). For example, `9_11_med`.
* Double click on `video-wrapper.exe` to run it.
* The script will prompt you for a Wowza path. Type in the path for the video composite folder on Wowza (with or without last forward slash) and press `Enter`.
* The script will ask you whether your videos are all in the same folder or in their own individual folders. Answer `Y` or `N` and press `Enter`.
* After the script is done, you can press `Enter` again to exit, and you will see a bunch of HTML wrappers (or folders containing HTML wrappers) generated.

## What's new in 1.1?
* Fixed a bug where video names starting with a digit caused an error.

## Source
You can view the source code [here](/media/video-wrapper/source/video-wrapper.py).