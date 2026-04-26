import os, shutil

def copy_dir(source, destination):
    if not os.path.exists(source):
        raise ValueError(f"Source path does not exist: {source}")
    if not os.path.exists(destination):
        os.mkdir(destination)
    source_contents = os.listdir(source)
    for item in source_contents:
        fullpath_source = os.path.join(source, item)
        fullpath_dest = os.path.join(destination, item)
        if os.path.isfile(fullpath_source):
            shutil.copy(fullpath_source, fullpath_dest)
        else:
            copy_dir(fullpath_source, fullpath_dest)