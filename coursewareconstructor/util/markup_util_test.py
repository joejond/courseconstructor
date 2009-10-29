import unittest
from markdown import markdown, markdownToDOM

class MarkupTestCase(unittest.TestCase):
    def setUp(self):
        self.markup_text = """
# H1
## H2
### H3
1. Hi
2. How
3. Are
4. You


~~~~{.python}
def foo():
    pass
~~~~
        """
    
    def testMarkup(self):
        
        html = markdown(self.markup_text, ["fenced_code"])
        print html
        self.assertEquals(1, html.count("<h1>"))
        self.assertEquals(1, html.count("H1"))
        self.assertEquals(1, html.count("<ol>"))
        self.assertEquals(4, html.count("<li>"))
        self.assertEquals(1, html.count("</ol>"))
        self.assertEquals(1, html.count("<code"))
        self.assertEquals(1, html.count("</code>"))
        

    def testMarkupToDOM(self):
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