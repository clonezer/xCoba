# List all unused files from you xcode project

### How to use:

just run the python script wit the project as parameter:

```
python xcoba.py 'path_to_project'
```

For dynamic resource naming, the script will look for strings replacing the image number for `'%d'`.

For example, a series of images ***button_1.png, button_2.png*** and ***button_3.png*** will be searched with their original
filenames and if not found the script will try to find a reference to `'button_%d'`

**Retina display images are also searched if the non-retina display image exist.**

###TODO :

- Allow passing excluded folders.
- Better output list.
- Allow output to a file.
- Create it as an xcode plugin.


###why xCoba?
Because xCoba sounds like broom in spanish 'Escoba', then you got it, right?