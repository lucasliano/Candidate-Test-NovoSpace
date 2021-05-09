import re

mem_filename = "memdump0.mem"

# We declare lists of strings used to store the lines that will be written to the output files
lines_output = []
lines_mem = []

try:
    # We open all the files that we will used to work with
    input_file = open("testcase.v","r")

    # Regex definitions
    pattern_name = re.compile(r"\s*reg \[.*\] (\S*) \[.*\];\n")
    pattern_begin = re.compile(r"\s*initial begin\n")

    # Flow control variable
    looping_mem = False

    # Name of the register array
    mem_name = ""

    # Start reading the input verilog file
    for each_line in input_file:
        # Match definitions for each line
        match_name = pattern_name.search(each_line)
        match_begin = pattern_begin.search(each_line)


        if match_name:
            # If we find a register definition
            mem_name = match_name.groups()[0]                                               # We store the name of the register array
            lines_output.append(each_line)                                                  # We save the line
        elif match_begin:
            # If we find the 'initial begin' line
            lines_output.append('  $readmemh("{:s}", {:s});\n'.format(mem_filename,mem_name))      # We add the new syntax
            looping_mem = True                                                              # The following lines are supposed to be assignations
        elif looping_mem:
            # Looping through the assignations
            pattern_end = re.compile(r"\s*end\n")
            match_end = pattern_end.search(each_line)
            if match_end:
                # If we find an 'end' line, we stop looping
                looping_mem = False
            else:
                # If we are looking to the assignations
                pattern_hex = re.compile(r"\'h(.*)\;")                                      # Look for hex values
                match_hex = pattern_hex.search(each_line)
                lines_mem.append(match_hex.groups()[0] + '\n')                              # Store hex values

        else:
            # If the line is not important to this analisis, we save it as it is
            lines_output.append(each_line)


except Exception as e:
    print("Error while reading input file: " + e)
finally:
    input_file.close()



# Writing Verilog File
try:
    output_verilog_file = open("output.v","w")
    output_verilog_file.writelines(lines_output)
except Exception as e:
    print("Error while writing output verilog file: " + e)
finally:
    output_verilog_file.close()

# Writing Memory File
try:
    output_mem_file = open(mem_filename,"w")
    output_mem_file.writelines(lines_mem)
except Exception as e:
    print("Error while writing output memory file: " + e)
finally:
    output_mem_file.close()
