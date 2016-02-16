# Introduction #

This code adds the ability to convert from Markdown text (the subset I am interested in) into Google Wiki format and now supports media wiki format.

FYI: "Markdown is a text-to-HTML conversion tool for web writers. Markdown allows you to write using an easy-to-read, easy-to-write plain text format, then convert it to structurally valid XHTML (or HTML)." See markdown and python-markdown for more details.

This python script coverts markdown text into Google Wiki text or media wiki format.

Using eval and polymorphism to easily support multiple Wiki's inputs.


```
    
class Tag:
    text=""
    name=""
    def __init__ (self, name, text=""):
        self.text = text
        self.name = name
    def writeTag(self, output):
            pass
        
class Heading(Tag):
    level=1
    def __init__ (self, text, level):
        Tag.__init__(self, "heading", text)
        self.level = level

class ListItem(Tag):
    def __init__ (self, text):
        Tag.__init__(self, "list-item", text)
    
class Text(Tag):
    def __init__ (self, text):
        Tag.__init__(self, "text", text)

class Strong(Tag):
    def __init__ (self, text):
        Tag.__init__(self, "strong", text)

class Emphasis(Tag):
    def __init__ (self, text):
        Tag.__init__(self, "emphasis", text)

class Code(Tag):
    def __init__ (self, text):
        Tag.__init__(self, "code", text)

class CodeBlock(Tag):
    def __init__ (self, text):
        Tag.__init__(self, "codeblock", text)

class Paragraph(Tag):
    def __init__ (self):
        Tag.__init__(self, "paragraph")
        self.tags = []
    def add_tag(self, tag):
        # You could do some tag validation here
        self.tags.append(tag)
        return tag


class List(Tag):
    ordered=False
    def __init__ (self, ordered):
        Tag.__init__(self, "list")
        self.ordered = ordered
        self.listItems = []
    def add_item(self, item):
        # You could do some item validation here
        self.listItems.append(item)
        return item
                
class Content:
    
    def __init__(self):
        self.tags = []

    def add_tag(self, tag):
        # You could do some tag validation here
        self.tags.append(tag)
        return tag
    
    def printIt(self):
        for tag in self.tags:
            print tag.name
            print tag.text
            if isinstance(tag, Paragraph):
                for ptag in tag.tags:
                    print ptag.name
                    print ptag.text
            if isinstance(tag, List):
                print "List is ordered? " + `tag.ordered`
                for listItem in tag.listItems:
                    print listItem.name
                    print listItem.text

    def generateDocument(self, output):
        for tag in self.tags:
            tag.writeTag(output)

from markdown import markdown
from xml.etree.cElementTree import ElementTree, tostring
from cStringIO import StringIO
from xml.dom.minidom import parseString

      
class ContentConverter:
    def paraHandler(self, element):
        para = parseString(tostring(element)).childNodes[0]
        paragraph = self.content.add_tag(eval("{0}Paragraph()".format(self.contentType)))
        for node in para.childNodes:
            if node.nodeName == "strong":
                strong = eval("{0}Strong(node.firstChild.nodeValue)".format(self.contentType))
                paragraph.add_tag(strong)
            elif node.nodeName == "em":
                emphasis = eval("{0}Emphasis(node.firstChild.nodeValue)".format(self.contentType))
                paragraph.add_tag(emphasis)
            elif node.nodeName == "code":
                code = eval("{0}Code(node.firstChild.nodeValue)".format(self.contentType))
                paragraph.add_tag(code)
            else:
                text = eval("{0}Text(node.nodeValue)".format(self.contentType))
                paragraph.add_tag(text)

    def unorderedListHanlder(self, element):
        lst = self.content.add_tag(eval("{0}List(ordered=False)".format(self.contentType)))
        for child in element.getchildren():
            lst.add_item(eval("{0}ListItem(child.text)".format(self.contentType)))
    
    
    def orderedListHandler(self, element):
        lst = self.content.add_tag(eval("{0}List(ordered=True)".format(self.contentType)))
        for child in element.getchildren():
            lst.add_item(eval("{0}ListItem(child.text)".format(self.contentType)))
    
    def preHandler(self, element):
        element = element.getchildren()[0]
        codeBlock = eval("{0}CodeBlock(element.text)".format(self.contentType))
        codeBlock.lang = element.get("class", "nolang")
        self.content.add_tag(codeBlock)
    
    def headerHandler(self, element, level):
        header = eval("{0}Heading(element.text, level + self.levelOffset)".format(self.contentType))
        self.content.add_tag(header)
                
    handlers = {
        "pre" : preHandler,
        "p" : paraHandler,
        "ul" : unorderedListHanlder,
        "ol" : orderedListHandler,
    }

    def convertToWiki(self, markdown_text, levelOffset=0, contentType=""):
        content = self.convert(markdown_text, levelOffset, contentType)
        output = StringIO() 
        content.generateDocument(output)
        return output.getvalue()
    
    def convert(self, markdown_text, levelOffset=0, contentType=""):
        self.levelOffset = levelOffset
        self.content = Content()
        self.contentType = contentType
        html = markdown(markdown_text, ["fenced_code"])
        html = "<div>\n{0}\n</div>".format(html)
        root = ElementTree().parse(StringIO(html))
        for child in root.getchildren():
            if child.tag[0] == "h":
                try:
                    level = int(child.tag[1])
                except:
                    continue
                self.headerHandler(child, level)
            elif child.tag in self.handlers:
                self.handlers[child.tag](self, child)
            else:
                print "Unknown tag {0}".format(child.tag)

        return self.content


            
class GoogleWikiHeading(Heading):
    def __init__ (self, text, level):
        Heading.__init__(self, text, level)
    def writeTag(self, output):
        output.write(("=" * self.level) + self.text + ("=" * self.level) + "\n")
 
class GoogleWikiListItem(ListItem):
    def __init__ (self, text):
        ListItem.__init__(self, text)
    
class GoogleWikiText(Text):
    def __init__ (self, text):
        Text.__init__(self, text)
    def writeTag(self, output):
        output.write("{0}".format(self.text, self.name))

class GoogleWikiStrong(Strong):
    def __init__ (self, text):
        Strong.__init__(self, text)
    def writeTag(self, output):
        output.write("*{0}*".format(self.text, self.name))

class GoogleWikiEmphasis(Emphasis):
    def __init__ (self, text):
        Emphasis.__init__(self, text)
    def writeTag(self, output):
        output.write("_{0}_".format(self.text, self.name))

class GoogleWikiCode(Code):
    def __init__ (self, text):
        Code.__init__(self, text)
    def writeTag(self, output):
        output.write("`{0}`".format(self.text, self.name))

class GoogleWikiCodeBlock(CodeBlock):
    def __init__ (self, text):
        CodeBlock.__init__(self, text)
    def writeTag(self, output):
        output.write("""
{{{
%s
}}}
""" % self.text)

class GoogleWikiParagraph(Paragraph):
    def __init__ (self):
        Paragraph.__init__(self)
    def writeTag(self, output):
        output.write("\n")
        for tag in self.tags:
            tag.writeTag(output)
        output.write("\n")


class GoogleWikiList(List):
    def __init__ (self, ordered):
        List.__init__(self, ordered)
    def writeTag(self, output):
        output.write("\n")
        for item in self.listItems:
            if self.ordered:
                output.write(" # {0}\n".format(item.text))
            else:
                output.write(" * {0}\n".format(item.text))
        output.write("\n")
                
class GoogleWikiContent(Content):
    pass

class MediaWikiHeading(Heading):
    def __init__ (self, text, level):
        Heading.__init__(self, text, level)
    def writeTag(self, output):
        output.write(("=" * self.level) + self.text + ("=" * self.level) + "\n")
 
class MediaWikiListItem(ListItem):
    def __init__ (self, text):
        ListItem.__init__(self, text)
    
class MediaWikiText(Text):
    def __init__ (self, text):
        Text.__init__(self, text)
    def writeTag(self, output):
        output.write("{0}".format(self.text, self.name))

class MediaWikiStrong(Strong):
    def __init__ (self, text):
        Strong.__init__(self, text)
    def writeTag(self, output):
        output.write("*{0}*".format(self.text, self.name))

class MediaWikiEmphasis(Emphasis):
    def __init__ (self, text):
        Emphasis.__init__(self, text)
    def writeTag(self, output):
        output.write("_{0}_".format(self.text, self.name))

class MediaWikiCode(Code):
    def __init__ (self, text):
        Code.__init__(self, text)
    def writeTag(self, output):
        output.write("`{0}`".format(self.text, self.name))

class MediaWikiCodeBlock(CodeBlock):
    def __init__ (self, text):
        CodeBlock.__init__(self, text)
    def writeTag(self, output):
        output.write("""
<source lang="%s">
%s
</source>
""" % (self.lang, self.text) )

class MediaWikiParagraph(Paragraph):
    def __init__ (self):
        Paragraph.__init__(self)
    def writeTag(self, output):
        output.write("\n")
        for tag in self.tags:
            tag.writeTag(output)
        output.write("\n")


class MediaWikiList(List):
    def __init__ (self, ordered):
        List.__init__(self, ordered)
    def writeTag(self, output):
        output.write("\n")
        for item in self.listItems:
            if self.ordered:
                output.write("# {0}\n".format(item.text))
            else:
                output.write("* {0}\n".format(item.text))
        output.write("\n")
                
class MediaWikiContent(Content):
    pass
```