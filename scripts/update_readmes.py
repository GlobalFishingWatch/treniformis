from __future__ import print_function
import os
from glob import glob
from utility import asset_dir
from utility import top_dir
from collections import OrderedDict
from collections import namedtuple
import yattag

Appendix = namedtuple('Appendix', ['link', 'name', 'content'])


def update_readmes(top, doc):

    appendices = []
    base = os.path.dirname(top)
    last_level = -1
    doc.line('h1', 'Treniformis')
    with doc.tag('a', name='contents'):
        doc.line('h2', 'Contents')
    for linkno, (root, dirs, files) in enumerate(os.walk(top)):
        dirs[:] = sorted(x for x in dirs if not x.startswith('.'))
        data_files = sorted(x for x in files if not (x.startswith('.') or x.lower().startswith('readme')))
        readmes = sorted(x for x in files if x.lower().startswith('readme'))
        if len(readmes) > 1:
            raise RuntimeError('multiple README files in ' + top)
        link = 'link-{}'.format(linkno)
        relpath = os.path.relpath(root, base)
        name = os.path.basename(root)
        level = relpath.count('/')
        if level > last_level:
            doc.asis('<ul>')
        if level < last_level:
            doc.asis('</ul>')
        last_level = level
        with doc.tag('li'):
            if readmes:
                doc.line('a', name, href='#'+link)
            else:
                doc.text(name)
        with doc.tag('ul'):
            for dfile in data_files:
                dname = os.path.splitext(dfile)[0]
                doc.line('li', dname)
        if readmes:
            readme_path = os.path.join(root, readmes[0])
            with open(readme_path) as f:
                readme = f.read()
        else:
            readme = None
        appendices.append(Appendix(link, name, readme))

    for i in range(last_level):
        doc.asis('</ul>')

    doc.line('h2', 'READMEs')    

    for apdx in appendices:
        # TODO, pull in text from README
        if apdx.content:
            with doc.tag('a', name=apdx.link):
                with doc.tag('h3'):
                    doc.text(apdx.name + ' ')
                    doc.line('a', '[toc]', href='#contents')
                doc.line('pre', apdx.content)



if __name__ == '__main__':
    top = os.path.join(asset_dir, "GFW")
    doc = yattag.Doc()
    update_readmes(top, doc)
    result = yattag.indent(doc.getvalue())
    with open(os.path.join(top_dir, "contents.html"), 'w') as f:
        f.write(result)
