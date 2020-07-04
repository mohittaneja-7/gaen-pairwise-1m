#!/usr/bin/python3

import json
import sys
import time
import socket
import subprocess

ADB="/usr/bin/adb"
PHONE_SERVER_IP = "127.0.0.1" #"192.168.1.191" #"127.0.0.1"
PHONE_SERVER_PORT = 8081

def start_app():
	# make sure phone is awake and exposure notification app is running on phone
	#command = ADB + ' shell input keyevent 26'
	#command = ADB + ' -s HT85G1A05551 forward tcp:8081 tcp:8081\n' # forward localhost:8081 to phone:8081
	command = ADB + ' forward tcp:8081 tcp:8081\n' # forward localhost:8081 to phone:8081
	#command += ADB + ' shell am start -n "com.google.android.apps.exposurenotification.MainActivity" -a android.intent.action.MAIN -c android.intent.category.LAUNCHER'
	p = subprocess.Popen(command, shell=True,
											 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = p.communicate()
	print('%s%s'%(stdout,stderr))
	time.sleep(1) # might take a while for phone to wake up

def open_conn():
	# open connection to server on phone
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((PHONE_SERVER_IP, PHONE_SERVER_PORT))
	return s

def read_line(s,endline='\n'):
	line=""
	i=0
	while 1:
		res = s.recv(1)
		if (not res) or (res.decode("ascii") == endline): break
		line += res.decode("ascii")
	return line

def read_line_ok(s, cmd):
	# if response is not 'ok', bail
	resp = read_line(s)
	if (resp != 'ok'):  # something went wrong
		print(cmd + " : " + resp)
		exit(-1)

def send_cmd(s,cmd, readline = True):
	# send a command to the phone
	msg = bytearray()
	msg.extend(cmd.encode("ascii"))
	s.sendall(msg)
	if (readline):
		read_line_ok(s,cmd)

def get_tek():
	send_cmd(s,"GET\n",False)
	return read_line(s) # get the  response


def put_tek(tek,start,dur,token):
	send_cmd(s,"PUT "+tek.lower()+" "+str(start)+" "+str(dur)+" "+token+"\n",False)
	return read_line(s,"#") # get the  response

def putlong_tek(tek,start,dur,token):
	send_cmd(s,"PUTLONG "+tek.lower()+" "+str(start)+" "+str(dur)+" "+token+"\n",False)
	return read_line(s,"#") # get the  response

def putshort_tek(tek,start,dur,token):
	send_cmd(s,"PUTSHORT "+tek.lower()+" "+str(start)+" "+str(dur)+" "+token+"\n",False)
	return read_line(s,"#") # get the  response


start_app()
s=open_conn()

# plu->mer
#print(putlong_tek("1f1cb46d99e793d90f5b72496dea2940",2654724,6,"plu_to_mer"))
# plu->mer(low power on plu)
#print(putlong_tek("27e72047a69813aa47a3ad7d6303a84d",2654730,6,"plu_to_mer_lp"))
# mer->plu(low power on plu)
#print(putlong_tek("58d714995c095739e92dec241f109cd1",2654735,6,"mer_to_plu_lp"))
# mer->ur
#print(putlong_tek("cb0bc38afd1886d94a852373009c6c3a",2654740,6,"mer_to_ur"))
# ur->mer
#print(putlong_tek("d53ae1f23f4154def6385cfe6403be36",2654749,6,"ur_to_mer"))
# nep->sat
#print(putlong_tek("b8086c7d9c6cc25a2937d2a4afeeff4a",2654859,6,"nep_to_sat"))
# sat->nep
#print(putlong_tek("bff5766f0624d3046e5c2460412fc750",2654865,6,"sat_to_nep"))
# ur->nep
#print(putlong_tek("abc3c82387f9b7abb3eba3aef31c5736",2654870,6,"ur_to_nep"))
# nep->ur
# print(putlong_tek("09db43b79617a10ec87177d475fbcea5",2654875,6,"nep_to_ur"))
# sat->ur
# print(putlong_tek("5dae33cb87f9d224cb22bdbcfd5771b9",2654882,6,"sat_to_ur"))
# ur->sat
# print(putlong_tek("2454b0c9d4a76c4cc0671a33cd2b4374",2654895,6,"ur_to_sat"))
# nep->plu
# print(putlong_tek("3982c082f848d0d02815144468439d21",2655000,6,"nep_to_plu"))
# sat->mer
# print(putlong_tek("fab92fe4e0f9c067165984d117ef1b76",2655009,6,"sat_to_mer"))
# mer->sat
# print(putlong_tek("4936721f440ea5219fbcf5517a72095b",2655015,6,"mer_to_sat"))
# blue->pink
# print(putlong_tek("bcdc08cff1e4b053215d284e3a9801c2",2655050,6,"blue_to_pink"))
# km->jer
# print(putlong_tek("473178f5193ca1ce386cac30e99c62ea",2655145,6,"km_to_jer"))
# km->jer (re-do)
# print(putlong_tek("b0bc7c992430256fc4883f8d4c0220df",2655152,6,"km_to_jer1"))
# km->pink
# print(putlong_tek("be319a53383558d50638eacd707bc1ae",2655157,6,"km_to_pink"))
# km->plu
# print(putlong_tek("921430cbd7643a9fa7c9ec9c56518a1b",2655162,6,"km_to_plu"))
# km->sat
# print(putlong_tek("80fe45fc26f033094289b6d604dd3df5",2655167,6,"km_to_sat"))
# km->ur
# print(putlong_tek("7c9e1ebfb8d24abb3cadb88ebae29321",2655173,6,"km_to_ur"))
# km->mer
# print(putlong_tek("9b5b250ade7da260115f7646e02ea6af",2655177,6,"km_to_mer"))
# blue->mer
# print(putlong_tek("0df85b07a4dd73adad63e774e6c8bc3a",2655186,6,"blue_to_mer"))
# blue->jer
# print(putlong_tek("4c5e8ea3c66a27c1ff4e32c5a6c8eecb",2655192,6,"blue_to_jer"))
# blue->ur
# print(putlong_tek("0310cd075ddf380bb32658185e7f0db5",2655276,6,"blue_to_ur"))
# blue->sat
# print(putlong_tek("e4567876fc6bef074a1207ef7dc43d3c",2655284,6,"blue_to_sat"))
# blue->nep
# print(putlong_tek("0fcd41076667e4db85add3b8b061cdeb",2655295,6,"blue_to_nep"))
# nep->pink
# print(putlong_tek("2a0789706182adc185d7bae84ddb9493",2655300,6,"nep_to_pink"))
# nep->pink
# print(putlong_tek("f708401469c4a30f6eca1803bdcba715",2655306,6,"sat_to_pink"))
# ur->pink
#print(putlong_tek("3ad40f9c08e259ed4ca42ac17a426c0e",2655310,6,"ur_to_pink"))
# mer->pink
# print(putlong_tek("168f0b8be8bd1f337c0367da22d3f728",2655314,6,"mer_to_pink"))
# mer->jer
# print(putlong_tek("ddf006e5421777edc51216b41bbd6d35",2655431,6,"nep_to_jer"))
# sat->jer
# print(putlong_tek("dbf340846ce4826924e743ad0105c120",2655437,6,"sat_to_jer"))
# ur->jer
# print(putlong_tek("d0ddc99a98dc6f28365c6ef429f0b3e9",2655442,6,"ur_to_jer"))
# mer->jer
# print(putlong_tek("b523e44eb2d7db8775f492f0e6eb13b2",2655447,6,"mer_to_jer"))
# km->pink repeat (outlier result 1st time)
# print(putlong_tek("ce9fa67fe651119f779989e3afef2500",2655743,6,"km_to_pink_again"))
# jer->blue (outlier result 1st time)
# print(putlong_tek("610603344fd783c138d36e452ff9b62a",2655748,6,"jer_to_blue_again"))
# jer->blue repeat (outlier result 1st time)
# print(putlong_tek("cf4da947d660b31a9040daa11f2e740e",2655756,6,"jer1_to_blue1_again"))
# jer->blue 2nd repeat (outlier result 1st time)
# print(putlong_tek("8f0b5655dd15eb924dd9e7e2e985267e",2655859,6,"jer2_to_blue2_again"))
# jer->blue 3rd repeat (outlier result 1st time)
# print(putlong_tek("cbedd7e99c4c8ac5d346ca48bdd56d63",2655864,6,"jer3_to_blue3_again"))
# jer->blue 4th repeat (outlier result 1st time)
# print(putlong_tek("d5e44d124aa38d9a26fb285e985f1093",2655868,6,"jer4_to_blue4_again"))
# km->blue 2nd repeat (outlier result 1st time)
# print(putlong_tek("b94b406cfc2117853cb220a6694e2a3c",2655876,6,"km2_to_blue5_again"))
# km->blue 3rd repeat (outlier result 1st time)
# print(putlong_tek("631e70e7af96304c4991bacc8b54c9ff",2655881,6,"km3_to_blue6_again"))
# km->pink repeat (outlier result 1st time)
# print(putlong_tek("bf998473449c0ab1b9673bc08d601336",2655881,6,"km4_to_pink2_again"))
# km->pink repeat (outlier result 1st time)
# print(putlong_tek("33773cdfef903b8b523defccbda8c02c",2655890,6,"km5_to_pink3"))
# km->blue double
# print(putlong_tek("35f571e2b97b70bcc071a870baca62da",2655901,6,"km_to_blue"))
# jer->blue double
# print(putlong_tek("1331c54d0901945b35a4bb5797c744c7",2655901,6,"jer_to_blue"))
# km->pink double
# print(putlong_tek("35f571e2b97b70bcc071a870baca62da",2655901,6,"km_to_pink"))
# jer->pink double
# print(putlong_tek("1331c54d0901945b35a4bb5797c744c7",2655901,6,"jer_to_pink"))
# km->blue double2
# print(putlong_tek("3258e34decbc86f0868d329bc47a92a0",2656006,6,"km_to_blue"))
# jer->blue double2
# print(putlong_tek("d77a29fe77690a0636ef7902159e3133",2656006,6,"jer_to_blue"))
# km->pink double2
# print(putlong_tek("3258e34decbc86f0868d329bc47a92a0",2656006,6,"km_to_pink"))
# jer->pink double2
# print(putlong_tek("d77a29fe77690a0636ef7902159e3133",2656006,6,"jer_to_pink"))
# km->blue double3
# print(putlong_tek("e20b1ecf625f226478f97a2b0e6c9c25",2656012,6,"km_to_blue"))
# jer->blue double3
# print(putlong_tek("7d0b965f09c8c04dae5b32cd103d764e",2656012,6,"jer_to_blue"))
# km->pink double3
# print(putlong_tek("e20b1ecf625f226478f97a2b0e6c9c25",2656012,6,"km_to_pink"))
# jer->pink double3
# print(putlong_tek("7d0b965f09c8c04dae5b32cd103d764e",2656012,6,"jer_to_pink"))

# run4
# nep->blue double3
# print(putlong_tek("573468c48ddebc948a96b01e2ec8b993",2656019,6,"nep_to_blue"))
# plu->blue double3
# print(putlong_tek("1772575ec57bc1e23c910fb59737e171",2656019,6,"plu_to_blue"))
# nep->pink double3
# print(putlong_tek("573468c48ddebc948a96b01e2ec8b993",2656019,6,"nep_to_pink"))
# plu->pink double3
# print(putlong_tek("1772575ec57bc1e23c910fb59737e171",2656019,6,"plu_to_pink"))

# run5
# nep->blue double3 
# print(putlong_tek("daf0d4b702512535c400991c084196bd",2656027,6,"nep_to_blue"))
# plu->blue double3
# print(putlong_tek("5a6debc8f4a7216753cdcd00cafcffb5",2656027,6,"plu_to_blue"))
# nep->pink double3
# print(putlong_tek("daf0d4b702512535c400991c084196bd",2656027,6,"nep_to_pink"))
# plu->pink double3
# print(putlong_tek("5a6debc8f4a7216753cdcd00cafcffb5",2656027,6,"plu_to_pink"))

# nep->blue solo
# print(putlong_tek("c2ff3f55fbaf234557f9282df41e6091",2656149,6,"nep_to_blue"))
# nep->pink solo
print(putlong_tek("57089d8724447e603ae7518ff634931f",2656163,6,"nep_to_pink"))

