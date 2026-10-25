import zipfile, os, sys, tempfile
from lxml import etree

def find_hoidong(docx_path, term='hội đồng'):
    term_lower = term.lower()
    tmp_dir = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(docx_path, 'r') as z:
            z.extractall(tmp_dir)
        doc_xml = os.path.join(tmp_dir, 'word', 'document.xml')
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(doc_xml, parser)
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        # iterate paragraphs
        matches = []
        for i, p in enumerate(tree.xpath('//w:p', namespaces=ns), start=1):
            texts = p.xpath('.//w:t/text()', namespaces=ns)
            para_text = ''.join(texts)
            if term_lower in para_text.lower():
                # provide a snippet (first 120 chars)
                snippet = para_text.strip().replace('\n', ' ')
                if len(snippet) > 120:
                    snippet = snippet[:117] + '...'
                matches.append((i, snippet))
        return matches
    finally:
        # cleanup temporary folder
        import shutil
        shutil.rmtree(tmp_dir)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python find_hoidong.py <docx_path>')
        sys.exit(1)
    path = sys.argv[1]
    results = find_hoidong(path)
    if results:
        for para, snippet in results:
            print(f'Paragraph {para}: {snippet}')
    else:
        print('No occurrence of "hội đồng" found.')
