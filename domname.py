from sys import argv
import socket

output=[]

for n in range(1,4):
	domain_name = argv[n]
	ip = socket.gethostbyname(domain_name)
	output.insert(n,ip)

for x in output:
        print("__"+x+"__")


for i in range(0,5):
	for n in range(1,4):
		domain_name = argv[n]
		ip = socket.gethostbyname(domain_name)
		print(domain_name+" "+ip)
		test = output[n]
		if test != ip:
			print("[ERROR] "+domain_name+" IP mismatch: "+output[n]+" "+ip)
			break
		output.insert(n,ip)
