#!/usr/bin/env python3

class Element:
	
	def __init__(self, content = None):
		self.content = []
		if content is not None:
			self.content.append(content)
	
	def append(self, content):
		self.content.append(content)

	def render(self, out_file, int=""):
		out_file.write("<html>\n")
		for stuff in self.content:
			out_file.write(stuff+"\n")
		out_file.write("</html>\n")

