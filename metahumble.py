#!/bin/python2

import os, os.path

class HumbleLinker(object):
	def __init__(self):
		self.cache = False

	def enable_cache(self):
		import requests_cache
		requests_cache.install_cache('web_cache')
		self.cache = True

	def login(self, username, password):
		import humblebundle
		self.client = humblebundle.HumbleApi()

		if not self.cache:
			self.client.login(username, password)

	def run(self, dl_dir = 'dl', platform = None, links_fn = None, btlinks_fn = None, get_torrents = False):
		links = open(links_fn, 'w') if links_fn else None
		btlinks = open(btlinks_fn, 'w') if btlinks_fn else None

		if not os.path.exists(dl_dir):
			os.makedirs(dl_dir)

		import metalink

		m = metalink.Metalink()
		m.files = []
		metalink._opts['overwrite'] = True
		metalink._opts['create_torrent'] = False

		files = set()

		import progressbar
		progress = progressbar.ProgressBar()

		for gamekey in progress(self.client.get_gamekeys()):
			order = self.client.get_order(gamekey)
			#print(order.product.machine_name)
			if order.subproducts is not None:
				for subproduct in order.subproducts:
					#print(subproduct)
					#print(" " + subproduct.machine_name)
					for download in subproduct.downloads:
						#print download.platform
						if platform is None or platform == download.platform:
							for struct in download.download_struct:
								found_link = False
								if struct.url.bittorrent is not None:
									found_link = True
									if btlinks:
										btlinks.write(struct.url.bittorrent + '\n')

									torrent_fn = dl_dir + '/' + struct.url.bittorrent.split("?")[0].split("/")[-1]
									if get_torrents and not os.path.exists(torrent_fn):
										import urllib
										urllib.urlretrieve (struct.url.bittorrent, torrent_fn)

								if struct.url.web is not None:
									found_link = True
									if links:
										links.write(struct.url.web + '\n')

								if not found_link:
									#print(subproduct)
									#print(download)
									#print(struct)
									#print('----------------')
									continue

								filename = struct.url.web.split("?")[0].split("/")[-1]
								if filename in files:
									continue
								files.add(filename)

								m.add_file()
								m.file.filename = filename
								m.file.os = download.platform
								if struct.file_size is not None:
									m.file.size = str(struct.file_size)
								if struct.sha1 and len(struct.sha1) == 40:
									m.file.hashes['sha1'] = struct.sha1
								if struct.md5 and len(struct.md5) == 32:
									m.file.hashes['md5'] = struct.md5
								if struct.url.web is not None:
									m.file.add_url(struct.url.web)
								if struct.url.bittorrent is not None:
									m.file.add_url(struct.url.bittorrent, 'bittorrent')

		m.generate(dl_dir + '/hb.metalink')

def main():
	import argparse

	parser = argparse.ArgumentParser(description='HumbleBundle Metalink generator')
	parser.add_argument('email', help='humblebundle.com login (email address)')
	parser.add_argument('password', help='humblebundle.com password')
	parser.add_argument('--cache', action='store_true', help='cache web requests')
	parser.add_argument('--platform', help='filter downloads to a certain platform (e.g.: android)')
	parser.add_argument('--torrents', action='store_true', help='download .torrent files to download directory')
	parser.add_argument('--dir', default='dl', help='target download directory (default: dl)')
	parser.add_argument('--save-links', metavar='FILE', help='save http/https links to given text file', dest='links')
	parser.add_argument('--save-bt-links', metavar='FILE', help='save bittorrent links to given text file', dest='btlinks')

	args = parser.parse_args()

	linker = HumbleLinker()
	if args.cache:
		linker.enable_cache()
	linker.login(args.email, args.password)
	linker.run(args.dir, args.platform, args.links, args.btlinks, args.torrents)

if __name__ == '__main__':
	main()
