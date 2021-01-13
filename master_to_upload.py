import pandas as pd
import numpy as np
import pandas as pd
import requests
import io

# Path of csrankings.csv
master_path = 'master.csv'
upload_path = 'upload.csv'
school = 'Seoul National University'

# Csrankings file update from github
r = requests.get('https://raw.githubusercontent.com/emeryberger/CSrankings/gh-pages/csrankings.csv')

# Load two csv files each
upload = pd.read_csv(io.StringIO(r.content.decode('utf-8')))
master = pd.read_csv(master_path)

# Sort master.csv by korean name and save
master = master.sort_values(by='korean_name')
master.to_csv(master_path, mode='w', index=False)

master[master.duplicated(subset=['scholarid'], keep=False)].to_csv('duplicated.csv')

faculty_id = master['scholarid'].tolist() # Faculty scholarid in master.csv
master = master[list(upload)] # Leave columns in upload.csv only

# Add or replace faculty rows
for i, id in enumerate(faculty_id) :
    faculty = master[master['scholarid']==id] # Faculty row in master.csv
    facluty_original = upload[upload['scholarid']==id] # Faculty row in upload.csv

    # If faculty not exists in upload.csv, add this in upload.csv
    if facluty_original.empty : 
        upload = upload.append(faculty)
        name = faculty.iloc[0]['name']
        print(str(i+1) + ' : ' + name + ' is appended successfully.')
    # If not, check for duplicates in two rows - 'faculty', 'facluty_original'.
    else :
        facluty_original = facluty_original.append(faculty)
        # If not duplicated, replace 'facluty_original' to 'faculty' in upload.csv.
        if not sum(facluty_original.duplicated()) :
            upload = upload[upload['scholarid']!=id]
            upload = upload.append(faculty)
            name = faculty.iloc[0]['name']
            print(str(i+1) + ' : ' + name + ' is editted successfully.')
        
# Sort upload.csv by name and save
upload = upload.sort_values(by='name')
upload.to_csv(upload_path, mode='w', index=False)