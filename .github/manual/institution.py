import subprocess
import json
import sys
import os

# Define the author
author = 'berndfunke'

# Define the inputs
inputs = '''
AUoT, Aristotle University of Thessaloniki, https://ror.org/02j61yw88, CMIP6
AoR, Astronomical Observatory of Rome, https://ror.org/02hnp4676, CMIP7
BAS, British Antarctic Survey, https://ror.org/01rhff309, CMIP6
EAWAG, Swiss Federal Institute of Aquatic Science and Technology, https://ror.org/00pc48d59, CMIP6
FMI, Finnish Meteorological Institute, https://ror.org/05hppb561, CMIP6, CMIP7
FU Berlin, Free University of Berlin, https://ror.org/046ak2485, CMIP6
GEOMAR, Helmholtz Centre for Ocean Research Kiel, https://ror.org/02h2x0161, CMIP6
GSFC, NASA Goddard Space Flight Center, https://ror.org/0171mag52, CMIP6
IAA-CSIC, Institute of Space Sciences, Spanish National Research Council, https://ror.org/04ka0vh05, CMIP6, CMIP7
ISSI, International Space Science Institute, https://ror.org/01xm30661, CMIP6, CMIP7
KIT, Karlsruhe Institute of Technology, https://ror.org/04t3en479, CMIP6, CMIP7
LASP, Laboratory for Atmospheric and Space Physics, University of Colorado Boulder, https://ror.org/01fcjzv38, CMIP6, CMIP7
LPC2E, Laboratory of Physics and Chemistry of the Environment and Space, https://ror.org/049k66y27, CMIP6, CMIP7
MOHC, UK Met Office, https://ror.org/01ch2yn61, CMIP6
MPS, Max Planck Institute for Solar System Research, https://ror.org/02j6gm739, CMIP6, CMIP7
NCAR, National Center for Atmospheric Research, https://ror.org/05cvfcr44, CMIP6, CMIP7
PMOD, Physikalisch-Meteorologisches Observatorium Davos, https://ror.org/02gtrqv93, CMIP6, CMIP7
UoBergen, University of Bergen, https://ror.org/03zga2b32, CMIP7
UoLeeds, University of Leeds, https://ror.org/024mrxd33, CMIP6, CMIP7
UoMontreal, University of Montreal, https://ror.org/0161xgx34, CMIP6
UoOtago, University of Otago, https://ror.org/01jmxt844, CMIP6, CMIP7
UoOulu, University of Oulu, https://ror.org/03yj89h83, CMIP6, CMIP7
UoReading, University of Reading, https://ror.org/05v62cm79, CMIP7
'''

# Split the inputs into individual entries
entries = inputs.strip().split('\n')

# Construct the command to execute
command = [sys.executable, __file__.replace('manual','libs/parse')]

# Execute the command and capture the output
for entry in entries:
    # Split each entry into its components
    acronym, name, ror, *cmip = entry.split(',')

    # Create the payload for submission
    payload = {
        'acronym': acronym.strip(),
        'full_name': name.strip(),
        'ror': ror.strip().split('/')[-1],
    }

    # Set the environment variables
    env = os.environ.copy()
    # none, auto, manual, commented out
    env['SUBMIT'] = 'auto'
    
    env['OVERRIDE_AUTHOR'] = author
    env['ISSUE']='-1'
    env['PAYLOAD_DATA'] = json.dumps(payload)

    print(command)
    # Run the command and capture the output
    result = subprocess.run(command, env=env, capture_output=True, text=True,shell=True)

    # Print the output
    print(f"STDOUT for {payload['acronym']}:\n{result.stdout.strip()}\n")
    print(f"STDERR for {payload['acronym']}:\n{result.stderr.strip()}\n")