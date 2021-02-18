from lxml import etree

dom = etree.parse("results/goods.xml")
xslt = etree.parse("xslt/goods.xslt")
transform = etree.XSLT(xslt)
result = transform(dom)

with open('results/goods.html', 'wb') as f:
        f.write(etree.tostring(result, pretty_print=True))