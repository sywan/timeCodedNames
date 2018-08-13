"""====================================================================================================
TripBuddyPlusPlus.py
Description:
    (1) This program copies the JPG/PNG/TIFF/BMP/GIF files in the specified source directory to a
        destination directory. If the source and destination are identical, a sub-directory "sorted" is
        forcefully created for the user.
    (2) The file names are replaced by their last updated date/time. [Obsolete: If two files were last
        updated at the same time, an incremental post-fix shall be automatically added.]
===================================================================================================="""
import os, shutil, datetime

# Enter the input and output paths, and replace '\' with '/', if any
# Any prefix or postfix spaces are removed by strip()
srcPath = input("Enter source path: ").strip().replace("\\", "/")
destPath = input("Enter destination path: ").strip().replace("\\", "/")

if not os.path.exists(srcPath) or not os.path.exists(destPath):
    if not os.path.exist(srcPath):
        print("Incorrect source path!")
    if not os.path.exist(destPath):
        print("Incorrect destination path!")
    exit(1)

# If the source dir and destination dir are identical, we create a default sub-directory "sorted"
if srcPath == destPath:
    destPath += "/tripBuddy"

output_dir = os.path.basename(destPath)
sample_tree = os.walk(srcPath)

for dirname, subdir, files in sample_tree:

    # Avoid recursive or repeated duplications
    basename = os.path.basename(dirname)
    if basename == output_dir:
        continue

    # Duplicate only candidate files with jpg, png, tiff, tif, bmp, gif extensions
    candidate_files = []
    for file in files:
        ext = file.split('.')[-1].lower()
        if ext in ["jpg", "png", "tiff", "tif", "bmp", "gif"]:
            candidate_files.append(file)

    print(len(candidate_files))
    print(candidate_files)

    # create the directory that accommodates the duplicated files
    if len(candidate_files) > 0:
        if not os.path.exists(destPath):
            os.mkdir(destPath)
    else:
        continue

    """
    Visit every .jpg/.png/.tiff/.tif/.bmp/.gif file and copy it to the specified directory.
    The file name is renamed to its time stamp per the last updated moment.
    If there already exists an identical file name, we pad "_(xx)" the end of the filename, 
    followed by its extension. Here, xx denotes the xxth occurrence of the same time stamp  
    """
    for file in candidate_files:

        ext = file.split(".")[-1].lower()
        file_full_path = dirname + "/" + file
        time_stamp = datetime.datetime.fromtimestamp(os.path.getmtime(file_full_path))
        prefix = time_stamp.strftime('%Y%m%d%H%M%S_')       # Set the prefix of the new file name
        prefix = (prefix+file).split('.')[0].lower()

        '''
        # We are now to examine whether there already exists a file with the same file name
        # In the below, we can simply ignore r and s, whereas work only on the F list
        r, s, F = list(os.walk(destPath))[0]
        already_there = [x.find(prefix)==0 for x in F]
        ifsame = already_there.count(True)
        dest_file = "{}/{}_({}).{}".format(destPath, prefix, str(ifsame).zfill(2), ext)
        '''
        # The above code is the original version of my approach and has been commented out
        # It original purpose was to deal with duplicate file names; however, it won't happen
        # in our current case
        # The below code is much simpler and works fine as well
        dest_file = "{}/{}.{}".format(destPath, prefix, ext)
        print(dest_file)
        shutil.copy(file_full_path, dest_file)




