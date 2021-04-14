from sys import argv
import sys,socket,json,yaml

output=[]
domain_name=argv
y = len(domain_name)
data=[]

for n in range(1,y): #забиваем массив айпишниками
	a = domain_name[n]
	ip = socket.gethostbyname(a)
	output.insert(n,ip)

for x in output:
	print(" __ "+x+"__")

def json_import(domain_name,output):
	for k in range(0,y-1): #пишем набор из адресов и айпишников в json
		q ='{ "'+domain_name[k+1]+'" : "'+output[k]+'"}'
		#print(q)
		data.insert(k,q)
	with open("ipnames.json","w") as write_file:
		json.dump(data, write_file)
	write_file.close()
	del data[:]

def yaml_import(domain_name,output):
	for k in range(0,y-1): #пишем набор из адресов и айпишников в yaml
		q = domain_name[k+1]+" : "+output[k]
		#print(q)
		data.insert(k,q)
	with open("ipnames.yml", "w") as write_file:
		json.dump(data, write_file)
	write_file.close()
	del data[:]


while y>1:
	for n in range(1,y):
		ip = socket.gethostbyname(domain_name[n])
		print(domain_name[n]+" "+ip)
		test = output[n-1]
		if test != ip:
			print("[ERROR] "+domain_name[n]+" IP mismatch: "+output[n]+" "+ip)
			json_import(domain_name,output)
			yaml_import(domain_name,output)
			break
		output.insert(n,ip)
