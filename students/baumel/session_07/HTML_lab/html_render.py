#!/usr/bin/env python3

class Element:
	
	def __init__(self, content = None, tag = None):
		self.content = []
		self.tag = tag
		if content is not None:
			self.content.append(content)
	
	def append(self, content):
		self.content.append(content)

	def render(self, out_file):
		if self.tag is None:
			self.tag = "html"
		start = "<",self.tag,">\n"
		finish = "</",self.tag,">\n"
		
		out_file.write(''.join(start))
		for stuff in self.content:
			out_file.write(stuff+"\n")
		out_file.write(''.join(finish))

#  sub classes for <html>, <body>, and <p> 
