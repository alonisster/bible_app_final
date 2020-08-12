MAP = {
    1 : 'א',
    2: 'ב',
    3: 'ג',
    4: 'ד',
    5: 'ה',
    6: 'ו',
    7: 'ז',
    8: 'ח',
    9: 'ט',
    10:'י',
    20:'כ',
    30:'ל',
    40:'מ',
    50:'נ',
    60:'ס',
    70:'ע',
    80:'פ',
    90:'צ',
    100: 'ק',
    200:'ר',
    300:'ש',
    400: 'ת',
    500: 'ך',
    600: 'ם',
    700: 'ן',
    800: 'ף',
    900: 'ץ'
}

BOOKS = {
  "Genesis": "בראשית",
  "Exodus": "שמות",
  "Leviticus": "ויקרא",
  "Numbers": "במדבר",
  "Deuteronomy": "דברים",
  "II_Kings": "מלכים ב",
  "I_Kings": "מלכים א",
  "II_Samuel": "שמואל ב",
  "I_Samuel": "שמואל א",
  "Joshua": "יהושע",
  "Judges": "שופטים",
  "Ruth": "רות",
  "I_Chronicles": "דברי הימים א",
  "II_Chronicles": "דברי הימים ב",
  "Ezra": "עזרא",
  "Nehemiah": "נחמיה",
  "Esther": "אסתר",
  "Job": "איוב",
  "Psalms": "תהילים",
  "Proverbs": "משלי",
  "Ecclesiastes": "קהלת",
  "Song_of_Songs": "שיר השירים",
  "Isaiah": "ישעיה",
  "Jeremiah": "ירמיה",
  "Lamentations": "איכה",
  "Ezekiel": "יחזקאל",
  "Daniel": "דניאל",
  "Hosea": "הושע",
  "Joel": "יואל",
  "Amos": "עמוס",
  "Obadiah": "עובדיה",
  "Jonah": "יונה",
  "Micah": "מיכה",
  "Nahum": "נחום",
  "Habakkuk": "חבקוק",
  "Zephaniah": "צפניה",
  "Haggai": "חגי",
  "Zechariah": "זכריה",
  "Malachi": "מלאכי"
}


# adapted from hebrew-special-numbers documentation
def idx_to_gem(idx, gershayim=False):
    num = idx#+1
    if(idx == 15):
        return _add_gershayim("טו")
    elif(idx == 16):
        return _add_gershayim("טז")

    parts = []
    rest = str(num)
    while rest:
        digit = int(rest[0])
        rest = rest[1:]
        if digit == 0:
            continue
        power = 10 ** len(rest)
        parts.append(MAP[power * digit])
    retval = ''.join(parts)
    # 3. Add gershayim
    return _add_gershayim(retval) if gershayim else retval


def _add_gershayim(s):
    if len(s) == 1:
        s += "'"
    else:
        s = ''.join([
            s[:-1],
            '"',
            s[-1:]
        ])
    return s