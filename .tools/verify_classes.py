import re

def extract_classes(path):
    text = open(path, encoding='utf-8').read()
    classes = set()
    for m in re.finditer(r'class="([^"]*)"', text):
        for tok in m.group(1).split():
            classes.add(tok)
    return classes

def css_class(text):
    escaped = re.escape(text)
    return re.compile(r'\.' + escaped.replace(r'\ ', r'\\?\s*') + r'(?=[\s.,:{>~+\[]|$)')

all_classes = set()
for f in ['index.html', 'about.html', 'demo.html']:
    all_classes |= extract_classes(f)

custom_classes = {
    'glass-card', 'blob', 'font-display', 'text-glow-white', 'glow-hover',
    'modal-panel', 'modal-active', 'modal-overlay', 'custom-scrollbar',
    'ambient-glow', 'glow-a', 'glow-b', 'matte-glass', 'group', 'hidden',
    'text-accent-gold',
}

css_text = open('tailwind.css', encoding='utf-8').read()
# build a set of escaped selector strings actually present, in Tailwind's own escaping form
# CSS escapes can be \X (literal) or \HH...  (hex codepoint, optionally followed by one space)
selectors_raw = re.findall(r'\.((?:\\[0-9a-fA-F]{1,6}\s?|\\.|[^\s{,:])+)', css_text)

def unescape(s):
    def repl(m):
        token = m.group(0)
        if re.fullmatch(r'\\[0-9a-fA-F]{1,6}\s?', token):
            return chr(int(token[1:].strip(), 16))
        return token[1]
    return re.sub(r'\\[0-9a-fA-F]{1,6}\s?|\\.', repl, s)

selector_set = set(unescape(s) for s in selectors_raw)

missing = []
for c in sorted(all_classes):
    if c in custom_classes:
        continue
    if c in selector_set:
        continue
    missing.append(c)

print(f"Total unique classes in HTML: {len(all_classes)}")
print(f"Genuinely missing ({len(missing)}):")
for m in missing:
    print(' -', m)
