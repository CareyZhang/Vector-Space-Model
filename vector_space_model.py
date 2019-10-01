import json
import math

Query = [query.strip('\n') for query in open("query_list.txt","r")]
Doc = [doc.strip('\n') for doc in open("doc_list.txt","r")]

QueryList_index = enumerate(Query)
DocList_index = enumerate(Doc)

query_cnt = len(Query)
doc_cnt = len(Doc)

Dictionary = {}
DF = {}
TF = {}
QTF = {}

for doc in Doc:
	for line in open("Document/"+doc,"r").readlines()[3:]:
		line = line.split()[0:-1]
		for word in line:
			if word not in Dictionary:
				Dictionary.update({word:0})

for query in Query:
	for line in open("Query/"+query,"r"):
		line = line.split()[0:-1]
		for word in line:
			if word not in Dictionary:
				Dictionary.update({word:0})

for doc in Doc:
	TF.update({doc:Dictionary.copy()})
	for line in open("Document/"+doc,"r").readlines()[3:]:
		line = line.split()[0:-1]
		for word in line:
			TF[doc].update({word:TF[doc][word] + 1})

for query in Query:
	QTF.update({query:Dictionary.copy()})
	for line in open("Query/"+query,"r"):
		line = line.split()[0:-1]
		for word in line:
			QTF[query].update({word:QTF[query][word] + 1})

for word in Dictionary.keys():
	df_cnt = 0
	for doc in Doc:
		if TF[doc][word] > 0:
			df_cnt += 1
	DF.update({word:df_cnt})

f = open("submission.txt", "w")
f.write("Query,RetrievedDocuments\r\n")

for query in Query:
	f.write(query+",")
	QueryWeight = {}
	DocWeight = {}
	SIM = {}
	for word in Dictionary.keys():
		if DF[word] == 0:
			QueryWeight.update({word:QTF[query][word] * math.log(doc_cnt)})
		else:
			QueryWeight.update({word:QTF[query][word] * math.log(doc_cnt/DF[word])})
			
	for doc in Doc:
		DocWeight.update({doc:{}})
		for word in Dictionary.keys():
			if DF[word] == 0:
				DocWeight[doc].update({word:TF[doc][word] * math.log(doc_cnt)})
			else:
				DocWeight[doc].update({word:TF[doc][word] * math.log(doc_cnt/DF[word])})
				
	for doc in Doc:
		s1 = 0
		s2 = 0
		s3 = 0
		for word, q_weight in QueryWeight.items():
			s1 += q_weight * DocWeight[doc][word]
			s2 += math.pow(q_weight,2)
			s3 += math.pow(DocWeight[doc][word],2)
		s2 = math.pow(s2,(1/2))
		s3 = math.pow(s3,(1/2))
		s4 = s2 * s3
		SIM.update({doc:s1/s4})
		
	SIM_SORT = sorted(SIM.items(), key=lambda SIM: SIM[1],reverse=True)
	
	for item in SIM_SORT:
		f.write(item[0] + " ")
	f.write("\r\n")

f.close()
			