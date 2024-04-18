import re

# text = """
# # Adding a new Consortium
# We wish to add a new consortium to [MIP_Consotiums](https://github.com/wolfiex/mip-cmor-tables/blob/main/MIP_consortiums.json)

# Use the below table to provide your consortium names

# ## Do not forget to add consortium name to issue title.  


# **Name**
# CONSORTIUM-NAME

# **Who is this part of **
# - CMIP institution 1 
# - CMIP institution 2
# """

import sys
text = sys.argv[1]

# Define regular expressions to extract the values
name_regex = r"\*\*Name\*\*\n(.*?)\n"
part_of_regex = r"\*\*Who is this part of \*\*\n(.*?)\n"

# Extract values using regular expressions
consortium_name = re.search(name_regex, text, re.DOTALL).group(1).strip()
part_of = re.search(part_of_regex, text, re.DOTALL).group(1).strip()

print("Consortium Name:", consortium_name)
print("Part of:", part_of)
