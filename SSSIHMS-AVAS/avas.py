from flask import Flask,render_template,request,session,flash,redirect,url_for
import pyaudio
import wave
import time
import datetime
import schedule
import os
import pygame
import sys
import threading
import werkzeug
import re
import subprocess
from easygui import *
import time
import webbrowser
import vlc



start_time="15:42" 
stop_time="15:45"

app = Flask(__name__)

#global variables for stopping the sound played and for authentication
flg=1
flag=0
str_var=1
stream1=""
previousFile = None
ENDEVENT=42
value=1#for stopping bhajans
value1=1

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init()
songNo=0
#The module for the automation of the bhajans will be done from here
#first find the current day.Based on the day play that particular platlist from time 5:00 am to 6:00 pm 
#we use schedule package for this purpose.

def assign():
	global flg
	global flag
	global str_var
	global stream1
	global previousFile
	global ENDEVENT
	global value#for stopping bhajans
	value=1
	flg=1
	flag=0
	str_var=1
	stream1=""
	previousFile = None
	ENDEVENT=42
	value1=1

def day():
	now = datetime.datetime.now()
	if now.strftime("%A")== "Monday":
		day=now.strftime("%A")
	if now.strftime("%A")== "Tuesday":
		day=now.strftime("%A")
	if now.strftime("%A")== "Wednesday":
		day=now.strftime("%A")
	if now.strftime("%A")== "Thursday":
		day=now.strftime("%A")
	if now.strftime("%A")== "Friday":
		day=now.strftime("%A")
	if now.strftime("%A")== "Saturday":
		day=now.strftime("%A")
	if now.strftime("%A")== "Sunday":
		day=now.strftime("%A")

	print "Todays day is",day
	print "Playing the playlist of",day#,That days playlist
	print "Server will start soon"
	# Get the playlist for the particular day.
	playlist = os.listdir('./playlist/'+ day)
	return playlist,day

#main function for songs playing
def play(filename,day):
	global songNo
	songNo += 1
	pygame.mixer.music.stop()
	previousFile = filename
	pygame.mixer.music.load('./playlist/'+day+'/'+ filename)
	print "Now playing " + filename + " songNo " + str(songNo)
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy():
		pygame.time.Clock().tick(1000)
		

def bhajans_play():
    global value
    pygame.mixer.music.set_volume(0.1)
    vol=pygame.mixer.music.get_volume()
    playlist,cur_day=day()
    for filename in playlist:
	if value==0:    
		return schedule.CancelJob
	print filename
	play(filename,cur_day)
	
    
def bhajans_stop():
    global value
    print('The bhajans will stop now'.format(datetime.datetime.now())) 
    pygame.mixer.music.stop()
    value=0
    schedule.clear('daily-tasks')	
    sys.exit()
    return scheduke.CancelJob	

def pause():
	pygame.mixer.music.pause()


def unpause():
	pygame.mixer.music.unpause()

def user_box(msg):
	title = "Login Information"
	fieldNames = [ "User Name", "Password"]
	fieldValues = []  
	fieldValues = multpasswordbox(msg,title, fieldNames)	
#To make sure that none of the fields was left blank
	while 1:  # do forever, until we find acceptable values and break out
		if fieldValues == None: 
        		break
		errmsg = ""
    # look for errors in the returned values
		for i in range(len(fieldNames)):
			if fieldValues[i].strip() == "":
				errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
		if errmsg == "": 
        		break # no problems found
    		else:
        		fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues)
	return fieldValues	


def valid(fieldValues):
	fp = open('user/user_details.txt','r')
	print fieldValues
	details = fp.readlines()
	for row in details:
		values=row.strip().split(':')
		if fieldValues[0]==values[0] and fieldValues[1]==values[1]:
			print ("Reply was:", fieldValues)
			print "Valid user"	
			return 1	
	user_box("Enter Valid credentials")	

def Admin_box():
	msgbox("Hello admin please login to use.", title = "SAIRAM")
	msg = "Enter the details:"
	fieldValues=user_box(msg)
	global value1
	global value
	val=valid(fieldValues)
	reply=""
	while value1==1:
		if value==0:  
			sys.exit(0)
			return schedule.CancelJob	
		msg="Hello Admin:"+fieldValues[0];
		choices= ["pause","play","stop","Exit","help"]
		reply=buttonbox(msg,choices=choices,title="SAIRAM")
		print reply
		if reply is "pause": 
		#pause the bhajans being played.
			pygame.mixer.music.pause()
		if reply is "play":
		#unpause or play the music stopped
			pygame.mixer.music.unpause()
		if reply is "stop":
		#stop the bahjans played (ie pause the bhajans.)
			pygame.mixer.music.pause()
		if reply is "Exit":
			Admin_box()
			#return schedule.CancelJob
		if reply is "help":
			#open 
			webbrowser.open("./help.html") 
			#pass
	

def authenticate_user(credentials):
	#session['username']=credentials['uname']
	fp = open('user/user_details.txt','r')
	details = fp.readlines()
	for row in details:
		values=row.strip().split(':')
		if credentials['uname']==values[0] and credentials['passwd']==values[1]:
			#session['logged_in']=True	
			return True
	return False

#main function call
@app.route("/")
def main():
	global flg
	flg=1
	#pause()
	return render_template('login.html')


@app.route("/bloodRequest",methods=['POST'])
def bloodRequest():
	#unpause()
	result = request.form
	check= authenticate_user(result)
	global flg
	if check == False:
		return render_template('error.html')
	#if session['logged_in']==False:
	#	return render_template('login.html')	
	if flg==0:
		return render_template('login.html')
	#flg=1	
	#session['logged_in']=True
	blood_group_list = ['O+','O-','A+','A-','B-','B+','AB-','AB+','ALL']
	return render_template('home.html',blood_group_list=blood_group_list)	

#route for logging out
@app.route("/logout",methods=['POST'])
def Exit():
	#session.clear()
	#session.pop('logged_in',None)	
	global flg
	flg=0
	return redirect(url_for('main'))

@app.route("/stop",methods=['GET','POST'])
def stop():
	global str_var
	#	if flag==1:	
	str_var=0
	unpause()
	blood_group_list = ['O+','O-','A+','A-','B-','B+','AB-','AB+','ALL']	
	return render_template('home.html',blood_group_list=blood_group_list)	

#method for adding a user	
@app.route("/adduser",methods=['POST'])
def adduser():
	return render_template('adduser.html');	


#method for admin to pause or play the music if at all	
@app.route("/Admin",methods=['GET','POST'])
def admin():
	#result = request.form
	#check= authenticate_user(result)
	#if check == False:
	#	return render_template('error.html')
	return render_template('Admin.html');	

@app.route("/Admin_home",methods=['POST'])
def admin_home():
	result = request.form
	check= authenticate_user(result)
	if check == False:
		return render_template('error.html')
	return render_template('Admin_home.html');	

@app.route("/home",methods=['POST'])
def home():
	#if not session.get('logged_in'):
       	#	return redirect(url_for('main'))
	blood_group_list = ['O+','O-','A+','A-','B-','B+','AB-','AB+','ALL']	
	return render_template('home.html',blood_group_list=blood_group_list)	
	
@app.route("/addusers",methods=['POST'])
def addusers():
	#if not session.get('logged_in'):
       	#	return redirect(url_for('main'))
	result=request.form
	if result['passwd']==result[passwd-rep]:
		s="\n"+result['uname']+":"+result['passwd']	
		fp=open('user/user_details.txt','ab');
		fp.write(s)
		fp.close()
		return 	render_template('user_added.html')
	else:
		return "Password missmatch"
#begining of the methods for playing audio.
def play_audio(path):
	chunk = 1048#1024 
	f = wave.open(path,"rb")  
	p = pyaudio.PyAudio()  
	stream = p.open(format = p.get_format_from_width(f.getsampwidth()),channels = f.getnchannels(),rate = f.getframerate(),output = True)  	
	global str_var
	data = f.readframes(chunk)  
	while data:  
	  if (str_var==0 and flag==1):
		  str_var=1	
		  stream.stop_stream()
		  stream.close()  
		  p.terminate() 
	  if (str_var==1):
		  stream.start_stream()
	  stream.write(data)  
	  data = f.readframes(chunk) 
	stream.stop_stream()  
	stream.close()  
	p.terminate() 

def play_all_blood_audio():
	path = 'audio/bloodgroup/'+'ALL'+str('.wav')
	play_audio(path)
	time.sleep(0.5)
	play_audio('audio/2.wav')
	time.sleep(0.5)
	play_audio('audio/7.wav')
	time.sleep(0.5)	
	play_audio('audio/6.wav')

def play_blood_names(result):
	i=1
	for element in result:
		path = 'audio/bloodgroup/'+str(element)+str('.wav')
		print path		
		play_audio(path)
		#play_audio('audio/Group.wav')				
		if ((len(result))!=i):		
			play_audio('audio/and.wav')
		#play_audio('audio/Groups.wav')
		i=i+1

def play_blood_groups(result):
	i=1
	for element in result:
		path = 'audio/bloodgroup/'+str(element)+str('.wav')
		
		print path		
		play_audio(path)
		#play_audio('audio/Group.wav')				
		play_audio('audio/only_groups/bloodgroup.wav')		
		if ((len(result))!=i):		
			play_audio('audio/and.wav')
		#play_audio('audio/Groups.wav')
		i=i+1

def play_group(result):
	i=1
	for element in result:
		path = 'audio/only_groups/'+str(element)+str('.wav')
		
		print path		
		play_audio(path)
		#play_audio('audio/Group.wav')				
		if ((len(result))!=i):		
			play_audio('audio/and.wav')
		#play_audio('audio/Groups.wav')
		i=i+1


def play_individual_blood_audio(result):
	
	play_blood_names(result) #plays names of checked blood groups
	time.sleep(0.7)	
	play_audio('audio/2.wav')
	time.sleep(0.5)
	play_audio('audio/3.wav')
	time.sleep(0.5)
	
	play_group(result)
	time.sleep(0.5)
	#play_audio('audio/Group.wav')
	if len(result)>1:
		play_audio('audio/only_groups/bloodgroups.wav')
	if len(result)==1:		
		play_audio('audio/only_groups/bloodgroup.wav')		
	
	time.sleep(0.5)	
	play_audio('audio/5.wav')
	time.sleep(0.5)	
	play_audio('audio/6.wav')

@app.route("/request_blood",methods=["POST"])
def request_blood():
	#pause the on going bhajans and make the announcement and unpause the song
	if request.method=='POST':
		result = request.form
		global flag
		flag=0
		print result == {}
		if result ==  {}:			
			blood_group_list = ['O+','O-','A+','A-','B-','B+','AB-','AB+','ALL']	
			return render_template('home.html',blood_group_list=blood_group_list)
		pause()
		flag=1
		play_audio('audio/before_announcement.wav')	
		time.sleep(1)		
		play_audio('audio/1.wav')
		time.sleep(1)
		for times in range(1,3):
			print "Result"
			print result
			if 'ALL' in result:
				play_all_blood_audio()
			else:
				play_individual_blood_audio(result)

			if times%2==1: # for 'I repeat'
				play_audio('audio/8.wav')
				#play_audio('')
				#play_audio('')
			time.sleep(0.5)		
		play_audio('audio/9.wav')	
		
		unpause()
		return render_template('after_announ.html')
	

def run_thread(job_fun):
	try:	
		job_thread= threading.Thread(target=job_fun)
		job_thread.start()
	except (KeyboardInterrupt, SystemExit):
		print '\n! Received keyboard interrupt, quitting threads.\n'


def avas():
	#Admin_box()
	print "The SSSIHMS-AVAS Server Started"
	try:
 	       if __name__=="__main__":
			app.secret_key = '3sdadsdad4'	
			app.run(host='0.0.0.0',threaded=True)
	except KeyboardInterrupt:
        # **** THIS PART NEVER EXECUTES. ****
        	print "You cancelled the program!"
        	sys.exit(1)	
	
def display():
	global start_time
	global stop_time
	os.system('clear')
	#sys("clear")
	print "				     		OM SRI SAIRAM\nThe Server and bhajans are going to start at time "+str(start_time)+" and stop at time "+str(stop_time)




#schedule.every().day.at("15:26").do(assign)
#schedule.every().day.at("15:26").do(run_thread,avas)
#schedule.every().day.at("15:26").do(run_thread,bhajans_play)
#schedule.every().day.at("15:26").do(run_thread,Admin_box)
#schedule.every().day.at("15:45").do(run_thread,bhajans_stop)
#schedule.every().day.at("15:44").do(avas_stop)

display()
schedule.every().day.at(start_time).do(display)
schedule.every().day.at(start_time).do(assign)
schedule.every().day.at(start_time).do(run_thread,Admin_box)
schedule.every().day.at(start_time).do(run_thread,avas)
schedule.every().day.at(start_time).do(run_thread,bhajans_play)
schedule.every().day.at(stop_time).do(run_thread,bhajans_stop)





#schedule.every().day.at("8:58").do(run_thread,avas)
#schedule.every().day.at("14:14").do(assign)
#schedule.every().day.at("14:14").do(run_thread,bhajans_play)
#schedule.every().day.at("14:15").do(run_thread,avas)
#schedule.every().day.at("14:16").do(run_thread,bhajans_stop)


while True:
	schedule.run_pending()
	time.sleep(1)	
	
