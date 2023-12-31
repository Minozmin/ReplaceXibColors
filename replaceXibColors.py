#!/usr/bin/python3

import sys
import os
from xml.dom.minidom import parse
import xml.dom.minidom

# https://docs.python.org/3/library/xml.dom.html#node-objects

if sys.version < '3':
    print('必须使用python3, 当前版本是: ' + sys.version)
    sys.exit(0)

if len(sys.argv) < 4:
    print('必须输入4个参数: 第1个是脚本路径, 第2个是需要替换的文件路径, 第3个是旧颜色字符串(rgba值), 第4个是新颜色字符串(颜色命名空间: name)')
    sys.exit(0)

#获取命令行的参数：参数2是文件路径，参数3是旧的颜色字符串rgba，参数4是新的颜色字符串name
path = path = sys.argv[1]
oldColoStr = sys.argv[2]
newColorStr = sys.argv[3]

if not (path.endswith('.xib') or path.endswith('.storyboard')):
    print('第2个参数路径必须是.xib或.storyboard结尾的文件')
    sys.exit(0)

 # 将字典转化为类对象
class DictToObject:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            isinstance
            if isinstance(value, dict):
                setattr(self, key, DictToObject(value))
            else:
                setattr(self, key, value)

# 字符串转字典
def stringMapToDict(colorStr):
    colorStr = colorStr.replace('"', '')
    colorList = colorStr.split(' ')
    colorDict = {}
    for item in colorList:
        nItem = item.split('=')
        if len(nItem) > 1:
            colorDict[nItem[0]] = nItem[1]

    return colorDict

# 第3个参数：旧颜色对象
oldColorObj = DictToObject(stringMapToDict(oldColoStr))
# 第4个参数：新颜色字典和对象
newColorDict = stringMapToDict(newColorStr)
newColorObj = DictToObject(newColorDict)

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
        colorKey = color.getAttribute('key')
        if colorKey and color.getAttribute('red') == oldColorObj.red and color.getAttribute('green') == oldColorObj.green and color.getAttribute('blue') == oldColorObj.blue and color.getAttribute('alpha') == oldColorObj.alpha:
            color.parentNode.replaceChild(replaceColor(colorKey), color)
            return True
        
    return False

# 替换color
def replaceColor(colorKey):
    newColor = dom.createElement('color')
    newColor.setAttribute('key', colorKey)
    for key, value in newColorDict.items():
        newColor.setAttribute(key, value)

    return newColor

# 插入颜色节点
def insertColorNode():
    insertColorNode = dom.createElement('color')
    insertColorNode.setAttribute('red', oldColorObj.red)
    insertColorNode.setAttribute('green', oldColorObj.green)
    insertColorNode.setAttribute('blue', oldColorObj.blue)
    insertColorNode.setAttribute('alpha', oldColorObj.alpha)
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
    namedColorNode = insertNamedColorNode(newColorObj.name)
    if root.getElementsByTagName(resources):
        for node in root.childNodes:
            if node.nodeName == resources:
                for subNode in node.childNodes:
                    if subNode.getAttribute('name') != newColorObj.name:
                        node.appendChild(namedColorNode)
                        return
    else:
        resourcesNode = dom.createElement('resources')
        resourcesNode.appendChild(namedColorNode)
        root.appendChild(resourcesNode)

isUpdate = replaceColorNode()

if isUpdate and 'name' in newColorDict.keys():
    insertResourceNode()

# Python DOM 写入XML
with open(path, 'w', encoding='UTF-8') as writer:
    # https://docs.python.org/zh-cn/3.9/library/xml.dom.minidom.html
    dom.writexml(writer, indent='', addindent='    ', newl='\n', encoding='UTF-8')