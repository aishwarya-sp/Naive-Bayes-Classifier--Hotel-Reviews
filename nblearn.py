import string
import math
import sys


#stopwords = open("stopwords.txt",'r').readlines()
f = open(sys.argv[1],"r").readlines()

output = open("nbmodel.txt","w")
output1 = open("wordset.txt",'w')

output2 = open("nbmodel1.txt","w")



word_prob_dict = dict()
true_prob_dict = dict()
global_set = set()
word_freq = dict()
stop_words =set()

stopwords = {"a","about","above","after","again","all","am","an","and","any","are","as","at","be","because","been","i",
"me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself",
"it","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were",
"be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at",
"by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over",
"under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same",
"so","than","too","very","s","t","can","will","just","don","should","now","before","being","below","between","both","but","by","cannot","could","did","do","does",
"doing","down","during","each","few","for","from","further","had","has","have","having","he","he'd","he'll","he's","her","here","here's","hers",
"herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","it","it's","its","itself","let's","me","more","most","my","myself","no",
"nor","not","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","she","she'd","she'll","she's","should","so","some",
"such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too",
"under","until","up","very","was","we","we'd","we'll","we're","we've","were","what","what's","when","when's","where","where's","which","while","who","who's","whom","why",
"why's","with","would","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"}


for sw in stopwords:
	#sw = sw.strip()
	#print sw
	sw = sw.translate(None, string.punctuation)
	stop_words.add(sw)

# print stop_words

#print stop_words


total_pos_tags = 0
total_neg_tags = 0

total_pos_words =0
total_neg_words = 0

total_true_tags = 0
total_fake_tags = 0

total_true_words =0
total_fake_words = 0

for document in f:
	values = document.strip().split(' ')
	for i in range(3,len(values)):
		values[i] = values[i].translate(None, string.punctuation)
		values[i] = values[i].lower()
		if values[i] in word_freq:
			word_freq[values[i]] += 1
		else:
			word_freq[values[i]] = 1





sorted_words = sorted(word_freq,key=word_freq.get,reverse = True)


for i in range(20):
	if sorted_words[i] not in stop_words:
		stop_words.add(sorted_words[i])


for document in f:

	#temp_set.clear()

	values = document.strip().split(' ')
	pos_or_neg = values[2]
	true_or_fake = values[1]
	
	if pos_or_neg == "Pos":
		total_pos_tags += 1
	elif pos_or_neg == "Neg":
		total_neg_tags += 1

	if true_or_fake == "True":
		total_true_tags += 1
	elif true_or_fake == "Fake":
		total_fake_tags += 1

	for i in range(3,len(values)): 

		values[i] = values[i].translate(None, string.punctuation)
		values[i] = values[i].lower()

		if values[i] not in stop_words:
		
			if (values[i],pos_or_neg) in word_prob_dict:
				word_prob_dict[(values[i],pos_or_neg)] += 1
			else:
				word_prob_dict[(values[i],pos_or_neg)] = 1

			if (values[i],true_or_fake) in true_prob_dict:
				true_prob_dict[(values[i],true_or_fake)] += 1
			else:
				true_prob_dict[(values[i],true_or_fake)] = 1


			global_set.add(values[i])
			#temp_set.add(values[i])
			
			if pos_or_neg == "Pos":
				total_pos_words += 1
			elif pos_or_neg == "Neg":
				total_neg_words += 1

			if true_or_fake == "True":
				total_true_words += 1
			elif true_or_fake == "Fake":
				total_fake_words += 1




pos_prior = math.log(total_pos_tags/((total_pos_tags+total_neg_tags)*1.0))
neg_prior = math.log(total_neg_tags/((total_pos_tags+total_neg_tags)*1.0))
true_prior = math.log(total_true_tags/((total_true_tags+total_fake_tags)*1.0))
fake_prior = math.log(total_fake_tags/((total_true_tags+total_fake_tags)*1.0))

#print pos_prior,neg_prior,true_prior,fake_prior


word_prob_dict_final = dict()


for key in word_prob_dict:
	if key[1] == "Pos":
		word_prob_dict_final[key] = math.log((1+word_prob_dict[key])/((len(global_set) + total_pos_words)*1.0))

		if (key[0],"Neg") not in word_prob_dict:
			word_prob_dict_final[(key[0],"Neg")] = math.log(1/((len(global_set) + total_neg_words)*1.0))

	elif key[1] == "Neg":
		word_prob_dict_final[key] = math.log((1+word_prob_dict[key])/((len(global_set) + total_neg_words)*1.0))
		if (key[0],"Pos") not in word_prob_dict:
			word_prob_dict_final[(key[0],"Pos")] = math.log(1/((len(global_set) + total_pos_words)*1.0))


word_prob_dict.update(word_prob_dict_final)


#print word_prob_dict
# for key in true_prob_dict:
# 	print key,true_prob_dict[key]

true_prob_dict_final = dict()


#print total_true_words,total_fake_words,len(global_set)

for key1 in true_prob_dict:
	if key1[1] == "True":
		true_prob_dict_final[key1] = math.log((1+true_prob_dict[key1])/((len(global_set) + total_true_words)*1.0))
		#print key1,true_prob_dict_final[key1]

		if (key1[0],"Fake") not in true_prob_dict:
			true_prob_dict_final[(key1[0],"Fake")] = math.log(1/((len(global_set) + total_fake_words)*1.0))

	elif key1[1] == "Fake":
		true_prob_dict_final[key1] = math.log((1+true_prob_dict[key1])/((len(global_set) + total_fake_words)*1.0))
		if (key1[0],"True") not in true_prob_dict:
			true_prob_dict_final[(key1[0],"True")] = math.log(1/((len(global_set) + total_fake_words)*1.0))




true_prob_dict.update(true_prob_dict_final)

#print true_prob_dict


output.write(str(pos_prior)+"\n"+str(neg_prior)+"\n")
for key in word_prob_dict:
	output.write(str(key[0]) +"/" +str(key[1]) + "," + str(word_prob_dict[key])+"\n")



output2.write(str(true_prior)+"\n"+str(fake_prior)+"\n")
for key1 in true_prob_dict:
	output2.write(str(key1[0]) +"/" +str(key1[1]) + "," + str(true_prob_dict[key1])+"\n")

for word in global_set:
		if word == '':
			pass
		else:
			output1.write(word+"\n")




