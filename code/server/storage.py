from os import scandir

__UPLOADS__ = "uploads/"
__DOWNLOADS__ = "grayscale/"

up_relpath = ""

CURRENT_USER = ""

__AUTHENTICATION__ = {}

prediction = "None"


def setFileName(dire):
    files = [f.name for f in scandir(dire) if f.is_file()]
    if len(files) == 0:
        return '1'
    else:
        index = int(sorted(files)[-1].split('.')[0])
        if dire == __UPLOADS__:
            return str(index+1)
        else:
            return str(index)


def up_file(fname):
    key = fname.split('.')[0]
    value = __DOWNLOADS__ + fname
    __AUTHENTICATION__[key] = value
