import os, json, sys
import re, tqdm, time, random
from io import StringIO
from progress.bar import Bar
import collections

#labels
section = {'Projects':["projects"],'Education':["education"],'Experience':["work experience  "],'Skills':["computer skills ","skills"]}

AllSection = ["projects","education","work experience  ","computer skills ","skills"]

RequiredSkill = ["sql", "php","java","python","powerpoint","excel","web","software","word","network","cyber","security"]

ReqWeight = {"sql": 7, "php": 15,"java": 22,"python": 25,"powerpoint": 14,"excel": 2, "word": 8,"web": 22,"software": 25,"network": 18,"cyber":15,"security":19}

directory = os.getcwd()

FileScore = {}

def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    stop_words = set(stopwords.words("english"))
    for word in words:
        if word not in stop_words:
            new_words.append(word)
    return new_words

def compute_Education(iofilename):
	infile = open(iofilename)
	temp = json.load(infile)
	s = 0
	Edu_List = set()

	for i in temp['data']:
		if s == 0:
			for j in section['Education']:
				if i.strip() == j.strip():
					s = 1
					break
		elif s == 1:
			for k in AllSection:
				if k.strip() == i.strip():
					s = 2
					break
				Edu_List.add(i.strip())

	#Remove Stopword in Edu List
	for i in AllSection:
		if i.strip() in Edu_List:
			Edu_List.remove(i.strip())

	#master = 32, bachelor = 26, diploma = 12
	count  = 0
	for j in Edu_List:
		if (re.search("master", j) or re.search('\S+m-\S',j) ) and (tempScore < 98):
			count = 32
		elif ( re.search("bachelor", j) or re.search('\S+b-\S',j) ) and (tempScore < 85):	
			count = 26
		elif (re.search("diploma", j) or re.search('dip',j) or re.search('\S+m.\S',j)) and (tempScore < 75):
			count = 12
			
	infile.close()
	return count

def compute_Experience(iofilename):
	infile = open(iofilename)
	temp = json.load(infile)
	s = 0
	Exp_List = set()

	for i in temp['data']:
		if s == 0:
			for j in section['Experience']:
				if i.strip() == j.strip():
					s = 1
					break
		elif s == 1:
			for k in AllSection:
				if k.strip() == i.strip():
					s = 2
					break
				Exp_List.add(i.strip())

	#Remove Stopword in Edu List
	for i in AllSection:
		if i.strip() in Exp_List:
			Exp_List.remove(i.strip())

	#print(Exp_List)
	return 0

def compute_Skills(iofilename):
	infile = open(iofilename)
	temp = json.load(infile)
	s = 0
	Skl_List = set()

	for i in temp['data']:
		if s == 0:
			for j in section['Skills']:
				if i.strip() == j.strip():
					s = 1
					break
		elif s == 1:
			for k in AllSection:
				if k.strip() == i.strip():
					s = 2
					break
				Skl_List.add(i.strip())

	#Remove Stopword in Edu List
	for i in AllSection:
		if i.strip() in Skl_List:
			Skl_List.remove(i.strip())

	count = 0
	for j in Skl_List:
		for k in RequiredSkill:
			if(re.findall(k.strip().lower(), j.lower())):
				count += ReqWeight[k.strip().lower()]

	tempScore = 0

	if count >= 85:
		tempScore = 38
	elif count >= 60:
		tempScore = 30
	elif count >=40:
		tempScore = 22
	elif count >=29:
		tempScore = 15
	else:
		tempScore = 5

	infile.close()
	return tempScore

def main():
	#json reading

	for filelist in os.listdir(os.getcwd()+"/processed"):
		with open(os.path.join(os.getcwd()+"/processed/"+filelist),"r", errors='ignore') as rf:
			
			iofilename = os.getcwd()+"/processed/"+filelist
			sum = 0

			# "compute_Education" : 35 ,"compute_Experience": 40,"compute_Skills": 25
			task = [compute_Education,compute_Experience,compute_Skills]

			"""
			#tqdm progress bar
			for i in tqdm.tqdm(range(3)):
				time.sleep(random.randint(2,5))
				sum += task[i](iofilename)

			"""
			infile = open(iofilename)
			temp = json.load(infile)
			ids = temp["id"]
			print("\nFile Name : {}".format(filelist))
			bar = Bar('Analysing', max=3)
			for i in range(3):
				time.sleep(random.randint(2,5))
				sum += task[i](iofilename)
				bar.next()
			bar.finish()
			for i in tqdm.tqdm(range(1)):
				time.sleep(random.randint(2,5))
			print("Completed....")
			print("Score : {}".format(sum+40))
			FileScore[filelist] = [ids,sum+40]

	#preprocessing 
	sorted_x = sorted(FileScore.items(), key=lambda kv: kv[1])
	FileScorex = collections.OrderedDict(sorted_x)

	#exporting
	with open(os.path.join(os.getcwd()+"/result.json"), "w") as output_file:
		json.dump(FileScorex, output_file, indent = 2, ensure_ascii = False)

main()