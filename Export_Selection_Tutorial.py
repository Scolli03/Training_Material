# -*- coding: utf-8 -*-
# Importing os lets me navigate and manipulate files and folders, csv allows me to read and write from/to csv files,
# and re is short for regular expression which I use to strip directories or serial numbers from a string.
import gom
import os
import csv
import re

'''Breakdown of the Element Explorer Location of Information will be presesnted as (F2) = [Object Group](First Box of options){Second Box of Options}'''

# These are just some variables I declared ahead of time, you can declare later in the script as long as you do so before you try to use them.
# To iterate over my list of alignments without the need for a nested forloop.
alignIndex = 0
# This is just to append a number to any exported csv filename that isnt the first export so I can easily call it and delete it.
fileCount = 0
# It was just simpler to use a variable than to constantly manipulate the file path string.
fileExtenstion = ".csv"
# This function takes information from the stl file and gets the serial number and path to the files location.


def getExportName():
    # Assings the variable file with the value of the current meshes file location (F2)=[Elements](Actual Meshes/Meshes/The mesh name){Information/Project File}. Note that the inital value will display the acutal mesh name where gom.app.project.actual_master is in the brackets.
    # I replaced the specific mesh name with a second value I pull from the Inster Value (F2) found not in Elements but in the Project drop down. (F2)=[Project](project){Project information/Actual master}
    file = gom.app.project.actual_elements[gom.app.project.actual_master].import_information.file
    # Since the program only lets me pull the full file path including the name, I had to create a second variable that was a string of the file location minus the length of the
    # name of the file itself. The value for the name itself is (F2)=[Elements](Actual Meshes/Meshes/The mesh name){Information/Name}. This is done inserting the (F2) value for the
    # meshes file path but adding a bracket with a colon in it. Depending on the number that come before and after the colon will dictacte where the new string will start and stop.
    # In this case I wanted everything from the begging to right before the name of the file itself. Then I had to put a -4 after the call for just the name itself to compensate for the file extension.
    meshDirectory = gom.app.project.actual_elements[gom.app.project.actual_master].import_information.file[:-len(
        gom.app.project.actual_elements[gom.app.project.actual_master].import_information.name)-4]
    # This creates a junk variable to reference after the regular expression search. The variable is = to the re.search function. The parameters in the parenthesis always begin with r' and end with '.
    # What comes between the two single quotes dictates what the function is searching for. It is VERY specific if not told otherwise. \S tells and \. before and after the inside parenthesis tells the
    # function what to look between. The capital S says im looking for a space but I DONT wasnt to actually include the space in my result, while a lower case s would. I currently dont know how to say look for a "." without including it.
    # This is compensated for in the next step.
    p = re.search(r'\S(\w*\d*)\.', file)
    # This creates your variable you wish to use. Your variable is equal the the junk variable with the group function applied. This groups the results of the search, can have mulitple results if search is created for it. That however
    # gets a little more complex. Notice the group function has () at the end. That signifies its a function call. the [:-1] says that I want the result of the search minus the last character. The "."
    sn = p.group()[:-1]
    # A final variable is made that combines previously gathered information into your FIANL result. This is an example of string formatting. Instead of plugging the variables directly into the string. Substitute them with a "{}"
    # Then at the end of the string call the format function, and add your variables there in the order they are to be inserted in the string.
    exportName = "{}{} Data".format(meshDirectory, sn)
    # This is the return for the function. Not all functions have returns. A function that manipulates already creadted objects such as lists dont need to return the object. But if an object is created within the function itself
    # Then in order to use the information a variable later in the script must be set to = the function call and will have the value of the functions return.
    return exportName


def getAlignments():
    # This is a faster way of created a list then using a multi line for loop with if statements. First the variable is created and set equal to a list []. But rather than leave it a blank list and appending items later
    # we can just populate the brackets with the parameters of what constitutes and item of that list. Its essentially a list with a nested for loop and if statement in one line. ".name" is a parameter you can call for
    # alignments that you get from (F2) and it return just the alingment name. This is found in (F2)=[Project](project){Project information/Alignment/Name}. The Element value for the list of alignments is found in
    # (F2) = [Elements](Alighnments/Main Alignments). So this statement says for each alignment (align) in the list alignments in main alignments, add the align.name (just its name) to the list.
    currentAlignment = [align.name for align in gom.ElementSelection(
        {'category': ['key', 'elements', 'explorer_category', 'alignment', 'object_family', 'alignment_main']})]
    # For some reason it kept return the alignment names starting with the last. This may not be an issue but I wanted to work from the top down. So by using your list variable and calling the reverse() function on it. It just
    # inverts the order the the list.
    currentAlignment.reverse()
    # Another return because this list is created within the function itself.
    return currentAlignment


def sortByTag():
    # This time I created my variable first, a dictionary. A dictionary holds values such as variables or lists but also asings each value or set of values a Key. That way you can access that information by calling
    # the dictionary's key.
    obj = {}
    # So for each alignment that was added to the list currentAlignment in the previous function, we will create a  list dynamically of the elements that correspond with that alignment by wether or not they have the
    # alignment name in thier list of tags. the first part obj[align+"_exports] creates the key name. so the key name for each set of elements will be the current alignment in the list plus the words "_exports". This is set
    # equal to the list itself. Again we are nesting in the for loop and if statement directly into the creation of the list. elem for elem mean for each element, in the selected Element Value list of the current projects
    # deviation lables found in (F2) = [Elements](Inspection/Deviation Lables). IF that devialtion lable has a tag that is the current alignment in the list. Then that label belongs in the currently generating list.
    for align in currentAlignment:
        obj[align+"_exports"] = [elem for elem in gom.ElementSelection(
            {'category': ['key', 'elements', 'explorer_category', 'inspection', 'object_family', 'deviation_label']}) if align in elem.tags]
    # This returns the dictionary contiaing the different lists of elements and thier corresponding Keys.
    return obj


# This creates the currentAlignment variable outside the function and sets it equal to the return of that function. Which is in fact the list of alignments.
# Notice again the closed () and the end of the function call. If the function itself did not contain the neccessary information. You would add that info here in the () and it would be represented in the def of the function.
# ex: def getAlignments(some variable):
# currentAlignment = getAlignments((F2) = [Elements](Alighnments/Main Alignments))
currentAlignment = getAlignments()
# This just get the length of the list of alignments. By length I mean number of alignments in the list.
alignCount = len(currentAlignment)
# This creates the dictionary oustide of the fucntion and set it equal to the returned value of the function wich is the dictionary created inside the fucntion. This does not have to be named the same as the functions return
# I only did that for simplicity, just remember whatever you call it here is how you will refer to it later in the script.
obj = sortByTag()
# This creates a list of just the keys within the newly created dictionary. This is gather by the fucntion .keys() that follows the name of your dictionary. I will show a long hand example of creating this list.
#exportLists = []
# for key in ob.keys():
#	exportLists.append(key)
# remeber!! when createing your empty list, not to create it within the for loop itself because every time the loop runs it will recreate it as an empty list.
exportLists = [key for key in obj.keys()]
# This gets the return from the function getExportName() and sets the variable exportName = to the functions return. Once again I did not have to call this variable exportName. But what I do call it I must from here out refer to it as such.
exportName = getExportName()

# This just makes sure that the current table view shows only visible elements. This is just something I recorded.
gom.script.table.set_list_mode(list_mode='all visible inspection elements'):

    # This for loop uses all the previously created information. This is where all your hard work wil get put to use!
    # If you fully understand everything that you've read so far....then you probably dont even need this tutorial...otherwise, keep trudging on...it get easier....ish.

    # So exportLists is actually a list of the keys in our obj dictionary. each key represents the corresponding list of elements. By doing it this way we can refer to all the elements in the list at once by refering to the lists key.
    # The word export in the for loop can be anything you want. This is just a representative variable which you will use to refer to each key as it is its turn in the loop. Every time the loop runs. The new key that it is calling
    # will be refered to as export.
for export in exportLists:
    # recorded myself making elements exlusive, the replaced the recorded elements with a dictionary call using my desired list of elements key. Remember export IS each key. I could be specific and say obj.get('AH|AG|AZ_exports')
    # Just remember when you call the .get() function on a dictionary. The key that you put in the function call must be a string. Thus the single quotes. Our list of keys are already string so the export variable that represents
    # each key is fine.
    gom.script.cad.show_element_exclusively(elements=obj.get(export))

    # This is a recording of reseting the zoom so all elements are visible and show up on the table.
    gom.script.view.adapt_zoom(use_animation=False)

    # Recording of setting all the elements visualization in the my current dictionary selection to Results. I only replaced the list of recorded elements. You must leave the other criteria. {'attachment_group': [None, 'criterias']}
    gom.script.sys.edit_properties(
        data=gom.ElementSelection(
            obj.get(export), {'attachment_group': [None, 'criterias']}),
        elem_show=True,
        label_show=True,
        label_template='Results')

    # Sets the initial file path name. This is just done by combining two previously created variables. Be aware of which variables contain "\" when using this method for creating directories. If the first variable doesnt end with
    # "\" then the second should start with it. or add it in manually like so. exportName + "\" + fileExtenstion
    file = exportName+fileExtenstion

    # This checks to see if the file already exists. If it doesnt meaning this is the first export, Then this loop is skipped, and the current file variable will be the export path for the table contents.
    # If the file has already been exported the first time. Then the logic will run. This if statement is the same as saying if os.path.isfile(file)== True:
    # os.path.isfile() function checks for the existance of a file. Remeber one equal sign assings value.....two equal sings checks if the statement is True or False.
    if os.path.isfile(file):
        # This just adds one to the fileCount variable created at the begging of the script.
        fileCount += 1
        # This uses string formatting to recreate the export path (file) using the exportName variable, substituting in the fileCount varuable, and adding on the file extenstion varible at the end.
        file = exportName + "{}".format(fileCount) + fileExtenstion
        # This add one to the alignIndex variable to use as a integer to tell wich item in the list of alignments (currentAlignment) that it should be refering to.
        alignIndex += 1
        # This is a recording of me changing the alignment then substituting in my list of current alignments at the appointed index...currentAlignment[2] is the third alignment in the list since list begin thier index at 0.
        gom.script.manage_alignment.set_alignment_active(
            cad_alignment=gom.app.project.alignments[currentAlignment[alignIndex]])
        # This recalculates not the whole project but only the selected elements defined by the dictionary call using the current key represented by export. This saves signifant time for recalculations.
        gom.script.sys.recalculate_elements(
            elements=gom.ElementSelection(obj.get(export)))

    # This just asks if this is the first export. If so, alignIndex is still 0 and the above process is applied here. This must come after the check to see if the file exists. Otherwise the file variable will not have yet
    # been formatted and this will run on the second export as well. If the previous if statement is true, this will be false and will not run a second time.
    if file == exportName+fileExtenstion:
        gom.script.manage_alignment.set_alignment_active(
            cad_alignment=gom.app.project.alignments[currentAlignment[alignIndex]])
        gom.script.sys.recalculate_elements(
            elements=gom.ElementSelection(obj.get(export)))

    # Rocording of exporting the table contents. I am however using a custom table template. The only difference is in the header where "Overview" used to say "datum" now says the current alignment.
    # This header is exported each time and appended in to the original file. This is all optional...was mainly just making sure proper exports were with proper alignments.
    gom.script.table.export_table_contents(
        cell_separator=',',
        codec='iso 8859-1',
        decimal_separator='.',
        elements=obj.get(export),
        file=file,
        header_export=True,
        line_feed='\n',
        sort_column=0,
        sort_order='ascending',
        template_name='Overview With Align',
        text_quoting='',
        write_one_line_per_element=False)

    # This only runs if the current export is NOT the FIRST export by checking the current file variable.
    if file == exportName + "{}".format(fileCount) + fileExtenstion:
        # This is a function to open the csv file itself and is from the csv module we imported at the begining of the script. with open(file name, open parameter) as f: f is how you want to refer to the open file.
        # The parameter 'r' means you open it as readable only, 'w' is writeable. There are several other options depending on how you wish to manipulate the file.
        # Here file is the current file path name which has the fileCount in the name.
        with open(file, 'r') as f:
            # This opens our original file, the First export to wich we wish to append our current files information to. Thus the 'a' parameter.
            # Notice this is refered to as f_out. this refernce is what ever you want to call the file in the next steps.
            with open(exportName+fileExtenstion, 'a', newline='') as f_out:
                # this just pre-sets our csv.reader to our current file f. sets the whole call to a variable called reader. ".reader()" is the csv's module function to read csv's.
                reader = csv.reader(f)
                # Same as the reader but for the writing function.
                writer = csv.writer(f_out)
                # This for loop will loop over each row in reader wich is the reading of our current file and use the writer to append each row to the f_out file. Our first file.
                for row in reader:
                    writer.writerow(row)
                # This steps call the close() function on the desired files. This is important because if you dont call it they will stay open in the backround and you could lose unsaved informations or changes.
                f_out.close()
                f.close()
                # Finally this is a function ".remove()" from the os module that deletes a specified file. In this case the most recently exported file which is no longer needed since the information is now saved
                # in our initially exported csv.
                os.remove(file)
