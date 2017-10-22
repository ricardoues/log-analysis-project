#!/usr/bin/env python3

import psycopg2
import math  # to use math.floor


def write_to_file(file, result_set, number_question):

    if number_question == 1:
        header1 = "Articles"
        header2 = "Number of views"
        file.write('%-40s %6s' % (header1, header2))
        file.write("\n")

        for row in result_set:
            article = str(row[0])
            num_view = str(math.floor(float(row[1])))
            file.write('%-40s %6s' % (article, num_view))
            file.write("\n")

        file.write("\n")

    elif number_question == 2:
        header1 = "Authors"
        header2 = "Number of views"
        file.write('%-40s %6s' % (header1, header2))
        file.write("\n")

        for row in result_set:
            author = str(row[0])
            num_view = str(math.floor(float(row[1])))
            file.write('%-40s %6s' % (author, num_view))
            file.write("\n")

        file.write("\n")

    else:
        header1 = "Date"
        header2 = "Percentage of errors"
        file.write('%-40s %6s' % (header1, header2))
        file.write("\n")

        for row in result_set:
            date = str(row[0])
            percentage_error = str(float(row[1]))
            file.write('%-40s %6s' % (date, percentage_error))
            file.write("\n")

        file.write("\n")


try:
    conn = psycopg2.connect("dbname='news' user='vagrant' \
                             host='localhost' \
                             password='badpassword'")
except Exception as e:
    print("It is unable to connect to the database" + str(e))

f = open('output.txt', 'w')


cursor = conn.cursor()

cursor.execute("""select * from views_articles
                order by views desc limit 3;""")

results = cursor.fetchall()

number_question = 1
write_to_file(f, results, number_question)


cursor.execute("""select A.name, B.views
                from authors A, views_authors B
                where A.id = B.author_id
                order by views desc;""")

results = cursor.fetchall()

number_question = 2
write_to_file(f, results, number_question)


cursor.execute("""select to_char(date, 'MON DD,YYYY')
                as date,
                error
                from error_percentage
                where error > 1.0;""")

results = cursor.fetchall()

number_question = 3
write_to_file(f, results, number_question)


f.close()
conn.close()
