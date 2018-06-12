import socket
import os
from common import hexdump
from structures import *
import asyncio
import ipaddress
import ntpath
import logging


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

async def unknown_client(ip, port, filename_base, loop):
	filename = None
	if filename_base:
		filename = '%s_%s_%d.txt' % (filename_base,ip, port)

	reader, writer = await asyncio.open_connection(ip, port,loop=loop)
	
	try:
		log.info('Sending initial request to %s:%d' % (ip, port))
		writer.write(b'GET / HTTP/1.1\r\nHost: dunno\r\n\r\n')

		header = await reader.readexactly(11) #not really important
		while True:
			b = await Block.from_asyncio(reader)
			if filename:
				with open(filename,'a', encoding="utf-8") as f:
					for element in b.elements:
						url = None
						try:
							url = element.data.decode().strip()
						except:
							pass
						if url and len(url) > 0:
							f.write(url + '\r\n')
			for element in b.elements:
				try:
					url = element.data.decode().strip()
					if len(url) > 0:
						log.info(url)
				except:
					log.debug('encode failed, the element type is probably an unknown one!')
					pass
	except Exception as e:
		logging.exception('Something crashed! The client for server %s:%d will not work anymore!' % (ip, port))
	finally:
		log.info('Close the socket')
		writer.close()

def main(targets):
	loop = asyncio.get_event_loop()
	for target in targets:
		loop.create_task(unknown_client(*target, loop))
	loop.run_forever()
	loop.close()


if __name__ == '__main__':
	import argparse
	
	parser = argparse.ArgumentParser(description='Weird protocol client')
	parser.add_argument('-a','--address', action='append', help='Server(s) to connect to. Expected format: <IP>:<port>', required=True)
	parser.add_argument('-o', help='Ouput filename base. It will be modified to include server address.')
	#parser.add_argument('-s', action='store_true', help='Silent mode, nothing will be printed (only exceptions). Should only be used when output file is specified.')
	args = parser.parse_args()
	
	
	#if args.s == True:
	#	log.setLevel(logging.WARN)
		
	
	targets = []
	for address in args.address:
		ip, port = address.split(':')
		try:
			port = int(port)
			t = ipaddress.ip_address(ip)
		except Exception as e:
			raise Exception('Wrong address format supplied! %s' % e)
			
		filename_base = None
		if args.o:
			abs_path = os.path.dirname(os.path.abspath(args.o))
			fn = ntpath.basename(args.o)
			filename_base = os.path.join(abs_path, fn)
		
		targets.append((ip, port,filename_base))
		
	log.info('Starting!')
	main(targets)
	