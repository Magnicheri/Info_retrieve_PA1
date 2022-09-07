import json
import re
import nltk
import matplotlib.pyplot as plot
from collections import Counter
from nltk.corpus import stopwords
import numpy as np
from fpdf import FPDF
from PyPDF2 import PdfMerger
import aspose.words as aw
#rnltk.download('stopwords')


plot.title("Word Frequencies")
plot.xlim(0, 1000)
plot.ylim(0,7800)
plot.ylabel("Frequency")
plot.xlabel("Rank of word")
np.seterr(divide = 'ignore')

file = open('Final.json')
data = json.load(file)

entry =()
entry= json.dumps(data, sort_keys=False, indent=4)
entry = entry.lower()
entry_words = entry.split(" ")

stop_space =list()
stop_space.append(' ')
stop_words = stopwords.words('english')
add_words = ['',']','}']
stop_words.extend(add_words)

space_filter = list()
word_filter = list()

form = "[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

email = re.findall(form, str(entry))
emails = list()
sourceFile = open("Assignment1.txt", 'w')
for word in entry_words:
    if len(word) >= 3:
        if word.isnumeric() != True:
            if word not in stop_words:
                word_filter.append(word)
        else:
            continue
    else:
        continue

for word in entry_words:
    if word not in stop_space:
        space_filter.append(word)
    else:
        continue


for word in entry_words:
    if word in emails:
        emails.append(word)
    else:
        continue


String_nonremoved = list()
String_nonremoved = Counter(space_filter)
String_removed = list()
String_removed = Counter(word_filter)

global rank
rank = 0
dash = '-' * 60

final_email = list()
final_email = Counter(email)
print("\n\nCommon emails:", file = sourceFile)
average_length = len(entry_words) /1194
email_average = len(email) /1194
print("Average length of Document: ", file = sourceFile)
print('{:^2.3f}'.format(average_length), file = sourceFile)
print(dash, file = sourceFile)
print('{:<40s}{:>8s}'.format("Email", "Count"), file = sourceFile)
print(dash, file = sourceFile)

for word, count in final_email.most_common(30):
    print('{:<30s}{:>8d}'.format(word, count), file = sourceFile)
print("\nPercent of webpages with Email", file = sourceFile)
email_average = len(final_email) /1194
print(email_average, file = sourceFile)



print("\n\nTop 30 Most Common words without stopwords removed:", file = sourceFile)
print(dash, file = sourceFile)
print('{:<2s}{:>6s}{:^14s}{:^8s}'.format("Rank", "Word", "Count", "Percent"), file = sourceFile)
print(dash, file = sourceFile)
for word,count in String_nonremoved.most_common(30):
    rank = rank +1
    percent = count/len(entry_words)
    print('{:<6d}{:<10s}{:^8d}{:^12.6f}'.format(rank, word, count, percent), file = sourceFile)

rank = 0

print("\n\nTop 30 Most Common words with stopwords removed:", file = sourceFile)
print(dash, file = sourceFile)
print('{:<2s}{:>6s}{:^14s}{:^8s}'.format("Rank", "Word", "Count", "Percent"), file = sourceFile)
print(dash, file = sourceFile)
for word,count in String_removed.most_common(30):
    rank = rank + 1
    percent = count/len(entry_words)
    print('{:<6d}{:<10s}{:^8d}{:^12.6f}'.format(rank, word, count, percent), file = sourceFile)

rank = 0
x_plot =[]
y_plot = []

for word, count in String_removed.most_common():
    x_plot.append(rank)
    rank = rank +1
    y_plot.append(count)


sourceFile.close()
sourceRead = open("Assignment1.txt", 'r')
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size = 12)
for x in sourceRead:
	pdf.cell(200, 10, txt = x, ln = 1, align = 'L')
pdf.output("stats.pdf")
sourceRead.close()

plot.plot(x_plot, y_plot)
plot.savefig("Plot1.pdf")

plot.clf()
plot.title("Word Frequencies Log Plot")
plot.ylabel("Frequency")
plot.xlabel("Rank of word")

xlog = np.log(x_plot)
ylog = np.log(y_plot)

plot.autoscale()

plot.plot(xlog, ylog)
plot.savefig("Plot2.pdf")

pdfs = ['stats.pdf', 'Plot1.pdf','Plot2.pdf']
merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)
merger.write("Assignment1.pdf")
merger.close()

file.close()

