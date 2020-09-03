import xml.etree.ElementTree as et
import re
from pathlib import Path
import os
import gematria

# constants
APPEARANCE_COUNT = "appearance_count"
APPEARANCES = "appearances"
PRIVATE_NAME = "שם-פרטי"
ADJECTIVES = "adjectives"


women_occ = {}
men_occ = {}
total_women_occ = 0
total_men_occ = 0
books_occ = {}

def remove_vowels(s):
    s = s.replace("/", "")
    s = s.replace("=", "")
    return re.sub(r'[\u0591-\u05BD\u05BF-\u05C2\u05C4-\u05C7]', '', s)


def get_list_of_files(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + get_list_of_files(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def verse_get_str(verse):
    words = []
    for word in verse:
        if word.attrib:  # word must have attributes
            words.append(word.text)
    return " ".join(words)


def verse_get_adjective(verse, name_word, female, book, num_chapter, num_verse, distance=1):
    ADJECTIVE_CONSTANT = 'ADJECTIVE'
    if female:
        GENDER_CONSTANT = 'FEMININE'
    else:
        GENDER_CONSTANT = "MASCULINE"
    SINGULAR_CONSTANT = 'SINGULAR'
    # example: "#BASEFORM_POS_ADJECTIVE #BASEFORM_GENDER_FEMININE #BASEFORM_NUMBER_SINGULAR #BASEFORM_STATUS_ABSOLUTE"
    bad_adjectives = ['אמרי', 'פלשתי', 'חתי', 'חי', 'יזרעאלי', 'מואבי', 'שונמי', 'עמוני', 'כרמלי', 'ראשון', 'שני',
                      'רביעי', 'שלישי', 'ארמי', 'כרתי', 'ארכי', 'מצרי', 'תימני', 'שילני', 'פלתי', 'כשי', 'תשבי',
                      'גלעדי', 'לוי']
    bad_adjectives.clear()
    bad_adjectives = ['חי']
    name_index = -1
    word_list = []
    cur_index = 0
    for word in verse:
        word_list.append(word)
        if word == name_word:
            name_index = cur_index
        cur_index += 1

    if name_index == -1:
        print("verse_get_adjective error") # should never get here
        exit(1)

    for i in range(distance*2+1):
        index = name_index + (i - distance)
        if index < 0 or index >= len(word_list):
            continue

        word = word_list[index]
        if word.attrib:  # word must have attributes
            for m in word:
                ana = m.attrib.get('ana', None)
                if ana and ADJECTIVE_CONSTANT in ana and GENDER_CONSTANT in ana and SINGULAR_CONSTANT in ana:
                    adj = remove_vowels(str(word.attrib['lemma']))
                    if adj not in bad_adjectives:
                        if not female and adj == "גדי":
                            s = "דמות: " + remove_vowels(str(name_word.attrib['lemma'])) + ", "
                            s += "ספר " + "'" + book + "'" + ", " + "פרק " + num_chapter + ", " + "פסוק " + num_verse
                            print(s)
                            verse_str = ""
                            for w in word_list:
                                if w.attrib:
                                    verse_str += w.text + " "
                            print('    ' + "”" + verse_str.strip() + "“")
                        #    print(remove_vowels(str(name_word.attrib['lemma'])) + ". " + adj + ". ", end="")
                        return adj

    return None


def get_occurrences(book_path, women_list, men_list):
    book_name = Path(book_path).stem
    book_name_heb = gematria.BOOKS[book_name]
    global total_women_occ, total_men_occ

    books_occ[book_name_heb] = {"women_appearances":0, "men_appearances":0}

    tree = et.parse(book_path)
    root = tree.getroot()

    num_chapter = 1
    for chapter in root[1][0]:  # root['text']['book']['chapter']
        num_verse = 1
        for verse in chapter:
            for word in verse:
                if word.attrib:  # word must have attributes
                    if word.attrib['root'] == PRIVATE_NAME:
                        name = remove_vowels(str(word.attrib['lemma']))
                        if name in women_list:
                            if name not in women_occ:
                                women_occ[name] = {APPEARANCE_COUNT:0, ADJECTIVES:[], APPEARANCES:[]}
                            women_occ[name][APPEARANCE_COUNT] += 1
                            verse_str = verse_get_str(verse)
                            new_app = {"book":book_name_heb, "chapter_id":gematria.idx_to_gem(num_chapter),
                                       "verse_id":gematria.idx_to_gem(num_verse), "verse":verse_str}
                            women_occ[name][APPEARANCES].append(new_app)
                            books_occ[book_name_heb]["women_appearances"] += 1

                            adj = verse_get_adjective(verse, word, True, book_name_heb,
                                                      gematria.idx_to_gem(num_chapter), gematria.idx_to_gem(num_verse))
                            if adj:
                                adj_map = {}
                                for woman_adj in women_occ[name][ADJECTIVES]:
                                    if woman_adj['adjective'] == adj:
                                        adj_map = woman_adj
                                        adj_map['occurrences'] += 1
                                        break
                                if not adj_map:
                                    women_occ[name][ADJECTIVES].append({'adjective':adj, 'occurrences':1})

                            total_women_occ += 1
                        elif name in men_list:
                            if name not in men_occ:
                                men_occ[name] = {APPEARANCE_COUNT: 0, ADJECTIVES:[], APPEARANCES: []}
                            men_occ[name][APPEARANCE_COUNT] += 1
                            verse_str = verse_get_str(verse)
                            new_app = {"book": book_name_heb, "chapter_id": gematria.idx_to_gem(num_chapter),
                                       "verse_id": gematria.idx_to_gem(num_verse),"verse":verse_str}
                            men_occ[name][APPEARANCES].append(new_app)
                            books_occ[book_name_heb]["men_appearances"] += 1

                            adj = verse_get_adjective(verse, word, False, book_name_heb,
                                                      gematria.idx_to_gem(num_chapter), gematria.idx_to_gem(num_verse))
                            if adj:
                                adj_map = {}
                                for man_adj in men_occ[name][ADJECTIVES]:
                                    if man_adj['adjective'] == adj:
                                        adj_map = man_adj
                                        adj_map['occurrences'] += 1
                                        break
                                if not adj_map:
                                    men_occ[name][ADJECTIVES].append({'adjective': adj, 'occurrences': 1})

                            total_men_occ += 1
            num_verse += 1
        num_chapter += 1



def get_top_occurences(figures_occ, count):
    fig_names = figures_occ.keys()
    full_list = []

    for name in fig_names:
        full_list.append({"name":name, "appearances": figures_occ[name]["appearance_count"]})
    full_list.sort(key= lambda x: x["appearances"], reverse=True)
    top_figs = full_list[:count]

    return top_figs


def get_top_adjectives(figures_occ, count):
    fig_names = figures_occ.keys()
    full_list = []
    full_map = {}

    for fig_name in fig_names:
        adjectives = figures_occ[fig_name][ADJECTIVES]
        for adj in adjectives:
            adj_name = adj['adjective']
            if adj_name not in full_map:
                full_map[adj_name] = {'adjective':adj_name, 'occurrences':0}
            full_map[adj_name]['occurrences'] += adj['occurrences']

    for key in full_map.keys():
        full_list.append(full_map[key])

    full_list.sort(key=lambda x: x["occurrences"], reverse=True)
    top_figs = full_list[:count]

    return top_figs


# ----- load data ------
books_file = open('data\\books.txt', encoding='utf-8')
books_list = books_file.read().split('\n')

men_file = open('data\\men.txt', encoding='utf-8')
men_list = men_file.read().split('\n')

women_file = open('data\\women.txt', encoding='utf-8')
women_list = women_file.read().split('\n')

# ----- retrieve women/men info, book info -----
print("getting occurrences in all books...")
all_books = get_list_of_files("data\\books\\")
for book_path in all_books:
    get_occurrences(book_path, women_list, men_list)

top10_women_occ = get_top_occurences(women_occ, 10)
top10_men_occ = get_top_occurences(men_occ, 10)

top10_women_adj = get_top_adjectives(women_occ, 20)
top10_men_adj = get_top_adjectives(men_occ, 20)

# printing outputs...
# other outputs are retrieved using (very) short scripts

print("writing results\\women_occ.txt ...")
with open('results\\women_occ.txt', 'w', encoding='utf-8') as f:
    print(women_occ, file=f)

print("writing results\\top10_women_occ.txt ...")
with open('results\\top10_women_occ.txt', 'w', encoding='utf-8') as f:
    print(top10_women_occ, file=f)

print("writing results\\top10_women_adj.txt ...")
with open('results\\top10_women_adj.txt', 'w', encoding='utf-8') as f:
    print(top10_women_adj, file=f)

print("writing results\\men_occ.txt ...")
with open('results\\men_occ.txt', 'w', encoding='utf-8') as f:
    print(men_occ, file=f)

print("writing results\\top10_men_occ.txt ...")
with open('results\\top10_men_occ.txt', 'w', encoding='utf-8') as f:
    print(top10_men_occ, file=f)

print("writing results\\top10_men_adj.txt ...")
with open('results\\top10_men_adj.txt', 'w', encoding='utf-8') as f:
    print(top10_men_adj, file=f)

print("writing results\\books_occ.txt ...")
with open('results\\books_occ.txt', 'w', encoding='utf-8') as f:
    print(books_occ, file=f)

print("writing results\\total_women_men.txt ...")
with open('results\\total_women_men.txt', 'w', encoding='utf-8') as f:
    print("total women/men occ: " + str(total_women_occ) + "/" + str(total_men_occ), file=f)

print("writing results\\books.csv ...")
with open('results\\books.csv', 'w', encoding='utf-8') as f:
    print(" ," + "נשים" + "," + "גברים", file=f)
    for book in books_occ:
        print(book + "," + str(books_occ[book]["women_appearances"]) + "," + str(books_occ[book]["men_appearances"])
              , file=f)