from subprocess import call

import sys
import os
import json

orden = sys.argv[1]
prp = False

#--- ORDEN PREPARE ---#

if orden == "prepare" :
	prp = True
# Obtención del numero de servidores 
	if len(sys.argv) == 3 :
		entrada = sys.argv[2]
		if int(entrada) > 5 or int(entrada) < 1 :
			print("ERROR: El número de servidores debe ser de entre 1 y 5")
		#sys.exit()
	else:
		entrada = "3"

# Creación del fichero de configuración

	try :
		fh = open("auto-p2.json", "w")
		fh.write("{ \n 'num_serv': \n" + entrada + "\n }")
		fh.close()
		fh1 = open("auto-p2.json", "a")
		fh1.write("\n launch = 0")
		fh1.write("\n launch c1 = 0")
		fh1.write("\n launch lb = 0")
		for x in range(1,int(entrada)+1) :
			fh1.write("\n launch s"+str(x)+" = 0")
		fh1.close()
	except:
		print("Error en la creación de fichero de configuración")
	
	def prepare() :
		# Creación de las imágenes
		try :
			os.system("qemu-img create -f qcow2 -b cdps-vm-base-pc1.qcow2 c1.qcow2")
		except:
			print("Error en c1")

		try :
			os.system("qemu-img create -f qcow2 -b cdps-vm-base-pc1.qcow2 lb.qcow2")
		except:
			print("Error en lb")

		for x in range(1,int(entrada)+1) : 
			try :
				os.system("qemu-img create -f qcow2 -b cdps-vm-base-pc1.qcow2 s"+str(x)+".qcow2")
			except:
				print("Error en s"+str(x))

		# Creación de los xml
		try :
			os.system("cp plantilla-vm-pc1.xml c1.xml")
		except:
			print("Error en xml de c1")

		try :
			os.system("cp plantilla-vm-pc1.xml lb.xml")
		except:
			print("Error en xml de lb")

		for x in range(1,int(entrada)+1) :
			try :
				os.system("cp plantilla-vm-pc1.xml s"+str(x)+".xml")
			except:
				print("Error en xml de s"+str(x))

		# Edición de los xml

		try :
			fhin = open("c1.xml", "r")
			fhout = open("c1pp", "w")

			for line in fhin :
				if "<name>XXX</name>" in line :
					fhout.write("<name>c1</name>\n")
				elif "<source file='/mnt/tmp/XXX/XXX.qcow2'/>" in line :
					fhout.write("<source file='/mnt/tmp/pc1/c1.qcow2'/>\n")
				elif "<source bridge='XXX'/>" in line :
					fhout.write("<source bridge='LAN1'/>\n")
				else :
					fhout.write(line)
			fhin.close()
			fhout.close()
		except:
			print("Error en edición xml de c1")

		try :
			fhin2 = open("c1pp", "r")
			fhout2 = open("c1.xml", "w")
			for line in fhin2 :
				fhout2.write(line)

			fhin2.close()
			fhout2.close()

		except :
			print ("Error en la copia xml de c1")

		try :
			fhin3 = open("lb.xml", "r")
			fhout3 = open("c1pp", "w")

			for line in fhin3 :
				if "<name>XXX</name>" in line :
					fhout3.write("<name>lb</name>\n")
				elif "<source file='/mnt/tmp/XXX/XXX.qcow2'/>"  in line :
					fhout3.write("<source file='/mnt/tmp/pc1/lb.qcow2'/>\n")
				elif "<source bridge='XXX'/>" in line :
					fhout3.write("<source bridge='LAN1'/>\n")
				elif "<model type='virtio'/>" in line :
					fhout3.write("")
				elif "</interface>" in line :
					fhout3.write("")
				elif "<serial type='pty'>" in line :
					fhout3.write("")
				elif "<target port='0'/>" in line :
					fhout3.write("")
				elif "</serial>" in line :
					fhout3.write("")
				elif "<console type='pty'>" in line :
					fhout3.write("")
				elif "<target type='serial' port='0'/>" in line :
					fhout3.write("")
				elif "</console>" in line :
					fhout3.write("")
				elif "<input type='mouse' bus='ps2'/>" in line :
					fhout3.write("")
				elif "<graphics type='vnc' port='-1' autoport='yes'/>" in line :
					fhout3.write("")
				elif "</devices>" in line:
					fhout3.write("")
				elif "</domain>" in line:
					fhout3.write("")
				else :
					fhout3.write(line)

			fhin3.close()
			fhout3.close()
		except:
			print("Error en edición xml de lb")

		fhaux = open("c1pp", "a")
		fhaux.write("<model type='virtio'/>\n")
		fhaux.write("</interface>\n")
		fhaux.write("<interface type='bridge'>\n")
		fhaux.write("<source bridge='LAN2'/>\n")
		fhaux.write('<model type="virtio"/>\n')
		fhaux.write("</interface>\n")
		fhaux.write("<serial type='pty'>\n")
		fhaux.write("<target port='0'/>\n")
		fhaux.write("</serial>\n")
		fhaux.write("<console type='pty'>\n")
		fhaux.write("<target type='serial' port='0'/>\n")
		fhaux.write("</console>\n")
		fhaux.write("<input type='mouse' bus='ps2'/>\n")
		fhaux.write("<graphics type='vnc' port='-1' autoport='yes'/>\n")
		fhaux.write(" </devices>\n")
		fhaux.write("</domain>\n")
		fhaux.close()

		fhin4 = open("c1pp", "r")
		fhout4 = open("lb.xml", "w")
		for line in fhin4:
			fhout4.write(line)
		fhin4.close()
		fhout4.close()

		for x in range(1,int(entrada)+1) :

			fhin = open("s"+str(x)+".xml", "r")
			fhout = open("c1pp", "w")

			for line in fhin :
				if "<name>XXX</name>" in line :
					fhout.write("<name>s"+str(x)+"</name>\n")
				elif "<source file='/mnt/tmp/XXX/XXX.qcow2'/>" in line :
					fhout.write("<source file='/mnt/tmp/pc1/s"+str(x)+".qcow2'/>\n")
				elif "<source bridge='XXX'/>" in line :
					fhout.write("<source bridge='LAN2'/>\n")
				else :
					fhout.write(line)
			fhin.close()
			fhout.close()
			fhin2 = open("c1pp", "r")
			fhout2 = open("s"+str(x)+".xml", "w")
			for line in fhin2 :
				fhout2.write(line) 
			fhin2.close()
			fhout2.close()

		try :
			os.system("rm c1pp")
		except:
			print("Error al borrar c1pp")


	prepare()

# Creación de los bridges
	try :
		os.system("sudo brctl addbr LAN1")
	except:
		print("Error bridges LAN1")

	try :
		os.system("sudo brctl addbr LAN2")
	except:
		print("Error bridges LAN2")

	try :
		os.system("sudo ifconfig LAN1 up")
	except:
		print("Error LAN1 up")

	try :
		os.system("sudo ifconfig LAN2 up")
	except:
		print("Error LAN2 up")
    

#--- FIN PREPARE ---#

#--- ORDEN LAUNCH ---#	

elif orden == "launch" :

	f2 = open("auto-p2.json", "r")
	f2.readline()
	f2.readline()
	entrada = int(f2.readline())
	f2.close()

#Comprobamos si se inició ya alguna máquina o todas

	if len(sys.argv) > 2 :
			mv = sys.argv[2]
			bol = True
			fhin = open("auto-p2.json", "r")
			for line in fhin :
				if mv == "c1":
					bol = False
					if "launch c1 = 1" in line:
						print("El escenario de c1 ya se ha inicializado")
						sys.exit()
				elif mv == "lb":
					bol = False
					if "launch lb = 1" in line:
						print("El escenario de lb ya se ha inicializado")
						sys.exit()
				elif bol :
					for x in range(1,int(entrada)+1) :
						if mv == "s"+str(x) :
							if "launch s"+str(x)+" = 1" in line:
								print("El escenario de s"+str(x)+" ya se ha inicializado")
								sys.exit()
			fhin.close()
	else:
		fhin = open("auto-p2.json", "r")
		for line in fhin :
			if "launch = 1" in line:
				print("El escenario ya se ha inicializado")
				sys.exit()
		fhin.close()

#Se configura las conexion del escenario
	if len(sys.argv) > 2 :
		mv = sys.argv[2]
		bol = True
		if mv == "c1":
			bol = False
			fh = open("auto-p2.json", "r")
			fhout = open("p2pp", "w")
			for line in fh:
				if "launch c1 = 0" in line:
					fhout.write("launch c1 = 1 \n")
				else:
					fhout.write(line)
			fh.close()
			fhout.close()
			try:
				fhin2 = open("p2pp", "r")
				fhout2 = open("auto-p2.json", "w")
				for line in fhin2:
					fhout2.write(line)
				fhin2.close()
				fhout2.close()
			except:
				print("Error en copia del json")
			
			os.system("rm p2pp")

			print("Configurando la conexión del escenario c1")
			try :
				os.system("sudo virt-edit -a lb.qcow2 /etc/sysctl.conf -e 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/'")
			except:
				print("Error")

			try :
				os.system("sudo ifconfig LAN1 10.0.1.3/24") 
				os.system("sudo ip route add 10.0.0.0/16 via 10.0.1.1")
			except:
				print("Error")

			try :
				fhin = open("hostname", "w")
				fhin.write("c1")
				fhin.close()

				fhin2 = open("interfaces", "w")
				#Configuración de datos de la red local
				fhin2.write("auto lo\n")
				fhin2.write("iface lo inet loopback\n")
				fhin2.write("\n")
				fhin2.write("auto eth0\n")
				fhin2.write("iface eth0 inet static\n")
				fhin2.write("address 10.0.1.2\n")
				fhin2.write("netmask 255.255.255.0\n")
				fhin2.write("gateway 10.0.1.1\n")
				fhin2.write("dns-nameservers 10.0.1.2\n")
				fhin2.close()

				os.system("sudo virt-copy-in -a c1.qcow2 interfaces /etc/network")
				os.system("sudo virt-copy-in -a c1.qcow2 hostname /etc")

				os.system("rm hostname")
				os.system("rm interfaces")
			except:
				print("Error en la configuración de conexión del escenario de c1")

		elif mv == "lb":
			bol = False
			fh = open("auto-p2.json", "r")
			fhout = open("p2pp", "w")
			for line in fh:
				if "launch lb = 0" in line:
					fhout.write("launch lb = 1 \n")
				else:
					fhout.write(line)
			fh.close()
			fhout.close()
			try:
				fhin2 = open("p2pp", "r")
				fhout2 = open("auto-p2.json", "w")
				for line in fhin2:
					fhout2.write(line)
				fhin2.close()
				fhout2.close()
			except:
				print("Error en copia del json")

			os.system("rm p2pp")

			print("Configurando la conexión del escenario lb")
			try :
				fhin = open("hostname", "w")
				fhin.write("lb")
				fhin.close()

				#os.system("rm interfaces")

				fhin2 = open("interfaces", "w")
				fhin2.write("auto lo\n")
				fhin2.write("iface lo inet loopback\n")
				fhin2.write("\n")
				fhin2.write("auto eth0\n")
				fhin2.write("iface eth0 inet static\n")
				fhin2.write("address 10.0.1.1\n")
				fhin2.write("netmask 255.255.255.0\n")
				fhin2.write("gateway 10.0.1.1\n")
				fhin2.write("dns-nameservers 10.0.1.1\n")
				fhin2.write("\n")
				fhin2.write("auto eth1\n")
				fhin2.write("iface eth1 inet static\n")
				fhin2.write("address 10.0.2.1\n")
				fhin2.write("netmask 255.255.255.0\n")
				fhin2.write("gateway 10.0.2.1\n")
				fhin2.write("dns-nameservers 10.0.2.1\n")

				fhin2.close()

				os.system("sudo virt-copy-in -a lb.qcow2 interfaces /etc/network")
				os.system("sudo virt-copy-in -a lb.qcow2 hostname /etc")

				os.system("rm hostname")
				os.system("rm interfaces")

			except:
				print("Error en la configuración de conexión del escenario de lb")
		else :
			cuenco = False
			fh = open("auto-p2.json", "r")
			fhout = open("p2pp", "w")
			for line in fh:
				for x in range(1,int(entrada)+1) :
					if mv == "s"+str(x):
						cuenco = True
						if "launch "+mv+" = 0" in line:
							fhout.write("launch "+mv+" = 1 \n")
						else:
							fhout.write(line)
			fh.close()
			fhout.close()
			if cuenco == False:
				print("No existe la máquina indicada")
				sys.exit()
			try:
				fhin2 = open("p2pp", "r")
				fhout2 = open("auto-p2.json", "w")
				for line in fhin2:
					fhout2.write(line)
				fhin2.close()
				fhout2.close()
			except:
				print("Error en copia del json")

			os.system("rm p2pp")

			print("Configurando la conexión del escenario de los servidores")
			try :
				for x in range(1,int(entrada)+1) :
					fhin = open("hostname", "w")
					fhin.write("s"+str(x))
					fhin.close()

					#os.system("rm interfaces")

					fhin2 = open("interfaces", "w")
					fhin2.write("auto lo\n")
					fhin2.write("iface lo inet loopback\n")
					fhin2.write("\n")
					fhin2.write("auto eth0\n")
					fhin2.write("iface eth0 inet static\n")
					fhin2.write("address 10.0.2.1"+str(x)+"\n")
					fhin2.write("netmask 255.255.255.0\n")
					fhin2.write("gateway 10.0.2.1\n")
					fhin2.write("dns-nameservers 10.0.2.1"+str(x)+"\n")
					fhin2.close()

					fhin3 = open("index.html", "w")
					fhin3.write("<!DOCTYPE html><html><h1>S"+str(x)+"</h1></html>")
					fhin3.close()

					os.system("sudo virt-copy-in -a s"+str(x)+".qcow2 interfaces /etc/network")
					os.system("sudo virt-copy-in -a s"+str(x)+".qcow2 hostname /etc")
					os.system("sudo virt-copy-in -a s"+str(x)+".qcow2 index.html /var/www/html") 
					#modifica las paginas webs iniciales de los servidores para poder diferenciarlas 
					prp = 2

				os.system("rm hostname")
				os.system("rm interfaces")
				os.system("rm index.html") 
			except:
				print("Error en la configuración de conexión del escenario de los servidores")
	
	else:
		fh = open("auto-p2.json", "r")
		fhout = open("p2pp", "w")
		for line in fh:
			if "launch = 0" in line:
				fhout.write("launch = 1 \n")
			else:
				fhout.write(line)
		fh.close()
		fhout.close()
		try:
			fhin2 = open("p2pp", "r")
			fhout2 = open("auto-p2.json", "w")
			for line in fhin2:
				fhout2.write(line)
			fhin2.close()
			fhout2.close()
		except:
			print("Error en copia del json")
		
		os.system("rm p2pp")

		print("Configurando la conexión del escenario c1")

		try :
			os.system("sudo virt-edit -a lb.qcow2 /etc/sysctl.conf -e 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/'")
		except:
			print("Error")

		try :
			os.system("sudo ifconfig LAN1 10.0.1.3/24") 
			os.system("sudo ip route add 10.0.0.0/16 via 10.0.1.1")
		except:
			print("Error")

		try :
			fhin = open("hostname", "w")
			fhin.write("c1")
			fhin.close()

			fhin2 = open("interfaces", "a")
			#Configuración de datos de la red local
			fhin2.write("auto lo\n")
			fhin2.write("iface lo inet loopback\n")
			fhin2.write("\n")
			fhin2.write("auto eth0\n")
			fhin2.write("iface eth0 inet static\n")
			fhin2.write("address 10.0.1.2\n")
			fhin2.write("netmask 255.255.255.0\n")
			fhin2.write("gateway 10.0.1.1\n")
			fhin2.write("dns-nameservers 10.0.1.2\n")
			fhin2.close()

			os.system("sudo virt-copy-in -a c1.qcow2 interfaces /etc/network")
			os.system("sudo virt-copy-in -a c1.qcow2 hostname /etc")
		except:
			print("Error en la configuración de conexión del escenario de c1")
	
		print("Configurando la conexión del escenario lb")
		try :
			fhin = open("hostname", "w")
			fhin.write("lb")
			fhin.close()

			os.system("rm interfaces")

			fhin2 = open("interfaces", "a")
			fhin2.write("auto lo\n")
			fhin2.write("iface lo inet loopback\n")
			fhin2.write("\n")
			fhin2.write("auto eth0\n")
			fhin2.write("iface eth0 inet static\n")
			fhin2.write("address 10.0.1.1\n")
			fhin2.write("netmask 255.255.255.0\n")
			fhin2.write("gateway 10.0.1.1\n")
			fhin2.write("dns-nameservers 10.0.1.1\n")
			fhin2.write("\n")
			fhin2.write("auto eth1\n")
			fhin2.write("iface eth1 inet static\n")
			fhin2.write("address 10.0.2.1\n")
			fhin2.write("netmask 255.255.255.0\n")
			fhin2.write("gateway 10.0.2.1\n")
			fhin2.write("dns-nameservers 10.0.2.1\n")

			fhin2.close()

			os.system("sudo virt-copy-in -a lb.qcow2 interfaces /etc/network")
			os.system("sudo virt-copy-in -a lb.qcow2 hostname /etc")

		except:
			print("Error en la configuración de conexión del escenario de lb")
		
		print("Configurando la conexión del escenario de los servidores")
		try :
			for x in range(1,int(entrada)+1) :
				fhin = open("hostname", "w")
				fhin.write("s"+str(x))
				fhin.close()

				os.system("rm interfaces")

				fhin2 = open("interfaces", "a")
				fhin2.write("auto lo\n")
				fhin2.write("iface lo inet loopback\n")
				fhin2.write("\n")
				fhin2.write("auto eth0\n")
				fhin2.write("iface eth0 inet static\n")
				fhin2.write("address 10.0.2.1"+str(x)+"\n")
				fhin2.write("netmask 255.255.255.0\n")
				fhin2.write("gateway 10.0.2.1\n")
				fhin2.write("dns-nameservers 10.0.2.1"+str(x)+"\n")
				fhin2.close()

				fhin3 = open("index.html", "w")
				fhin3.write("<!DOCTYPE html><html><h1>S"+str(x)+"</h1></html>")
				fhin3.close()

				os.system("sudo virt-copy-in -a s"+str(x)+".qcow2 interfaces /etc/network")
				os.system("sudo virt-copy-in -a s"+str(x)+".qcow2 hostname /etc")
				os.system("sudo virt-copy-in -a s"+str(x)+".qcow2 index.html /var/www/html") 
				#modifica las paginas webs iniciales de los servidores para poder diferenciarlas 
				prp = 2

			os.system("rm hostname")
			os.system("rm interfaces")
			os.system("rm index.html") 
		except:
			print("Error en la configuración de conexión del escenario de los servidores")
#Se abre consola
	try :
		os.system("sudo virt-manager")  
	except:
		print("Error")

#Se definen e inicializan las distintas maquinas
	if len(sys.argv) > 2 :
			mv = sys.argv[2]
			bol = True
			if mv == "c1" or mv == "lb" :
				bol = False
				os.system("sudo virsh define "+mv+".xml")
				os.system("sudo virsh start "+mv)
				os.system("xterm -e \'sudo virsh console "+mv+" \' &")
			elif bol :
				for x in range(1,int(entrada)+1) :
					if mv == "s"+str(x) :
						os.system("sudo virsh define "+mv+".xml")
						os.system("sudo virsh start "+mv)
						os.system("xterm -e \'sudo virsh console "+mv+" \' &")
			
	else :
		try:
			os.system("sudo virsh define c1.xml")
			os.system("sudo virsh start c1") 
			os.system("xterm -e \'sudo virsh console c1 \' &")
			os.system("sudo virsh define lb.xml")
			os.system("sudo virsh start lb")
			os.system("xterm -e \'sudo virsh console lb \' &")

			for x in range(1,int(entrada)+1) :
				os.system("sudo virsh define s"+str(x)+".xml")
				os.system("sudo virsh start s"+str(x))
				os.system("xterm -e \'sudo virsh console s"+str(x)+" \' &")
		except:
			print("Error definiendo, inicializando las máquinas y/o abriendo las consolas")

#---- FIN LAUNCH ----#

#--- ORDEN STOP ---#

elif orden == "stop" :
    
#Comprobacion si sistema se ha inicializado

	f3 = open("auto-p2.json", "r")
	f3.readline()
	f3.readline()
	entrada = int(f3.readline())
	f3.close()

	if len(sys.argv) > 2 :
			mv = sys.argv[2]
			bol = True
			fhin = open("auto-p2.json", "r")
			for line in fhin :
				if mv == "c1":
					bol = False
					if "launch c1 = 0" in line:
						print("El escenario de c1 no se ha inicializado, usar launch")
						sys.exit()
				elif mv == "lb":
					bol = False
					if "launch lb = 0" in line:
						print("El escenario de lb no se ha inicializado, usar launch")
						sys.exit()
				elif bol :
					for x in range(1,int(entrada)+1) :
						if mv == "s"+str(x) :
							if "launch s"+str(x)+" = 1" in line:
								print("El escenario de s"+str(x)+" no se ha inicializado, usar launch")
								sys.exit()
			fhin.close()
	else:
		fhin = open("auto-p2.json", "r")
		for line in fhin :
			if "launch = 0" in line:
				print("El escenario no se ha inicializado, usar launch")
				sys.exit()
		fhin.close()


#Comprobacion de segundo argumento 
	if len(sys.argv) > 2 :
			mv = sys.argv[2]
			if mv == "c1" or mv == "lb" :
				os.system("sudo virsh shutdown "+mv)
			else :
				cuenco = False
				for x in range(1,int(entrada)+1) :
					if mv == "s"+str(x) :
						cuenco = True
						os.system("sudo virsh shutdown "+ mv)
				if cuenco == False:
					print("No existe la máquina indicada")
	else :
		os.system("sudo virsh shutdown c1")
		os.system("sudo virsh shutdown lb")
		for x in range(1,int(entrada)+1) :
			os.system("sudo virsh shutdown s"+str(x))

#---- FIN STOP ----#

#--- ORDEN RELEASE ---#	
elif orden == "release" :

	f4 = open("auto-p2.json", "r")
	f4.readline()
	f4.readline()
	entrada = int(f4.readline())
	f4.close()

	fhin = open("auto-p2.json", "r")
	for line in fhin :
		if "launch c1 = 1" in line:
			os.system("sudo virsh undefine c1")
			os.system("sudo virsh destroy c1")
	fhin.close()
	
	fhin = open("auto-p2.json", "r")
	for line in fhin :
		if "launch lb = 1" in line:
			os.system("sudo virsh undefine lb")
			os.system("sudo virsh destroy lb")
	fhin.close()

	fhin = open("auto-p2.json", "r")
	for line in fhin :
			for x in range(1,int(entrada)+1) :
				if "launch s"+str(x)+" = 1" in line:
					os.system("sudo virsh undefine s"+str(x))
					os.system("sudo virsh destroy s"+str(x))
	fhin.close()

	fhin = open("auto-p2.json", "r")
	for line in fhin :
		if "launch = 1" in line:
			os.system("sudo virsh undefine lb")
			os.system("sudo virsh undefine c1")
			os.system("sudo virsh destroy lb")
			os.system("sudo virsh destroy c1")
			for x in range(1,int(entrada)+1):
				os.system("sudo virsh undefine s"+str(x))
				os.system("sudo virsh destroy s"+str(x))
	fhin.close()

	try :
		os.system("rm c1.xml")
		os.system("rm -f c1.qcow2")
		os.system("rm lb.xml")
		os.system("rm -f lb.qcow2")
		os.system("rm auto-p2.json")
		for x in range(1,int(entrada)+1) :
			os.system("rm s"+str(x)+".xml")
			os.system("rm -f s"+str(x)+".qcow2")
		os.system("sudo ifconfig LAN1 down")
		os.system("sudo ifconfig LAN2 down")
		os.system("sudo brctl delbr LAN1")
		os.system("sudo brctl delbr LAN2")
	except:
		print("Error apagando las LAN")

#---- FIN STOP ----#

#--- ORDEN RESUME ---#	

elif orden == "resume" :

	#Comprobacion si sistema se ha inicializado
	f3 = open("auto-p2.json", "r")
	f3.readline()
	f3.readline()
	entrada = int(f3.readline())
	f3.close()

	if len(sys.argv) > 2 :
			mv = sys.argv[2]
			bol = True
			fhin = open("auto-p2.json", "r")
			for line in fhin :
				if mv == "c1":
					bol = False
					if "launch c1 = 0" in line:
						print("El escenario de c1 no se ha inicializado, usar launch")
						sys.exit()
				elif mv == "lb":
					bol = False
					if "launch lb = 0" in line:
						print("El escenario de lb no se ha inicializado, usar launch")
						sys.exit()
				elif bol :
					for x in range(1,int(entrada)+1) :
						if mv == "s"+str(x) :
							if "launch s"+str(x)+" = 1" in line:
								print("El escenario de s"+str(x)+" no se ha inicializado, usar launch")
								sys.exit()
			fhin.close()
	else:
		fhin = open("auto-p2.json", "r")
		for line in fhin :
			if "launch = 0" in line:
				print("El escenario no se ha inicializado, usar launch")
				sys.exit()
		fhin.close()

	#Comprobacion de segundo argumento 
	if len(sys.argv) > 2 :
		mv = sys.argv[2]
		if mv == "c1" or mv == "lb" :
			os.system("sudo virsh start "+mv)
			os.system("xterm -e \'sudo virsh console "+mv+" \' &")
		else :
			cuenco = False
			for x in range(1,int(entrada)+1) :
				if mv == "s"+str(x) :
					cuenco = True
					os.system("sudo virsh start "+mv)
					os.system("xterm -e \'sudo virsh console "+mv+" \' &")
			if cuenco == False:
				print("No existe la máquina indicada")
	else :
		os.system("sudo virsh start c1")
		os.system("sudo virsh start lb")
		os.system("xterm -e \'sudo virsh console c1 \' &")
		os.system("xterm -e \'sudo virsh console lb \' &")
		for x in range(1,int(entrada)+1) :
			os.system("sudo virsh start s"+str(x))
			os.system("xterm -e \'sudo virsh console s"+str(x)+" \' &")

#---- FIN RESUME ----#

#--- ORDEN WATCH ---#	

elif orden == "watch" :
	os.system("gnome-terminal -- watch sudo virsh list --all")

#---- FIN WATCH ----#














