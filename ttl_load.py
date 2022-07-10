import urllib.request
import xml.etree.ElementTree as elemTree
name= 'Ardea_cinerea'
req = urllib.request.urlopen("http://lod.nature.go.kr/data/"+name+"?output=xml")
tll= req.read().decode("utf-8")

root= elemTree.fromstring(tll)

triples="["
# print("[")
for child in root[0]:
    if child.text==None:
        # text=child.attrib
        # text=str(text).split("}")[1]
        continue
    else:
        text=child.text.replace('\n', '').replace('\r', '').replace('"','')
    triples+='{ subject: "'+(name)+'",predicate:"'+child.tag.split("}")[1]+'",object:"'+text+'"},'
    # print('{ subject: "',name,'",predicate:"',child.tag.split("}")[1],'",object:"',text,'"},')
triples+="];"
# print("];")

print(triples)

