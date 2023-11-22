import sys
import os
from xml.dom.minidom import parse
import xml.dom.minidom

# https://docs.python.org/3/library/xml.dom.html#node-objects

path = '/Users/litb/Desktop/write_test.xml'
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
        if color.getAttribute('red') == '0.0':
            color.parentNode.replaceChild(replaceColor, color)

# 替换color
def replaceColor():
    newColor = dom.createElement('color')
    newColor.setAttribute('key', 'backgroundColor')
    newColor.setAttribute('name', 'primary')

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

insertResourceNode()
replaceColorNode()

# Python DOM 写入XML
with open(path, 'w', encoding='UTF-8') as writer:
    # https://docs.python.org/zh-cn/3.9/library/xml.dom.minidom.html
    dom.writexml(writer, indent='', addindent='    ', newl='\n', encoding='UTF-8')