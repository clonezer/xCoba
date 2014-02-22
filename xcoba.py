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
            if objcImage in ['Finance open Edit']:
                print "This File"  
                print source_file
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
html_str = '<style type=\"text/css\">.tg  {border-collapse:collapse;border-spacing:0;border-color:#ccc;}.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#fff;}.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#f0f0f0;}.tg .tg-s6z2{text-align:center}</style><center><h2>xCobaReport (%d unused images found : total size %s )</h2><table class=\"tg\"><tr><th class=\"tg-031e\">NO</th><th class=\"tg-031e\">Image Name</th><th class=\"tg-031e\">File Size</th><th class=\"tg-031e\">Preview</th></tr><indent>' % (len(unused), total_size(unused))
i = 1;
for image in unused:
    html_str += '<tr><td class=\"tg-s6z2\"> %d </td><td class=\"tg-031e\"> %s </td><td class=\"tg-031e\"> %s </td><td class=\"tg-s6z2\"> <img src=\"%s\"> </td></tr>' %(i, image['clean_name'], sizeof_fmt(image['file_size']), image['path_to_file'])
    i += 1
html_str += '</indent></table></center>'
Html_file= open("xCobaReport.html","w")
Html_file.write(html_str)
Html_file.close()

report_url = 'file://' + os.path.dirname(os.path.realpath(__file__)) + '/xCobaReport.html'
# Open report file in web browser
webbrowser.open_new_tab(report_url)
