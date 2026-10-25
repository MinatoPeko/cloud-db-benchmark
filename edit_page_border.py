import zipfile, os, sys, shutil, tempfile
from lxml import etree

def add_double_border(docx_path, output_path=None):
    if output_path is None:
        output_path = docx_path
    # Create a temporary directory
    tmp_dir = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(docx_path, 'r') as zip_ref:
            zip_ref.extractall(tmp_dir)
        # Path to document.xml
        doc_xml_path = os.path.join(tmp_dir, 'word', 'document.xml')
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(doc_xml_path, parser)
        root = tree.getroot()
        # Namespaces
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        # Find sectPr (section properties) – usually the last sectPr in the document
        sect_pr = root.find('.//w:sectPr', namespaces=ns)
        if sect_pr is None:
            # If not found, create one at the end of body
            body = root.find('.//w:body', namespaces=ns)
            sect_pr = etree.SubElement(body, '{%s}sectPr' % ns['w'])
        # Check if pgBorders already exists
        pg_borders = sect_pr.find('w:pgBorders', namespaces=ns)
        if pg_borders is None:
            pg_borders = etree.SubElement(sect_pr, '{%s}pgBorders' % ns['w'])
        # Define double border attributes (top, left, bottom, right)
        border_attrib = {
            f'{{{ns["w"]}}}val': 'double',   # double line
            f'{{{ns["w"]}}}sz': '12',        # size (8‑pt = 12 half‑points?)
            f'{{{ns["w"]}}}space': '24',    # space from text
            f'{{{ns["w"]}}}color': 'auto'
        }
        for side in ['top', 'left', 'bottom', 'right']:
            el = pg_borders.find(f'w:{side}', namespaces=ns)
            if el is None:
                el = etree.SubElement(pg_borders, f'{{{ns["w"]}}}{side}')
            # set attributes (override existing)
            for k, v in border_attrib.items():
                el.set(k, v)
        # Write back document.xml
        tree.write(doc_xml_path, xml_declaration=True, encoding='UTF-8', pretty_print=False)
        # Re‑zip into new docx
        if output_path == docx_path:
            # overwrite original – create a temporary zip then replace
            tmp_docx = docx_path + '.tmp'
        else:
            tmp_docx = output_path
        with zipfile.ZipFile(tmp_docx, 'w', zipfile.ZIP_DEFLATED) as zip_out:
            for foldername, subfolders, filenames in os.walk(tmp_dir):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, tmp_dir)
                    zip_out.write(file_path, arcname)
        if output_path == docx_path:
            # replace original
            shutil.move(tmp_docx, docx_path)
    finally:
        shutil.rmtree(tmp_dir)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python edit_page_border.py <docx_path> [output_path]')
        sys.exit(1)
    docx_path = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    add_double_border(docx_path, out)
    print(f'Border added to {docx_path}')
