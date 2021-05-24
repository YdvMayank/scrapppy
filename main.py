import csv
import sqlite3
import os
from bs4 import BeautifulSoup
import nltk


conn = sqlite3.connect("ipr.db")
c = conn.cursor()

try:
    c.execute("""CREATE TABLE er_analysis(primary_key VARCHAR(32), tm_application_no VARCHAR(16), tm_applied_for VARCHAR(1024), tm_applied_for_len VARCHAR(32),  tm_conflict_no VARCHAR(16), tm_conflict_class VARCHAR(64), tm_conflict_applied_for VARCHAR(1024), tm_conflict_applied_for_len VARCHAR(32),publication_details_conflict_journal_no VARCHAR(32), proprietor_conflict_name VARCHAR(1024), proprietor_conflict_address VARCHAR(1024), status_conflict VARCHAR(32), date_of_application_conflict VARCHAR(32), text_distance INT)""")

except:
    pass

count = 0
file1 = open("log.txt", "a")
path = "C:\\Users\\admin\\Desktop\\problem"
os.chdir(path)

def html_parser(file_path):
    try:
        soup = BeautifulSoup(open(file_path, encoding="utf8"), "html.parser")
        # print(soup)
        total_table = 0
        indexx = []
        span = soup.find("span")
        table = span.find_all("table")
        #print(len(table))
        for i in table:
            td1 = i.find_all("td")
            for j in td1:
                if (j.text == "LOCATION: SECTION: EXMREPORT: EXM007"):
                    #print(j.text)
                    total_table += 1
                    #print(table.index(i))
                    indexx.append(table.index(i))

        #print("Hello", indexx)
        if (total_table == 1):
            td = table[indexx[0]].find_all("td")[1]
            a = td.text.split()
            #print(a)
            tm_application_no = a[a.index("NUMBER:") + 1]
            b = a[a.index(":") + 2:]
            d = " "
            tm_applied_for = d.join(b)[1:-1]
            tm_applied_for_len = str(len(tm_applied_for))
            tab5 = table[indexx[0] + 3:-2]
            #print(tm_applied_for, tm_application_no)
            if len(tab5) == 0:
                tm_conflict_no = None
                tm_conflict_class = None
                confMark = None
                confMark_len = None
                journal_no = None
                proprietor_name = None
                proprietor_address = None
                status = None
                date = None
                textDistance = None
                primary_key = tm_application_no
                #print("Hello")
                #print(primary_key, tm_application_no, tm_applied_for, tm_conflict_no, tm_conflict_class, confMark, journal_no, proprietor_name, proprietor_address, status, date, textDistance)
                c.execute('''INSERT INTO er_analysis VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (primary_key, tm_application_no, tm_applied_for, tm_applied_for_len, tm_conflict_no, tm_conflict_class, confMark, confMark_len, journal_no, proprietor_name, proprietor_address, status, date, textDistance))

            tab5 = table[indexx[0] + 3:-2]
            for i in tab5:
                rows = i.find_all("td")
                tm_conflict_no = rows[0].text
                tm_conflict_class = rows[1].text
                confMark = rows[2].text.strip()
                confMark_len = str(len(confMark))
                journal_no = rows[3].text
                proprietor_name = rows[4].text
                proprietor_address = rows[5].text
                status = rows[6].text
                date = rows[8].text[17:]
                textdistance = nltk.edit_distance(confMark.lower(), tm_applied_for.lower(), transpositions=False)
                primary_key = tm_application_no + tm_conflict_no
                #print(confMark, ", " , tm_applied_for, textdistance)
                print(primary_key, tm_application_no, tm_applied_for, tm_applied_for_len, tm_conflict_no, tm_conflict_class, confMark,confMark_len, journal_no, proprietor_name, proprietor_address, status, date, textdistance)
                c.execute('''INSERT INTO er_analysis VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (primary_key, tm_application_no, tm_applied_for, tm_applied_for_len, tm_conflict_no, tm_conflict_class, confMark, confMark_len, journal_no, proprietor_name, proprietor_address, status, date, textdistance))


        else:
            tab1 = table[indexx[0] + 3: indexx[1] - 3]
            tab2 = table[indexx[1] + 3: -2]
            tab = tab1 + tab2
            #print(tab2)
            td = table[indexx[0]].find_all("td")[1]
            a = td.text.split()
            #print(a)
            tm_application_no = a[a.index("NUMBER:") + 1]
            b = a[a.index(":") + 2:]
            d = " "
            tm_applied_for = d.join(b)[1:-1]
            tm_applied_for_len = str(len(tm_applied_for))
            #print(tm_applied_for, tm_application_no)
            if len(tab) == 0:
                tm_conflict_no = None
                tm_conflict_class = None
                confMark = None
                confMark_len = None
                journal_no = None
                proprietor_name = None
                proprietor_address = None
                status = None
                date = None
                textDistance = None
                primary_key = tm_application_no
                #print("hi")
                #print(primary_key, tm_application_no, tm_applied_for, tm_conflict_no, tm_conflict_class, confMark, journal_no, proprietor_name, proprietor_address, status, date, textDistance)
                c.execute('''INSERT INTO er_analysis VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (primary_key, tm_application_no, tm_applied_for, tm_applied_for_len, tm_conflict_no, tm_conflict_class, confMark, confMark_len, journal_no, proprietor_name, proprietor_address, status, date, textDistance))

            for i in tab:
                rows = i.find_all("td")
                tm_conflict_no = rows[0].text
                tm_conflict_class = rows[1].text
                confMark = rows[2].text.strip()
                confMark_len = str(len(confMark))
                journal_no = rows[3].text
                proprietor_name = rows[4].text.strip()
                proprietor_address = rows[5].text.strip()
                status = rows[6].text
                date = rows[8].text[17:]
                textDistance = nltk.edit_distance(confMark.lower(), tm_applied_for.lower(), transpositions=False)
                primary_key = tm_application_no + tm_conflict_no
                #print(textDistance)
                #print(confMark, ", " , tm_applied_for, textDistance)
                print(primary_key, tm_application_no, tm_applied_for, tm_applied_for_len, tm_conflict_no, tm_conflict_class, confMark,confMark_len, journal_no, proprietor_name, proprietor_address, status, date, textDistance)

                c.execute('''INSERT INTO er_analysis VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (primary_key, tm_application_no, tm_applied_for, tm_applied_for_len, tm_conflict_no, tm_conflict_class, confMark, confMark_len, journal_no, proprietor_name, proprietor_address, status, date, textDistance))



    except:
        file1.write(file + " : " + "Error Occured\n")

    else:
        file1.write(file + " : " + "Done\n")


for file in os.listdir():
    if file.endswith(".html"):
        file_path = f"{path}\{file}"
        print(file)
        html_parser(file_path)

    # call read text file function

conn.commit()
#print("Completed")

# c.execute('''SELECT * FROM er_analysis''')
# print(c.fetchall())
#
# c.execute('''SELECT max(rowid) from er_analysis''')
# n = c.fetchone()[0]
# print(n)

n_estimate = c.execute("SELECT COUNT() FROM er_analysis").fetchone()[0]
print(n_estimate)

a = c.execute("SELECT COUNT(DISTINCT tm_application_no) FROM er_analysis").fetchone()[0]
print(a)

file1.close()
conn.close()