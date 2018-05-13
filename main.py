import nltk
import copy
# nltk.download()
# print nltk.help.upenn_tagset()
sentence = raw_input('Enter a sentence: ')
# sentence = "The very small biy kissed the platypus"
sentence = sentence.split()

dict_pos = {"NN":"N", "DT":"D", "RB":"Adv", "VBD":"V","VBP":"V", "JJ":"Adj", "NNP" : "N", "VBZ":"V", "VB":"V",  "PRP": "N", "IN": "P", "TO": "P"}
sentence_pos = nltk.pos_tag(sentence)
print sentence_pos
stage_array = []
for words in sentence_pos:
	stage_array.append(words[0])
	# print words[0] + "\t",
# print
print_array = []
print_array.append((stage_array))

stage_array = []
p=0
for words in sentence_pos:
	if p==0 and dict_pos[words[1]] == "IN":
		stage_array.append("C")
	else:
		stage_array.append(dict_pos[words[1]])
	p=1
	# print  dict_pos[words[1]] + "\t",	
# print_array
print_array.append((stage_array))
# ===============

left = "<="
right = "=>"
while len(stage_array) - stage_array.count(" ")- stage_array.count(left)- stage_array.count(right)  > 1:
	stage_array = []
	current_stage = []
	positional = []
	for words in range(len(print_array[-1])):
		if print_array[-1][words] != "|" and print_array[-1][words] != right and print_array[-1][words] != left and print_array[-1][words] != " ":
			current_stage.append(print_array[-1][words])
			positional.append(1)
		else:
			for x in xrange(1,10):
				if print_array[-x][words] != "|" and print_array[-1][words] != left and print_array[-1][words] != right and print_array[-1][words] != " ":
					current_stage.append(print_array[-x][words])
					positional.append(1)
					break
				elif print_array[-x][words] == "|":
					pass
				else:
					positional.append(0)
					break
	# print current_stage
	words = 0
	while words < len(current_stage):
		### RULE A
		if current_stage[words] == "C":
			if words < len(current_stage):
				if current_stage[words + 1] == "TP":
					stage_array.append("CP")
					stage_array.append(left)
		### RULE B
		elif current_stage[words] == "VP":
			i=0
			while i < len(current_stage):
				i+=1
				listss = ["NP","CP","T","VP"]
				if current_stage[i-1] in listss:
					continue
				else:
					break
			if i != len(current_stage):
				stage_array.append("|")	
			else:	
				if words > 0:
					if current_stage[words-1] == "NP" or current_stage[words-1] == "CP" or current_stage[words-1] == "T":
						stage_array[words-1] = (right)
					if current_stage[words-1] == "T" and (current_stage[words-2] == "NP" or current_stage[words-2] == "CP"):
						stage_array[words-2] = (right)
				stage_array.append("TP")
		### RULE C
		elif current_stage[words] == "V": 
			i=0
			while i < len(current_stage):
				i+=1
				if current_stage[i-1] == "V" or current_stage[i-1] == "conj" or current_stage[i-1][-1] == "P":
					if current_stage[i-1] == "P":
						break
					continue
				else:
					break
				
			if i != len(current_stage):
				stage_array.append("|")	
			else:				
				i = 1
				while words - i >= 0:
					if current_stage[words-i] == "AdvP":
						stage_array[words-i] = (right)
						continue
					else:
						break
					i+=1				
				i = 1
				stage_array.append("VP")
				if words + i < len(current_stage):
					if current_stage[words+i] == "NP":
						stage_array.append(left)
						i+=1
						if words + 2 < len(current_stage):
							if current_stage[words+i] == "NP" or current_stage[words+i] == "CP":
								stage_array.append(left)
								i+=1
					elif current_stage[words+i] == "CP":
						stage_array.append(left)
						i+=1			
				while words + i < len(current_stage):
					if current_stage[words+i] == "AdvP":
						stage_array.append(left)
					else:
						break
					i+=1	
				while words + i < len(current_stage):
					if current_stage[words+i] == "PP":
						stage_array.append(left)
					else:
						break
					i+=1
				while words + i < len(current_stage):
					if current_stage[words+i] == "AdvP":
						stage_array.append(left)
					else:
						break
					i+=1													
		### RULE D
		elif current_stage[words] == "N": 
			change = 1
			i = 1
			while words - i >= 0:
				if current_stage[words-i] == "Adj":
					change = 0
					break
				elif current_stage[words-i] == "D":
					stage_array[words-i]=(right)
					break
				elif current_stage[words-i] == "AdjP":
					stage_array[words-i]=(right)
				else:
					break
				i+=1
			i = 1
			if change == 1:
				stage_array.append("NP")
				while words + i < len(current_stage) -1 and (current_stage[words + i] == "PP" or current_stage[words + i] == "CP"):
					stage_array.append(left)
					if current_stage[words + i] == "CP":
						break
					i+=1	
			else:
				stage_array.append("|")	
		### RULE E
		elif current_stage[words] == "P":
			i=1
			if words + i < len(current_stage):
				if current_stage[words+1] == "N":
					stage_array.append("|")
				else:
					if current_stage[words+1] == "NP":
						stage_array.append("PP")
						stage_array.append(left)
							
			else:
				stage_array.append("PP")					
		### RULE F
		elif current_stage[words] == "Adj":
			if words > 0:
				if current_stage[words-1] == "Adv":
					stage_array.append("|")
				else:
					if current_stage[words-1] == "AdvP":
						stage_array[words-1]=(right)
					stage_array.append("AdjP")
		### RULE G
		elif current_stage[words] == "Adv":
			if words > 0:
				if current_stage[words-1] == "Adj":
					stage_array.append("|")
				else:
					if current_stage[words-1] == "AdjP":
						stage_array[words-1]=(right)
					stage_array.append("AdvP")					
		elif current_stage[words] == right or current_stage[words] == left or current_stage[words] == " ":
			stage_array.append(" ")
		else:
			stage_array.append("|")
		words = len(stage_array)


	new_array = []
	k = 0

	for item in positional:
		if item == 0:
			new_array.append(" ")
		else:
			new_array.append(stage_array[k])
			k+=1
	print_array.append((new_array))




# ===============
for x in xrange(1,len(print_array)+1):
	for y in print_array[len(print_array)-x]:
		print y + "\t",
	print
