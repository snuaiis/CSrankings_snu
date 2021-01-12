import pandas as pd
import numpy as np
import pandas as pd
import requests
import io

# path of csrankings.csv
master_path = "master.csv"
upload_path = "upload.csv"

# csrankings file update from github
r = requests.get('https://raw.githubusercontent.com/emeryberger/CSrankings/gh-pages/csrankings.csv')

upload = pd.read_csv(io.StringIO(r.content.decode('utf-8')))
#upload = master[master["affiliation"] == "Seoul National University"]
master = pd.read_csv(master_path)

faculty_names = master["name"].tolist()
master = master[list(upload)]

for i, name in enumerate(faculty_names) :
    faculty = master[master["name"]==name]
    facluty_original = upload[upload["name"]==name]
    if facluty_original.empty :
        upload = upload.append(faculty)
        print(str(i+1) + " : " + name + " is appended successfully.")
    else :
        facluty_original = facluty_original.append(faculty)
        if not sum(facluty_original.duplicated()) :
            upload = upload[upload["name"]!=name]
            upload = upload.append(faculty)
            print(str(i+1) + " : " + name + " is editted successfully.")
        

upload = upload.sort_values(by='name')

upload.to_csv(upload_path, mode = 'w', index=False)