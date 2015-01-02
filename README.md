HumbleBundle Metalink generator
===============================

Generates a .metalink file for your HumbleBundle downloads.

The generated .metalink file includes HTTPS, torrent and magnet links, as well as other information provided by the HumbleBundle API (file size, MD5/SHA1 hashes).

	usage: metahumble.py [-h] [--cache] [--platform PLATFORM] [--torrents]
	                     [--dir DIR] [--save-links FILE] [--save-bt-links FILE]
	                     email password

	positional arguments:
	  email                 humblebundle.com login (email address)
	  password              humblebundle.com password

	optional arguments:
	  -h, --help            show this help message and exit
	  --cache               cache web requests
	  --platform PLATFORM   filter downloads to a certain platform (e.g.: android)
	  --torrents            download .torrent files to download directory
	  --dir DIR             target download directory
	  --save-links FILE     save http/https links to given text file
	  --save-bt-links FILE  save bittorrent links to given text file
