__author__ = 'rcj1492'
__created__ = '2017.06'
__license__ = 'MIT'


def generate_roadmap():

    ''' a method to generate the roadmap markdown from template and yaml details '''

    import csv
    from os import path
    from tabulate import tabulate

    components_path = 'components.csv'
    roadmap_temp = 'roadmap.md'
    docs_folder = '../docs'

    skip = False
    if not path.exists(components_path):
        skip = True
    elif not path.exists(roadmap_temp):
        skip = True
    elif not path.exists(docs_folder):
        skip = True
    roadmap_docs = path.join(docs_folder, roadmap_temp)

    if not skip:
        roadmap_text = open(roadmap_temp).read()

        components_text = open(components_path, newline='')
        components_csv = csv.reader(components_text, delimiter=',', quotechar='"')
        components_headers = []
        components_table = []
        count = 0
        for row in components_csv:
            if not count:
                components_headers = row
            else:
                components_table.append(row)
            count += 1

        def replace_url(x):
            url_text = '<a href="%s">%s</a>' % (x.group(1), x.group(0))
            return url_text

        import re
        url_regex = re.compile('\[(.*?)\]\((.*)\)')
        comp_regex = re.compile('\[\[components\]\]')
        comp_html = tabulate(components_table, components_headers, tablefmt='html')
        comp_html = url_regex.sub(replace_url, comp_html)
        roadmap_new = comp_regex.sub(comp_html, roadmap_text)

        with open(roadmap_docs, 'wt') as f:
            f.write(roadmap_new)
            f.close()


if __name__ == '__main__':
    generate_roadmap()