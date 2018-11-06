import os
import re
# to create a zip object you must use zipfile module. in the code it looks like zipfile.ZipFile(file). so to simplify
# importing ZipFile from zipfile as z.... then zipfile.ZipFile(file) = z(file)
from zipfile import ZipFile as z



# Setting my directories
prodDir = r'Some/prod/dir'
exportDir = r"Some/export/dir"

# List of castings
serialnumbers = ["someSN#B", "someSN#D", "someSN#A", "someSN#B", "someSN#A", "someSN#A", "someSN#A", "someSN#A",
                 "someSN#E", "someSN#J", "someSN#C", "someSN#D", "someSN#E", "someSN#E", "someSN#D", "someSN#C",
                 "someSN#K", "someSN#S", "someSN#L", "someSN#K", "someSN#L", "someSN#K", "someSN#H", "someSN#E",
                 "someSN#N", "someSN#V", "someSN#N", "someSN#N", "someSN#T", "someSN#P", "someSN#L", "someSN#U",
                 "someSN#S", "someSN#Y", "someSN#T", "someSN#S", "someSN#V", "someSN#Y", "someSN#S", "someSN#Y"]



# Created a dictionary that will have keys that are the mold numbers and a list of corresponding zip files as values.
zipsdict = {}

# Empty list to append all found zip files to.
zips = []

# Walk the entire Part# production folder and append any .zip file that starts with Part# (to exclude job number zips) to
#  the zips list.
for root, dirs, files in os.walk(prodDir):
    # Because this is a walk...files = every possible file in the entire Part# production folder!
    for file in files:
        if file.endswith(".zip") and file.startswith("Part#"):
            # use os.path.join to get the full file path not just file name. root = the full path leading up to the
            # file name
            zips.append(os.path.join(root, file))

# iterate over the serialnumbers list, extract the mold number and create regular expressions to find the first
# round, and remaining rework round zip files.
for sn in serialnumbers:
    mold = sn[:-1]
    # These will be used as a pre-defined pattern or template.
    first = re.compile(r'Part# Mold {}.zip'.format(mold))
    rwrk = re.compile(r'Part# Mold {} Rework #\d.zip'.format(mold))

    # Filter through zip files with regex templates and consolidate like mold zip files into lists and set those lists
    # as values in a the zipdict dictionary with the mold number as the key.
    for file in zips:
        # fist.search(file) searches the file name (string) for the re.compile pattern (line 39) created above,
        # return is None by default if nothing is found so... if first.search(file) != None is not necessary.
        if first.search(file) or rwrk.search(file):
            # if stripping the letter from the sn results in a mold number that is already a key in the dictionary
            # and that current file has not yet been added to that molds list of zip files, the current zip file
            # is appended to the list of zip files for that mold...print the dictionary zipsdict after this loop to see.
            if mold in zipsdict.keys() and file not in zipsdict[mold]:
                zipsdict[mold].append(file)
            # if the resulting mold number is not yet a key in the dictionary, a new key is made with a new list
            # containing the current file.
            else:
                zipsdict[mold] = [file]
# print(zipdict)

# Deep breaths....

# starts a for loop for each sn in the list of serial numbers. each time it moves to the next serial number the "next"
# variable is set to False and the mold number is reassigned. Since there is multiple nested for loops i use the "next"
#  variable to control when to break my way back to the top for loop.
for sn in serialnumbers:
    next = False
    mold = sn[:-1]
    # iterate over the dictionary keys, as long as next is still False it wont move to the next serial number.
    for key in zipsdict.keys():
        if next == True:
            break
        else:
            # Compares the current key (mold number) to the mold number gathered from stripping the letter off of the
            #  serial number.
            if key == mold:
                # if the current sn mold number and dict key match it reverses the list of zip files that corresponds
                #  to that key in the dictionary and creates a zip object out of the each zipped file and checks to
                # see if the current serial number from the first for loop exists in the list of members for that zip
                #  file. if not it loops to the next zip file up..ex: Rework #3 to Rework #2...ect.
                for file in reversed(zipsdict[key]):
                    f = z(file, "r")
                    if "{}.stl".format(sn) in f.namelist():
                        # if the serial number is found among the zip files members it is then extracted to the
                        # exportDIR defined in the beginning of the script.
                        f.extract("{}.stl".format(sn), exportDir)
                        # since we found our STL we don't need to continue looping through the rest of the zip files
                        # because we already have the latest version of that STL. So we set next to True so the
                        # script will break its way back up to the sn for loop and move onto the next serial number.
                        next = True
                        print("{},{}".format(sn, file))
                        break
                    else:
                        # if the STL wasn't found in the latest zip file, it will continue the for loop the next most
                        # recent zip file.
                        print("{} not in {}".format(sn, file))
