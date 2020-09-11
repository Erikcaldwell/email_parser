import sys
import os
from tika import parser
from dateutil.parser import parse
import shutil
import pandas as pd

#list to out output from the loop below
date_list = []
to_list = []
cc_list = []
from_list = []
subject_list = []
files_list = []

#looping through the source folder and opening pdf files
for filename in os.listdir('./source'):
    if filename.endswith(".pdf"):
         print(os.path.join(filename))
         new_filename = (os.path.join(filename))
         #opening the target PDF
         reader = parser.from_file('./source/'+filename)
         pdfText = reader['content']
         #getting the date
         date_target = pdfText.split('Sent: ')
         date_target = date_target[1].split('\n')
         date_target_final=date_target[0]
         date_entry=parse(date_target_final, fuzzy_with_tokens=True)
         #getting the recipients
         to_target = pdfText.split('To: ')
         to_target = to_target[1].split('\n')
         to_entry=to_target[0]
         try:
                cc_target = pdfText.split('Cc: ')
                cc_target = cc_target[1].split('\n')
                cc_entry=cc_target[0]
         except:
                cc_entry=''
         #getting the sender
         from_target = pdfText.split('From: ')
         from_target = from_target[1].split('\n')
         from_entry=from_target[0]
          #getting the subjet
         subject_target = pdfText.split('Subject: ')
         subject_target = subject_target[1].split('\n')
         subject_entry=subject_target[0]
         #creating a date string as index for files
         datestr = str(date_entry[0].year)+'-'+str(date_entry[0].month)+'-'+str(date_entry[0].day)+'-'+str(date_entry[0].hour)+str(date_entry[0].minute)
         # Destination path for the labeled file
         source = ('./source/'+filename)
         destination = ("./out/"+datestr+'_filename'+'.pdf')
         # Copy the content of
         # source to destination
         dest = shutil.copyfile(source, destination)
         #adding metadata to our lists
         date_list.append(datestr)
         to_list.append(to_entry)
         cc_list.append(cc_entry)
         from_list.append(from_entry)
         subject_list.append(subject_target)
         files_list.append(datestr+'_filename'+'.pdf')
    else:
        next

#creating a dataframe from our entry lists
data = {'Date': date_list, 'From': from_list, 'To': to_list,'CC': cc_list,'Subject': subject_list}
df = pd.DataFrame(data)
df.to_csv('./out/metadata.csv')
