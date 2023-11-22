import sys
import os
from xml.dom.minidom import parse
import xml.dom.minidom

# https://docs.python.org/3/library/xml.dom.html#node-objects

# 字符串转字典
def stringMapToDict(colorStr):
    colorStr = colorStr.replace('<color ', '')
    colorStr = colorStr.replace('/>', '')
    colorStr = colorStr.replace('"', '')
    colorList = colorStr.split(' ')
    colorDict = {}
    for item in colorList:
        nItem = item.split('=')
        if len(nItem) > 1:
            colorDict[nItem[0]] = nItem[1]

    return colorDict

path = '/Users/litb/Desktop/write_test.xml'
oldDict = stringMapToDict('<color key="backgroundColor" red="0.89019607840000003" green="0.19215686269999999" blue="0.14117647059999999" alpha="1" colorSpace="custom" customColorSpace="sRGB"/>')
newDict = stringMapToDict('<color key="backgroundColor" name="primary"/>')
# path = '/Users/litb/Desktop/TestColor/TestColor/Base.lproj/Main.storyboard'

# 移除缩进和换行符，后面写入的时候统一添加格式
def removeEnterAndSpace():
    with open(path, 'r') as f:
        data = f.read()
        data = data.replace("    ", '')
        data = data.replace("\n", '')
    with open(path, 'w') as f:
        f.write(data)

removeEnterAndSpace()

# xml文件
dom = parse(path)
# 根节点
root = dom.documentElement

# 替换颜色节点
def replaceColorNode():
    colors = root.getElementsByTagName('color')
    for color in colors:
        if color.getAttribute('key') == oldDict['key'] and color.getAttribute('red') == oldDict['red'] and color.getAttribute('green') == oldDict['green'] and color.getAttribute('alpha') == oldDict['alpha']:
            color.parentNode.replaceChild(replaceColor(), color)
            return True
        
    return False

# 替换color
def replaceColor():
    newColor = dom.createElement('color')
    
    for key, value in newDict.items():
        newColor.setAttribute(key, value)

    return newColor

# 插入颜色节点
def insertColorNode():
    insertColorNode = dom.createElement('color')
    insertColorNode.setAttribute('red', '0.1')
    insertColorNode.setAttribute('green', '0.19607843137254902')
    insertColorNode.setAttribute('blue', '0.078431372549019607')
    insertColorNode.setAttribute('alpha', '1')
    insertColorNode.setAttribute('colorSpace', 'custom')
    insertColorNode.setAttribute('customColorSpace', 'sRGB')
    return insertColorNode

# 插入颜色命名空间节点
def insertNamedColorNode(name):
    namedColorNode = dom.createElement('namedColor')
    namedColorNode.setAttribute('name', name)
    namedColorNode.appendChild(insertColorNode())

    return namedColorNode

# 插入color命名空间代码
def insertResourceNode():
    resources = 'resources'
    namedColorNode = insertNamedColorNode('primary')
    if root.getElementsByTagName(resources):
        for node in root.childNodes:
            if node.nodeName == resources:
                node.appendChild(namedColorNode)
    else:
        resourcesNode = dom.createElement('resources')
        resourcesNode.appendChild(namedColorNode)
        root.appendChild(resourcesNode)

isUpdate = replaceColorNode()

if isUpdate:
    if 'name' in newDict.keys():
        print('包含')
        insertResourceNode()
    
    # Python DOM 写入XML
    with open(path, 'w', encoding='UTF-8') as writer:
        # https://docs.python.org/zh-cn/3.9/library/xml.dom.minidom.html
        dom.writexml(writer, indent='', addindent='    ', newl='\n', encoding='UTF-8')