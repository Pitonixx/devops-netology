from sys import argv
import sys,socket

output=[]
domain_name=argv
y = len(domain_name)

for n in range(1,y):
	a = domain_name[n]
	ip = socket.gethostbyname(a)
	output.insert(n,ip)

for x in output:
        print(" __ "+x+"__")


while y > 1:
	for n in range(1,y):
		ip = socket.gethostbyname(domain_name[n])
		print(domain_name[n]+" "+ip)
		test = output[n-1]
		if test != ip:
			print("[ERROR] "+domain_name[n]+" IP mismatch: "+output[n]+" "+ip)
		output.insert(n,ip)
