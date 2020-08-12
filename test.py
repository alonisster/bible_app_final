import xml.etree.ElementTree as et
import re

APPEARANCE_COUNT = "appearance_count"
APPEARANCES = "appearances"
PRIVATE_NAME = "שם-פרטי"

tree = et.parse("data\\books\\Torah\\Genesis.xml")
root = tree.getroot()

women_file = open('data\\women.txt', encoding='utf-8')
women_list = women_file.read().split('\n')


def remove_vowels(s):
    s = s.replace("/", "")
    s = s.replace("=", "")
    return re.sub(r'[\u0591-\u05BD\u05BF-\u05C2\u05C4-\u05C7]', '', s)

num_chapter = 1
num_chapter = 1
for chapter in root[1][0]:  # root['text']['book']['chapter']
    num_verse = 1
    for verse in chapter:
        if num_chapter == 6 and num_verse == 2:
            for word in verse:
                if word.attrib:  # word must have attributes
                    if word.attrib['root'] == "טוב":
                        for m in word:
                            print(m.attrib['ana'])
            num_verse += 1
            #        if word.attrib['root'] == PRIVATE_NAME:
            #            name = remove_vowels(str(word.attrib['lemma']))
            #            if name in women_list:
            #                print()#print(name)
        num_verse += 1
    num_chapter += 1