import json
import math

def get_idf(doc_dataset,target,doc_cnt):
	cnt = 0
	for docs in doc_dataset:
		if target in doc_dataset[docs].keys():
			cnt += 1
	return cnt
	
query_list = [query.strip('\n') for query in open("query_list.txt","r")]
doc_list = [doc.strip('\n') for doc in open("doc_list.txt","r")]

dictionary = {}
query_dataset = {}
query_dataset_tf = {}
doc_dataset = {}
doc_dataset_tf = {}
cnt = 0

for query in query_list:
	query_dataset.update({query:{}})
	query_dataset_tf.update({query:{}})
	word_cnt = 0
	for line in open("Query/"+query,"r"):
		line = line.split()[0:-1]
		for word in line:
			if word in query_dataset[query]:
				query_dataset[query].update({word:query_dataset[query][word]+1})
			else:
				query_dataset[query].update({word:1})
			word_cnt += 1
			cnt += 1
			
			if word not in dictionary:
				dictionary.update({word:cnt})
			
	for word in query_dataset[query]:
		query_dataset_tf[query].update({word:query_dataset[query][word]/word_cnt})
				
for doc in doc_list:
	doc_dataset.update({doc:{}})
	doc_dataset_tf.update({doc:{}})
	f = open("Document/"+doc,"r").readlines()[3:]
	word_cnt = 0
	for line in f:
		line = line.split()[0:-1]
		for word in line:
			if word in doc_dataset[doc]:
				doc_dataset[doc].update({word:doc_dataset[doc][word]+1})
			else:
				doc_dataset[doc].update({word:1})
			word_cnt += 1
			
			
			if word not in dictionary:
				dictionary.update({word:cnt})
			
	for word in doc_dataset[doc]:
		doc_dataset_tf[doc].update({word:doc_dataset[doc][word]/word_cnt})

doc_cnt = len(doc_dataset.keys())
idf = {}

for queries in query_list:
	for words in query_dataset[queries].keys():
		if words not in idf:
			a = get_idf(doc_dataset,words,doc_cnt)
			if a != 0:
				idf.update({words:a})

for word in dictionary.keys():
	for doc in doc_list:
		if word not in doc_dataset_tf[doc]:
			doc_dataset_tf[doc].update({word:0})
			
	for query in query_list:
		if query not in query_dataset_tf[query]:
			query_dataset_tf[query].update({word:0})
f = open("submission.txt", "w")
f.write("Query,RetrievedDocuments\r\n")

for queries in query_list:
	f.write(queries+",")
	query_weight = {}
	doc_weight = {}
	sim = {}
	for words in dictionary.keys():
		if words in idf:
			query_weight.update({words:query_dataset_tf[queries][words] * math.log(doc_cnt/idf[words],10)})
		else:
			query_weight.update({words:0})

	for docs in doc_list:
		doc_weight.update({docs:{}})
		for words in dictionary.keys():
			if words in idf:
				doc_weight[docs].update({words:doc_dataset_tf[docs][words] * math.log(doc_cnt/idf[words],10)})
			else:
				doc_weight[docs].update({words:0})
				
	for docs in doc_list:
		s1 = 0
		s2 = 0
		s3 = 0
		for words, q_weight in query_weight.items():
			if words not in doc_weight[docs]:
				continue
			else:
				s1 += q_weight * doc_weight[docs][words]
				s2 += math.pow(q_weight,2)
				s3 += math.pow(doc_weight[docs][words],2)
		s2 = math.pow(s2,(1/2))
		s3 = math.pow(s3,(1/2))
		s4 = s2 * s3
		if s4!=0:
			sim.update({docs:s1/s4})
		else:
			sim.update({docs:0})
	sim = sorted(sim.items(), key=lambda sim: sim[1],reverse=True)
	for item in sim:
		f.write(item[0] + " ")
	f.write("\r\n")

f.close()