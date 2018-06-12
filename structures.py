import sys
import io
import asyncio
from common import hexdump

def peek(buff, size = 0x20):
	print(hexdump(buff.read(size)))
	buff.seek(-size,1)

class Element:
	def __init__(self):
		self.type_probably = None
		self.length = None
		self.header = None
		self.data = None
		
	def parse(reader):
		#peek(reader)
		#input()
		e = Element()
		e.type_probably = int.from_bytes(reader.read(8), byteorder = 'big', signed = False)
		e.length = int.from_bytes(reader.read(4), byteorder = 'little', signed = False)
		#input('e_length: %s' % hex(e.length))
		e.header = reader.read(25)
		e.data = reader.read(e.length - (25 + 4 + 8))
		#print(e.data)
		return e
"""
class BigBlock:
	def __init__(self):
		self.hdr_type = None
		self.hdr_unknown = None
		self.blocks = None
		
	def parse(reader):
		b = BigBlock()
		b.hdr_type = int.from_bytes(reader.read(4), byteorder = 'big', signed = False)
		b.hdr_unknown_1 = int.from_bytes(reader.read(4), byteorder = 'big', signed = False)
		
		
		while tbuff.tell() < len(data):
			b.blocks.append(Block.parse(tbuff))
		
		return b
"""
		
class Block:
	def __init__(self):
		self.hdr_unknown_byte = None
		self.hdr_maxlength = None
		self.hdr_minlength = None
		self.hdrunknown = None
		self.elements = []
		self.data = None
		
	
	async def from_asyncio(reader):
		b = Block()
		t = await reader.readexactly(1)
		b.hdr_unknown_byte = int.from_bytes(t, byteorder = 'big', signed = False)
		#print(b.hdr_unknown_byte)
		t = await reader.readexactly(4)
		b.hdr_maxlength = int.from_bytes(t, byteorder = 'little', signed = False)
		#print(b.hdr_maxlength)
		t = await reader.readexactly(4)
		b.hdr_minlength = int.from_bytes(t, byteorder = 'little', signed = False)
		b.hdr_unknown_2 = await reader.readexactly(12)
		
		#input('hdr_maxlength: %s ' % b.hdr_maxlength)
		
		data = await reader.readexactly(b.hdr_maxlength - 21)
		#print(hexdump(data))
		tbuff = io.BytesIO(data)
			
		while tbuff.tell() < len(data):
			b.elements.append(Element.parse(tbuff))
		
		return b
		
	def parse(reader):
		b = Block()
		b.hdr_unknown_byte = int.from_bytes(reader.read(1), byteorder = 'big', signed = False)
		b.hdr_maxlength = int.from_bytes(reader.read(4), byteorder = 'little', signed = False)
		b.hdr_minlength = int.from_bytes(reader.read(4), byteorder = 'little', signed = False)
		b.hdr_unknown_2 = reader.read(12)
		
		#input('hdr_maxlength: %s ' % b.hdr_maxlength)
		
		data = reader.read(b.hdr_maxlength - 21)
		#print(hexdump(data))
		tbuff = io.BytesIO(data)
			
		while tbuff.tell() < len(data):
			b.elements.append(Element.parse(tbuff))
		
		return b
		
if __name__ == '__main__':
	with open('.\\sample_data\\wifithing.bin','rb') as f:
		data = f.read()

	buff = io.BytesIO(data)
	main_header = buff.read(8)
	while buff.tell() < len(data):
		b = Block.parse(buff)
		#input('New block!')