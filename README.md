# List all unused images from you xcode project

### why xCoba?
Because xCoba sounds like broom in spanish 'Escoba', then you got it, right?

### How to use:

just run the python script with path to project folder as parameter in Terminal:

```
python xcoba.py 'path_to_project'
```
and you will get `xcobaReport.html` in same directory  

For dynamic resource naming, the script will look for strings replacing the image number for `'%d'`.

For example, a series of images ***button_1.png, button_2.png*** and ***button_3.png*** will be searched with their original
filenames and if not found the script will try to find a reference to `'button_%d'`

**Retina display images are also searched if the non-retina display image exist.**

### Sample Image:

![Run](https://raw.github.com/clonezer/xCoba/master/sample1.png)

![Report in web browser](https://raw.github.com/clonezer/xCoba/master/sample2.png)