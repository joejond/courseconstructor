from markdown import markdown
from xml.etree.cElementTree import ElementTree, tostring
from cStringIO import StringIO
from xml.dom.minidom import parseString

def pHandler(element, output):
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
    "p" : pHandler,
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

if __name__ == '__main__':
    pass