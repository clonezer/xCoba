__author__ = 'Billy Tobon (Updated by Peerasak Unsakon)'

import os
import re
import argparse
import webbrowser

parser = argparse.ArgumentParser(description='Find unused images on an xcode project.')
parser.add_argument('path', help='Project path')
args = parser.parse_args()

path = args.path
_digits = re.compile('\d')

def contains_digits(d):
    return bool(_digits.search(d))

# File size conversion by Sridhar Ratnakumar from http://goo.gl/nbAhU
def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')

def total_size(file_list):
    total = 0
    for file in file_list:
        total += file['file_size']
    return sizeof_fmt(total)

assets_list = []
source_list = []
unused = []

for dirname, dirnames, filenames in os.walk(path):

    # print path to all filenames.
    for filename in filenames:
        if filename.endswith(".png") or filename.endswith(".jpg"):
            path_to_file = os.path.join(dirname, filename)
            clean_name = filename.split('.')[0]
            if not '@2x' in clean_name:
                assets_list.append({'clean_name': clean_name, 'path_to_file': path_to_file, 'file_size': os.path.getsize(path_to_file)})

        if filename.endswith(".m") or filename.endswith(".plist") or filename.endswith(".xib") or filename.endswith(".storyboard"):
            path_to_file = os.path.join(dirname, filename)
            source_list.append(path_to_file)

    # Advanced usage:
    # editing the 'dirnames' list will stop os.walk() from recursing into there.
    if '.git' in dirnames:
        # don't go into any .git directories.
        dirnames.remove('.git')

    if '3rdParty' in dirnames:
        dirnames.remove('3rdParty')

for image in assets_list:
    is_used = False
    objcImage = image['clean_name']

    for source_file in source_list:
        f = open(source_file)
        content = f.read()
        f.close()
        image_to_search = objcImage if source_file.endswith('.m') else image['clean_name']

        if not content.find(image_to_search) == -1:
            is_used = True
            break

        if contains_digits(image_to_search):
            numbers = re.search('[0-9]+', image_to_search)
            img = re.sub(r'\d+', '%d', image_to_search)

            if not content.find(img) == -1:
                is_used = True
                break

    if not is_used:
        unused.append(image)

print '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - '
print 'scanning completed'
print '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - '
for image in unused:
    print '* %s - filesize: %s' % (image['clean_name'], sizeof_fmt(image['file_size']))
print '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - '
print '%d unused images found' % len(unused)
print '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - '    

# Generate report file
html_str = ''
html_str += '<style type=\"text/css\">'
html_str += '.tg {'
html_str += '    border-collapse:collapse;'
html_str += '    border-spacing:0;'
html_str += '    border-color:#ccc;'
html_str += '}'
html_str += '.tg td {'
html_str += '    font-family:Arial, sans-serif;'
html_str += '    font-size:14px;'
html_str += '    padding:10px 5px;'
html_str += '    border-style:solid;'
html_str += '    border-width:1px;'
html_str += '    overflow:hidden;'
html_str += '    word-break:normal;'
html_str += '    border-color:#ccc;'
html_str += '    color:#333;'
html_str += '    background-color:#fff;'
html_str += '}'
html_str += '.tg th {'
html_str += '    font-family:Arial, sans-serif;'
html_str += '    font-size:14px;'
html_str += '    font-weight:normal;'
html_str += '    padding:10px 5px;'
html_str += '    border-style:solid;'
html_str += '    border-width:1px;'
html_str += '    overflow:hidden;'
html_str += '    word-break:normal;'
html_str += '    border-color:#ccc;'
html_str += '    color:#333;'
html_str += '    background-color:#f0f0f0;'
html_str += '}'
html_str += '.tg .tg-s6z2 {'
html_str += '    text-align:center'
html_str += '}'
html_str += '</style>'
html_str += '<center>'
html_str += '    <h2>xCobaReport (%d unused images found : total size %s )</h2>' % (len(unused), total_size(unused))
html_str += '    <table class=\"tg\">'
html_str += '        <tr>'
html_str += '            <th class=\"tg-031e\">NO</th>'
html_str += '            <th class=\"tg-031e\">Image Name</th>'
html_str += '            <th class=\"tg-031e\">File Size</th>'
html_str += '            <th class=\"tg-031e\">Preview</th>'
html_str += '        </tr>'
html_str += '        <indent>'

i = 1;
for image in unused:
    html_str += '<tr>'
    html_str += '    <td class=\"tg-s6z2\">%d</td>' % i
    html_str += '    <td class=\"tg-031e\">%s</td>' % image['clean_name']
    html_str += '    <td class=\"tg-031e\">%s</td>' % sizeof_fmt(image['file_size'])
    html_str += '    <td class=\"tg-s6z2\">'
    html_str += '        <img src=\"%s\">' % image['path_to_file']
    html_str += '    </td>'
    html_str += '</tr>'
    i += 1

html_str += '        </indent>'
html_str += '    </table>'
html_str += '</center>'

Html_file= open("xCobaReport.html","w")
Html_file.write(html_str)
Html_file.close()

# Open report file in web browser
report_url = 'file://' + os.path.dirname(os.path.realpath(__file__)) + '/xCobaReport.html'
webbrowser.open_new_tab(report_url)
