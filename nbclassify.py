import sys
import string

file = open(sys.argv[1],"r").readlines()
model1 = open("nbmodel1.txt","r").readlines()
model = open("nbmodel.txt","r").readlines()
wordset = open("wordset.txt",'r').readlines()
output = open("nboutput.txt","w")
stopwords = open("stopwords.txt",'r').readlines()
stop_words = {'A','a','an','An','and','are','as','at','be','by','for','from','has','he','in','is','it','its','of','on','that','the','The','It','to','was','were','will','with'}

for sw in stopwords:
	sw = sw.strip()
	sw = sw.translate(None, string.punctuation)
	stop_words.add(sw)


pos_prior = float(model[0])
neg_prior = float(model[1])
true_prior = float(model1[0])
fake_prior = float(model1[1])

global_set = set()
word_prob_dict = dict()
true_prob_dict = dict()

for word in wordset:
	global_set.add(str(word.strip()))


for i in range(2,len(model)):
	values = model[i].strip().split(',')
	word_prob_dict[values[0]] = float(values[1])

for i in range(2,len(model1)):
	values = model1[i].strip().split(',')
	true_prob_dict[values[0]] = float(values[1])
	


#print word_prob_dict

for line in file:
	words = line.strip().split(' ')
	id_no = words[0]
	positive = pos_prior
	negative = neg_prior
	true = true_prior
	fake = fake_prior
	
	for i in range(1,len(words)):
		words[i] = words[i].lower()
		words[i] = words[i].translate(None, string.punctuation)
		if words[i] not in stop_words:
			if words[i] in global_set:
				positive += word_prob_dict[words[i]+"/"+"Pos"]
				negative += word_prob_dict[(words[i]+"/"+"Neg")]
				true += true_prob_dict[words[i]+"/"+"True"]
				fake += true_prob_dict[words[i]+"/"+"Fake"]
				
	#print positive,negative

	output.write(str(id_no))


	if max(true,fake) == true:
		output.write(" "+"True")
	else:
		output.write(" "+ "Fake")

	if max(positive,negative) == positive:
		output.write(" "+"Pos"+"\n")
	else:
		output.write(" " + "Neg"+"\n")


	
