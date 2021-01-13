import pandas as pd
import numpy as np
import pandas as pd
import requests
import io

# Path of csrankings.csv
master_path = 'master.csv'
upload_path = 'upload.csv'
dblp_master_path = 'dblp-aliases-master.csv'
dblp_upload_path = 'dblp-aliases-upload.csv'
school = 'Seoul National University'

# Csrankings file update from github
r = requests.get('https://raw.githubusercontent.com/emeryberger/CSrankings/gh-pages/csrankings.csv')
r2 = requests.get('https://raw.githubusercontent.com/emeryberger/CSrankings/gh-pages/dblp-aliases.csv')

# Load four csv files each
upload = pd.read_csv(io.StringIO(r.content.decode('utf-8')))
master = pd.read_csv(master_path)
dblp_upload = pd.read_csv(io.StringIO(r2.content.decode('utf-8')))
dblp_master = pd.read_csv(dblp_master_path)


# Sort master.csv by korean name and save
master = master.sort_values(by='korean_name')
master.to_csv(master_path, mode='w', index=False)

# Check duplicated faculties and save to dblp-aliases
duplicated = master[master.duplicated(subset=['scholarid'], keep=False)]
duplicated.to_csv('duplicated.csv')

dblp_upload = dblp_upload.append(dblp_master)
dblp_upload = dblp_upload.drop_duplicates()

#dblp_upload_top = dblp_upload.iloc[:2]
#dblp_upload_bottom = dblp_upload.iloc[2:]
#dblp_upload_bottom = dblp_upload_bottom.sort_values(by='name')
#dblp_upload = dblp_upload_top.append(dblp_upload_bottom)

dblp_upload.to_csv(dblp_upload_path, mode='w', index=False)
    

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