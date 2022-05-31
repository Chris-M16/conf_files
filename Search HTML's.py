import re

# Input the path of the OLD HTML file
old_file = "PATH"
# Input the path of the NEW HTML file
new_file = "PATH"
files = [old_file,new_file]

# Creates two seperate lists to store each files error codes
old_file_results = []
new_file_results = []

def vuln_codes():
    # Run files seperately through code
    for file in files:
        with open(file) as f:
            contents = f.readlines()

        # Parse through file and look at each individual line
        for line in contents:

            # Search for pattern in HTML code
            match = re.search(r'a href(.*?) - ', line)
            
            # Only runs for lines that contain any succesful search
            if match != None:
                # Split the regex find
                regex_split = str(match).split('>')
                # Split the above value
                data_split = str(regex_split[1]).split(' ')
                
                # Grabs the vulnerability number
                vuln = data_split[0]

                # Appends the vuln number to the appropriate file
                if file == old_file:
                    old_file_results.append(vuln)
                elif file == new_file:
                    new_file_results.append(vuln)
                else:
                    pass
            # Skips any line not returning a find
            else:
                pass

    # Creates list to store recurring values
    recurring = []

    # Go through each vulnerability in old HTML
    for value in old_file_results:
        # Check if the vulnerability is in the new HTML. If so append to list, else pass.
        if value in new_file_results:
            recurring.append(value)
        else:
            pass
    return(recurring)

# Prints the recurring vulnerabilities
#print(vuln_codes())

# Get the vulnerabilities name from the code
def vuln_name():
    # Create list to store names in
    list_of_names = []

    # Load the new HTML file
    with open(new_file) as f:
            contents = f.readlines()

    # For each vulnerability
    for vulnerability in vuln_codes():
        # Parse through file and look at each individual line
        for line in contents:
            # Search for pattern in HTML code
            match = re.search(r''+(vulnerability)+' .*', line)
            # Only runs for lines that contain any succesful search
            if match != None:
                # Split the line
                grab_field = line.split('<')
                # Split the above variable
                grab_name = grab_field[-2].split(' - ')
                # Check if name is in list of names
                if grab_name[-1] not in list_of_names:
                    list_of_names.append(grab_name[-1])
                else:
                    pass
            else:
                pass
    # Removes value from list as it is not needed
    list_of_names.remove('/a>')
    # Return the list of names
    return(list_of_names)

# Store functions as variables to make calling them quick
codes = vuln_codes()
names = vuln_name()

old_file_occurence = {}
new_file_occurence = {}

def occurence():
    # Run files seperately through code
    for file in files:
        with open(file) as f:
            contents = f.readlines()

            # For each vulnerability
        for vulnerability in vuln_codes():
            # Parse through file and look at each individual line
            for line in contents:
                # Search for pattern in HTML code
                match = re.search(r'a href(.*)'+vulnerability+r' (.*)', line)

                # Only runs for lines that contain any succesful search
                if match != None:
                    # Split the regex find
                    regex_split = str(match).split('>')
                    # Split the above value
                    data_split = str(regex_split[1]).split(' ')
                    
                    v_code = data_split[0]
                    # Grabs the occurence of vuln
                    occur = data_split[1]
                    # Appends the vuln number to the appropriate file
                    if file == old_file:
                        old_file_occurence[v_code]=occur
                    elif file == new_file:
                        new_file_occurence[v_code]=occur
                    else:
                        pass
                # Skips any line not returning a find
                else:
                    pass

occurence()

# For the number of recurring vulnerabilites print with the below formatting
for x in range(0,len(codes)):
    pretty = """
{number} - {name} | Occasions on OLD Scan = {old} | Occasions on NEW Scan = {new}
"""
    print(pretty.format(number=codes[x],name=names[x],old=old_file_occurence[codes[x]],new=new_file_occurence[codes[x]]))
