import swiftclient
import keystoneclient
import os
import re 

import gnupg

container_name = 'Files'
container_name1 = 'Files1 '

projectId = '1531d2c4c0104376b352f37685d982a4'region = 'dallas'userId = 'd80318b5852c474abcb8c1700ac80806'username = 'admin_d843b44bc4a026b0e594292cc874d5ceb5ca83b1'password = 'M4/pAA~NM.Sm&4F}'



con = swiftclient.Connection(key=password,authurl='https://identity.open.softlayer.com/v3',auth_version='3',
os_options={"project_id": projectId,"user_id": userId,"region_name": region})




gpg = gnupg.GPG()
input_data=gpg.gen_key_input(key_type="RSA", key_length=1024, passphrase='abcd')
key=gpg.gen_key(input_data)
con.put_container(container_name)
con.put_container(container_name1)
print "\nContainer named %s created successfully." % container_name
print "\nContainer named %s created successfully." % container_name1




print "1.upload"
print "2.download"
print "3.list"

choice = int(raw_input("enter choice:"))

if choice == 1: 
	rootDir= raw_input("enter the folder name from which you want to upload the .txt,.pdf files into blue mix")

	#filter = ['txt','pdf']
	for dirName, subdirList, fileList in os.walk(rootDir):
    		for fname in fileList:
    			if fname[-3:] == 'txt':
        			location = (dirName+ "/" + fname)
				
				with open(location, 'rb') as f:
    					status = gpg.encrypt_file(f,recipients=None, 						symmetric="AES256",passphrase='abcd', 							armor=False,output='my-encrypted.txt.gpg')

					print 'ok: ', status.ok
					print 'status: ', status.status
					print 'stderr: ', status.stderr
					file = 'my-encrypted.txt.gpg'
        				print "uploaded from"+location		
        				with open(file, 'r') as example_file:
						con.put_object(container_name,fname,contents=example_file.read())
 						example_file.close()
			elif fname[-3:] == 'pdf':
				location = (dirName+ "/" + fname)
				
				with open(location, 'rb') as f:
    					status = gpg.encrypt_file(f,recipients=None, 						symmetric="AES256",passphrase='abcd', 							armor=False,output='my-encrypted.txt.gpg')

					print 'ok: ', status.ok
					print 'status: ', status.status
					print 'stderr: ', status.stderr
					file = 'my-encrypted.txt.gpg'
        				print "uploaded from"+location		
        				with open(file, 'r') as example_file:
						con.put_object(container_name1,fname,contents=example_file.read())
 						example_file.close()


elif choice == 2:
	Integer = random.randint(0,9)
	
	file_name = raw_input("enter file you want to download with extension:")
	obj = con.get_object(container_name, file_name)
	with open(file_name, 'w') as integer:
		integer.write(obj[1])
	print "\nObject %s downloaded successfully." % file_name
	with open(file_name, 'rb') as f:
		 status = gpg.decrypt_file(f, passphrase='abcd', output='decrypted.txt')
		

elif choice == 3:
	# List your containers
	print ("\nContainer List:")
	for container in con.get_account()[1]:
		for data in con.get_container(container['name'])[1]:
			size = data['bytes']
			print 'File: {0}\t size: {1}\t date: {2}'.format(data['name'], data['bytes'], data['last_modified'])
			if size > 1000:
				con.delete_object(container['name'],data['name'])

else:
	print "You have entered wrong choice. Try again."
	






