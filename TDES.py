# -*- coding: utf-8 -*-
"""
@author: Shreya

@versions:
    Python 3.8.8
    Pycryptodome 3.10.4
    Spyder 4.2.5
    Spyder terminal 1.10.2

"""

#Password hashing Iterations - KEEP CONSTANT through out this application existence.
pi=100006

salt_const="$2a$10$B0czYdLVHJG4x0HnEuVX2eF7T9m1UZKynw.gRCrq8S98z84msdxdi"

#importing libraries
from crypto.Cipher import DES
from crypto.Hash import SHA256
from getpass import getpass
from crypto.Protocol.KDF import PBKDF2

#encrypting function
def encryptor(path):
	#opening the image file
	try:
		with open(path, 'rb') as input_file:
			file=input_file.read()
			
		#padding	
		while len(file)%8!=0:
			file+=b" "
	except:
		print("Error loading the file. Make sure file is in same directory, spelled correctly and non-corrupted.")
		exit()
	
	#hashing original image in SHA256	
	hash_of_original=SHA256.new(data=file)
	
	
	
	#Inputting Keys
	key_enc=getpass(prompt="Enter minimum 8 character long password:\n")
	#Checking if key is of invalid length
	while len(key_enc)<8:
		key_enc=getpass(prompt="Invalid password! Enter atleast 8 character password:\n")
	
	key_enc_confirm=getpass(prompt="Enter password again:\n")
	while key_enc!=key_enc_confirm:
		print("\nKey not matched! Try again.")
		key_enc=getpass(prompt="Enter 8 character long password:\n")
	
		#Checking if key is of invalid length
		while len(key_enc)<8:
			key_enc=getpass(prompt="Invalid password! Enter atleast 8 character password:\n")
		key_enc_confirm=getpass(prompt="Enter password again:\n")
	
	
	#Salting and hashing password
	key_enc=PBKDF2(key_enc,salt_const,48,count=pi)

	
	#Encrypting using triple 3 key DES	
	print("\nencrypting...")	
	try:
		
		cipher1=DES.new(key_enc[0:8],DES.MODE_CBC,key_enc[24:32])
		ciphertext1=cipher1.encrypt(file)
		cipher2=DES.new(key_enc[8:16],DES.MODE_CBC,key_enc[32:40])
		ciphertext2=cipher2.decrypt(ciphertext1)
		cipher3=DES.new(key_enc[16:24],DES.MODE_CBC,key_enc[40:48])
		ciphertext3=cipher3.encrypt(ciphertext2)
		print("ENCRYPTION SUCCESSFUL!")
	except:
		print("Encryption failed. Possible causes:\n1.Library not installed properly\n2.low device memory\n3.Incorrect padding or conversions")
		exit()
	
	#Adding hash at end of encrypted bytes
	ciphertext3+=hash_of_original.digest()

	
	#Saving the file encrypted
	try:
		dpath="encrypted_"+path
		with open(dpath, 'wb') as image_file:
    			image_file.write(ciphertext3)
		print("Encrypted Image saved successfully as filename "+dpath)
    		
		
	except:
		temp_path=input("Saving file failed! Enter alternate name without format to save the encrypted file. If it is still failing then check system memory.")
		try:
			dpath=temp_path+path
			dpath="encrypted_"+path
			with open(dpath, 'wb') as image_file:
    				image_file.write(ciphertext3)
			print("Encrypted Image saved successfully as filename "+dpath)
			exit()
		except:
			print("Failed! Exiting...")
			exit()

#decrypting function
def decryptor(encrypted_image_path):
	
	try:
		with open(encrypted_image_path,'rb') as encrypted_file:
			encrypted_data_with_hash=encrypted_file.read()
			
	except:
		print("Unable to read source cipher data. Make sure the file is in same directory. Exiting...")
		exit()
	
	
	#Inputting the key
	key_dec=getpass(prompt="Enter password:\n")
	
	
	#extracting hash and cipher data without hash
	extracted_hash=encrypted_data_with_hash[-32:]
	encrypted_data=encrypted_data_with_hash[:-32]

	
	#salting and hashing password
	key_dec=PBKDF2(key_dec,salt_const,48,count=pi)
	

	#decrypting using triple 3 key DES
	print("\nDecrypting...")
	try:
		
		cipher1=DES.new(key_dec[16:24],DES.MODE_CBC,key_dec[40:48])
		plaintext1=cipher1.decrypt(encrypted_data)
		cipher2=DES.new(key_dec[8:16],DES.MODE_CBC,key_dec[32:40])
		plaintext2=cipher2.encrypt(plaintext1)
		cipher3=DES.new(key_dec[0:8],DES.MODE_CBC,key_dec[24:32])
		plaintext3=cipher3.decrypt(plaintext2)
		
		
	except:
		print("Decryption failed. Possible causes:\n1.Library not installed properly\n2.low device memory\n3.Incorrect padding or conversions")

	#hashing decrypted plain text
	hash_of_decrypted=SHA256.new(data=plaintext3)

	
	#matching hashes
	if hash_of_decrypted.digest()==extracted_hash:
		print("Password matched!")
		print("DECRYPTION SUCCESSFUL!")
	else:
		print("Incorrect Password!")
		exit()
		
        #saving the decrypted file	
	try:
		epath=encrypted_image_path
		if epath[:10]=="encrypted_":
			epath=epath[10:]
		epath="decrypted_"+epath
		with open(epath, 'wb') as image_file:
			image_file.write(plaintext3)
		print("Image saved successully with name " + epath)
		print("Note: If the decrypted image is appearing to be corrupted then password may be wrong or it may be file format error.")
	except:
		temp_path=input("Saving file failed! Enter alternate name without format to save the decrypted file. If it is still failing then check system memory.")
		try:
			epath=temp_path+encrypted_image_path
			with open(epath, 'wb') as image_file:
				image_file.write(plaintext3)
			print("Image saved successully with name " + epath)
			print("Note: If the decrypted image is appearing to be corrupted then password may be wrong or it may be file format error.)")
		except:
			print("Failed! Exiting...")
			exit()


try:
	choice=int(input("Choose one of the following operations:\n\n\t1. Encrypt\n\t2. Decrypt\n\nYour choice: "))
	while choice!=1 and choice!=2:
		choice=int(input("Invalid Choice! Try Again:\n"))
except:
	print("Error, please provide valid Input")
	exit()



if choice==1:
#Encryption Mode, function call
	path=input("Enter file name to encypt:\n")
	encryptor(path)
		


else:
#Decryption mode, function call
	encrypted_image_path=input("Enter file name to decrypt:\n")
	decryptor(encrypted_image_path)
