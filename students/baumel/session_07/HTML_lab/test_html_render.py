"""
test code for html_render
"""
import io
from html_render import Element

def test_init():
	e = Element()

	e = Element("this is some text")

def test_content():
	#fixme: this test internals!!!!!!!!
	e = Element("this is some text")

	assert "this is some text" in e.content

def test_append():
	e = Element("this is some text")

	e.append("some more text, wooHoo!")

	assert "some more text, wooHoo!" in e.content

def test_two_instances():
	e = Element("this is some text")
	e2 = Element("this is some text")

	e.append("some more text")

	assert "some more text" not in e2.content
	
def test_render():
	outfile = io.StringIO()

	e = Element("this is some text")
	e.append("and this is some more text, WooHoo!!")
	
	e.render(outfile)

	outfile.seek(0)
	file_contents = outfile.read()
	#f = open('test1.html', 'w')
	#f.write(file_contents)
	open('test1.html', 'w').write(file_contents)

	print(file_contents)
	assert ("this is some text") in file_contents
	assert ("and this is some more text, WooHoo!!") in file_contents

	assert file_contents.startswith("<html>")
	assert file_contents.strip().endswith("</html>")

def test_tag():
	outfile = io.StringIO()

	e = Element("this is some text", "body")
	e.append("and this is some more text, WooHoo!!")
	
	e.render(outfile)

	outfile.seek(0)
	file_contents = outfile.read()
	#f = open('test1.html', 'w')
	#f.write(file_contents)
	open('test1.html', 'w').write(file_contents)

	print(file_contents)
	assert ("this is some text") in file_contents
	assert ("and this is some more text, WooHoo!!") in file_contents

	assert file_contents.startswith("<body>")
	assert file_contents.strip().endswith("</body>")

	

	
