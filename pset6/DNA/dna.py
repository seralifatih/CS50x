import sys
import csv
import re
from collections import Counter

if len(sys.argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    sys.exit()
    
with open(sys.argv[2], "r") as file:
    reader = csv.reader(file)
    for row in reader:
        DNAseq = row

DNA = DNAseq[0]

sequences = {}

with open(sys.argv[1], "r") as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        DNAsequences = row
        DNAsequences.pop(0)
        break

for item in DNAsequences:
    sequences[item] = 1

for key in sequences:
    l = len(key)
    tempMax = 0
    temp = 0
    for i in range(len(DNA)):
        # after having counted a sequence
        # skip at the end of it to avoid counting again        
        while temp>0:
            temp -= 1
            continue
# if the segment of dna corresponds to the key && 
        #there is a repetition of it 
        #increment counter        
        if DNA[i:i+l] == key:
            while DNA[i-l:i] == DNA[i:i+l]:
                temp += 1
                i += l
# compare the value to the previous longest sequence && 
            # if it is longer it becomes the new max                
            if temp > tempMax:
                tempMax = temp
                
    sequences[key] += tempMax
            





#DNAregex = re.compile(r'(AGATC|AATG|TATC|AGATC|TTTTTTCT|AATG|TCTAG|GATA|TATC|GAAA|TCTG){1,}')
#mo = DNAregex.findall(DNA)
#DNAresult = Counter(mo)

with open(sys.argv[1], newline='') as peoplefile:
    people = csv.DictReader(peoplefile)
    for person in people:
        match = 0
        for DNA in sequences:
            if sequences[DNA] == int(person[DNA]):
                match += 1
        if match == len(sequences):
            print(person['name'])
            exit()
    print("No match")