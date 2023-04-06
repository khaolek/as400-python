# -*- coding: utf-8 -*-
import jpype
import jpype.imports
import os


# CALL $GETAGNM ('7300' ' ')
as400_server = "255.255.255.255"
#as400_user = "quser"
#as400_password = "quser"
as400_user = "BBOUSR"
as400_password = "BBOUSR"
as400_library = "TPIDEV"

jcom_ibm_as400_access_AS400 = "com.ibm.as400.access.AS400"
jcom_ibm_as400_data_ProgramCallDocument = "com.ibm.as400.data.ProgramCallDocument"

jvm_path = jpype.getDefaultJVMPath()

print(f"jvm_path > {jvm_path}")

filepath_script = os.path.dirname(os.path.abspath(__file__))
jar_as400_path = filepath_script + '/database/jt400-11.1.jar'


# Launch the JVM
#jpype.startJVM(jvm_path,  convertStrings=True)
jpype.startJVM(jvm_path)

jpype.addClassPath(jar_as400_path)

# import the Java modules
from com.ibm.as400.access import AS400
from com.ibm.as400.access import ProgramCall
from com.ibm.as400.access import ProgramParameter
from com.ibm.as400.access import AS400Message
from com.ibm.as400.access import AS400Text
from com.ibm.as400.access import AS400ZonedDecimal
from com.ibm.as400.access import CommandCall
from java.lang import String

as400 = AS400(as400_server, as400_user, as400_password)

print(f"as400 > {as400}")
if (as400 is not None):
	as400_include_library = ["CHGLIBL LIBL(*NONE)", "ADDLIBLE NEW38", "ADDLIBLE QGPL", "ADDLIBLE QSYS38",
							 "ADDLIBLE UTILITIES","ADDLIBLE PROGXREF", "ADDLIBLE CPLFILES", "ADDLIBLE CPLENG",
							 "ADDLIBLE CPLOBJ", "ADDLIBLE TPISRC", "ADDLIBLE TPIENGDOC",
	                         "ADDLIBLE TPIENG", f"ADDLIBLE {as400_library}", "ADDLIBLE TPIOBJ"]
	as400_programe = "$GETAGNM1"
	#fullProgramName = f"{as400_library}.LIB/$TEST01.PGM"
	fullProgramName = f"/QSYS.LIB/{as400_library}.LIB/{as400_programe}.PGM"
	print(f"Connection to {as400_server} Success")
	as400_connect = CommandCall(as400)
	for library_data in as400_include_library:
		print(f"Run command : {library_data}")
		as400_str_command = f"{library_data}"
		as400_connect.run(as400_str_command)
	
	#error no has library
	#Application error.  MCH3401 unmonitored by $GETAGNM at statement 0000000144, instruction X'0000'.

	print(f"fullProgramName > {fullProgramName}")
	
	#input = "4183"
	input = "0007300"
	output_length_param1 = 100
	output_length_param2 = 9
	print(f"input > {input}")
	#inData = input.encode()
	parameters = []
	as400_input = AS400Text(7, as400)
	inData = as400_input.toBytes(input)
	#print(as400_input)
	print(f"inData (bytes)> {inData}")
	print(type(inData))
	#print(as400_input.toObject(inData))
	#print(str(as400_input.toObject(inData)).encode())
	#parameters.append(ProgramParameter(str(as400_input.toObject(inData)).encode()))
	parameters.append(ProgramParameter(inData))
	parameters.append(ProgramParameter(100))
	#parameters.append(ProgramParameter(9))
	print(parameters)
	
	as400_connect = ProgramCall(as400)
	#as400_connect.setProgram(fullProgramName)
	as400_connect = ProgramCall(as400, fullProgramName, parameters)
	#as400_connect.setProgram(fullProgramName, parameters)
	as400_result = as400_connect.run()
	print(f"as400_result > {as400_result}")
	as400_msg = as400_connect.getMessageList()
	if(as400_result):
		print(f"Run programe {fullProgramName} success.")
		as400_output1 = parameters[1].getOutputData()
		#as400_output2 = parameters[2].getOutputData()
		#print("type(as400_output1) > ", type(as400_output1))
		
		as400_set_output1 = AS400Text(output_length_param1)
		as400_return1 = as400_set_output1.toObject(as400_output1)
		
		#as400_set_output2 = AS400ZonedDecimal(9, 2)
		#as400_return2 = as400_set_output2.toObject(as400_output2)
		#with open("file_output.txt", 'w+', encoding="utf8") as f:
		#	f.truncate(0)
		#	f.write(as400_return1.encode())
		
		print("type as400_return1 > ", as400_return1)
		print("type as400_return1 type > ", type(as400_return1))
		print("type as400_return1  > ", as400_return1)
		#print(as400_return1.encode("tis-620").decode("utf-8"))
		print("type as400_return1 encode > ", as400_return1.encode(encoding='UTF-8'))
		
		#s = bytes(as400_return1, 'UTF-8')
		#print(String(s, 'UTF-8'))
		import ebcdic
		#print(as400_return1.encode('cp838'))
		#print(as400_return1.encode('cp874'))
		#print(as400_return1.encode().decode('cp838'))
		
		
	else:
		print(f"Run programe {fullProgramName} unsuccess. : ")
		for data_row in as400_msg:
			print(data_row.getText())
			
	as400.disconnectAllServices()
else:
	print(f"Connection to {as400_server} Unsuccess")


jpype.shutdownJVM()
#jpype.detachThreadFromJVM()
