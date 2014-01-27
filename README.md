SnapSync
========

SnapSync - Syncing your Mac Snaps with Google Drive. It is written in PyObjC.

The build script, credentials and client_secrets would be shared on demand (if Application is not published), as the complete Application would be shared on GitHub soon.


Objective:
The name of the application is SnapSync. This application basically syncs Snapshots taken from Mac Systems to the user's respective Google Drive Account.
The reason behind writing this application was to automate the backup of Snaps which I take during my research on any topic, as well as to access those contents / snaps from any device.

Features:
It will change the default Screenshots path of the Macintosh Systems to the directed path, and a watch on this directory is maintained.
A smart tool which also gives Macintosh Notifications as soon as any file is uploaded on the Drive, and copies that file's URL to clipboard as well as writes the same into a text file for keeping a track of links.

These URL are shortened and saved using Google's URL Shortener.

Also, to regenerate Copy-to-Clipboard function, Context Menu is added to specifically Screenshots Directory, wherein, an additional option would be visible when a Right-Click event is called on that file, and to only those Snaps which are inside the Screenshots directory.

An add-on feature which I am working on is grab the screenshot of the complete page on which the user is currently active, even if the whole page is not visible, and store that file with URL as its file name. A new HotKey has been defined to perform this add-on feature.
