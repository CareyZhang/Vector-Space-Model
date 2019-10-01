import json
import math

def get_idf(doc_dataset,target,doc_cnt):
	cnt = 0
	for docs in doc_dataset:
		if target in doc_dataset[docs].keys():
			cnt += 1
	return math.log(1+(doc_cnt/(1+cnt)),10)
	
def get_sim(query_tf_idf,doc_tf_idf):
	return 0

query_list = [query.strip('\n') for query in open("query_list.txt","r")]
doc_list = [doc.strip('\n') for doc in open("doc_list.txt","r")]

query_dataset = {}
query_dataset_tf = {}
doc_dataset = {}
doc_dataset_tf = {}

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
			
	for word in doc_dataset[doc]:
		doc_dataset_tf[doc].update({word:doc_dataset[doc][word]/word_cnt})

doc_cnt = len(doc_dataset.keys())
idf = {}

for queries in query_list:
	for words in query_dataset[queries].keys():
		if words not in idf:
			idf.update({words:get_idf(doc_dataset,words,doc_cnt)})

f = open("submission.txt", "w")
f.write("Query,RetrievedDocuments\n")
for queries in query_list:
	f.write(queries+",")
	query_tf_idf = {}
	doc_tf_idf = {}
	sim = {}
	for words in query_dataset[queries].keys():
		query_tf_idf.update({words:query_dataset_tf[queries][words] * idf[words]})

	for docs in doc_list:
		doc_tf_idf.update({docs:{}})
		for words in doc_dataset[docs]:
			if words in idf:
				doc_tf_idf[docs].update({words:doc_dataset_tf[docs][words] * idf[words]})
			else:
				doc_tf_idf[docs].update({words:doc_dataset_tf[docs][words] * math.log(doc_cnt,10)})

	for docs in doc_list:
		s1 = 0
		s2 = 0
		s3 = 0
		for words, q_tf_idf in query_tf_idf.items():
			if words not in doc_tf_idf[docs]:
				continue
			else:
				s1 += q_tf_idf * doc_tf_idf[docs][words]
				s2 += math.pow(q_tf_idf,2)
				s3 += math.pow(doc_tf_idf[docs][words],2)
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
	f.write("\n")

f.close()