This code adds the ability to convert from Markdown text (the subset I am interested in) into Google Wiki format.

FYI: "Markdown is a text-to-HTML conversion tool for web writers. Markdown allows you to write using an easy-to-read, easy-to-write plain text format, then convert it to structurally valid XHTML (or HTML)." See [markdown](http://daringfireball.net/projects/markdown/) and [python-markdown](http://www.freewisdom.org/projects/python-markdown/) for more details.

This python script coverts markdown text into Google Wiki text.

```
from markdown import markdown
from xml.etree.cElementTree import ElementTree, tostring
from cStringIO import StringIO
from xml.dom.minidom import parseString

def paraHandler(element, output):
    para = parseString(tostring(element)).childNodes[0]
    output.write("\n")
    for node in para.childNodes:
        if node.nodeName == "strong":
            output.write("*{0}*".format(node.firstChild.nodeValue))
        elif node.nodeName == "em":
            output.write("_{0}_".format(node.firstChild.nodeValue))
        elif node.nodeName == "code":
            output.write("`{0}`".format(node.firstChild.nodeValue))
        else:
            output.write("{0}".format(node.nodeValue))
    output.write("\n")

def unorderedListHanlder(element, output):
    output.write("\n")
    for child in element.getchildren():
        output.write(" *  {0} \n".format(child.text))
    output.write("\n")


def orderedListHandler(element, output):
    output.write("\n")
    for child in element.getchildren():
        output.write(" #  {0} \n".format(child.text))
    output.write("\n")

def preHandler(element, output):
    code = element.getchildren()[0]
    output.write("""
{{{
%s
}}}
    """ % code.text)

def headerHandler(element, output, level):
    output.write(("=" * level) + element.text + ("=" * level) + "\n") 
    
handlers = {
    "pre" : preHandler,
    "p" : paraHandler,
    "ul" : unorderedListHanlder,
    "ol" : orderedListHandler,
}


def convert_to_wiki(text):
    output = StringIO()    
    html = markdown(text, ["fenced_code"])
    html = "<div>\n{0}\n</div>".format(html)
    root = ElementTree().parse(StringIO(html))
      
    for child in root.getchildren():
        if child.tag[0] == "h":
            try:
                level = int(child.tag[1])
            except:
                continue
            headerHandler(child, output, level)
        elif child.tag in handlers:
            handlers[child.tag](child,output)
        else:
            print "Unknown tag {0}".format(child.tag)
    return output.getvalue()

```

To exercise this, I wrote a unit test (not a very good unit test btw) as follows:

```
import unittest
from markdown import markdown
from util.markup_util import convert_to_wiki

class MarkupTestCase(unittest.TestCase):
    def setUp(self):
        self.markup_text = """
# H1
## H2
### H3
# Header 1
## Header 2
### Hi how are you
----------
1. Hi
2. How
3. Are
4. You
---------

-----------
- this
- is
- anohter
- list
----------
This is some text. 

This is some more text.

I am a paragraph with special sauce *emphasis* and **strong asdfasdf** `printf (void)`.

~~~~{.python}
def foo():
    pass
~~~~
        """
    
    def testMarkup(self):
        
        html = markdown(self.markup_text, ["fenced_code"])
        print html
#        self.assertEquals(1, html.count("<h1>"))
#        self.assertEquals(1, html.count("H1"))
#        self.assertEquals(1, html.count("<ol>"))
#        self.assertEquals(4, html.count("<li>"))
#        self.assertEquals(1, html.count("</ol>"))
#        self.assertEquals(1, html.count("<code"))
#        self.assertEquals(1, html.count("</code>"))
        
    def testConvertToWiki(self):
        print "WIKI \n" + convert_to_wiki(self.markup_text)
        
    def ztestMarkupToDOM(self):
        from cStringIO import StringIO
        
        html = markdown(self.markup_text, ["fenced_code"])
        html = "<div>\n{0}\n</div>".format(html)
        print "\n"
        print "#" + html + "#"
        myfile = StringIO(html)
        
        from xml.etree.ElementTree import ElementTree
        tree = ElementTree()
        root = tree.parse(myfile)
        print `root`
      
        for child in root.getchildren():
            if child.tag == "pre":
                child = child.getchildren()[0]
            print "tag " + `child.tag`
            print "text " + `child.text`
            print "attrib " + `child.attrib`
                
        #http://docs.python.org/library/xml.etree.elementtree.html
        
if __name__ == '__main__':
    unittest.main()        
```

In short this markdown text

```
# H1
## H2
### H3
# Header 1
## Header 2
### Hi how are you
----------
1. Hi
2. How
3. Are
4. You
---------

-----------
- this
- is
- anohter
- list
----------
This is some text. 

This is some more text.

I am a paragraph with special sauce *emphasis* and **strong asdfasdf** `printf (void)`.

~~~~{.python}
def foo():
    pass
~~~~

```

Can convert into this HTML

```
<h1>H1</h1>
<h2>H2</h2>
<h3>H3</h3>
<h1>Header 1</h1>
<h2>Header 2</h2>
<h3>Hi how are you</h3>
<hr />
<ol>
<li>Hi</li>
<li>How</li>
<li>Are</li>
<li>You</li>
</ol>
<hr />
<hr />
<ul>
<li>this</li>
<li>is</li>
<li>anohter</li>
<li>list</li>
</ul>
<hr />
<p>This is some text. </p>
<p>This is some more text.</p>
<p>I am a paragraph with special sauce <em>emphasis</em> and <strong>strong asdfasdf</strong> <code>printf (void)</code>.</p>
<pre><code class="python">def foo():
    pass
</code></pre>
```

And now with this utility, it can now be converted to this GoogleWiki format:

```
 
=H1=
==H2==
===H3===
=Header 1=
==Header 2==
===Hi how are you===

 #  Hi 
 #  How 
 #  Are 
 #  You 


 *  this 
 *  is 
 *  anohter 
 *  list 


This is some text. 

This is some more text.

I am a paragraph with special sauce _emphasis_ and *strong asdfasdf* `printf (void)`.

{{{
def foo():
    pass

}}}

```
Which should look like this


# H1 #
## H2 ##
### H3 ###
# Header 1 #
## Header 2 ##
### Hi how are you ###

  1. Hi
  1. How
  1. Are
  1. You


  * this
  * is
  * anohter
  * list


This is some text.

This is some more text.

I am a paragraph with special sauce _emphasis_ and **strong asdfasdf** `printf (void)`.

```
def foo():
    pass

```