# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 20:50:58 2019

@author: Dasu Gautham Sreeram
"""
#This is the second version of avas for steaming the bhajans from the radio sai website.
#The goal of this program is to give voice output of announcements along with bhajans playing from the radio sai stream.

from flask import Flask,render_template,request,session,redirect,url_for
import pyaudio
import wave
import time
import datetime
import schedule
import os
import pygame
import sys
import threading
from easygui import *
import webbrowser
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import vlc
import urllib


app = Flask(__name__)

#global variables for stopping the sound played and for authentication
flg=1
flag=0
pygame_val=0
str_var=1
stream1=""
previousFile = None
ENDEVENT=42
value=1#for stopping bhajans
url = "http://stream.radiosai.org:8000/"
#bhajans_abs=""
vlc_player = vlc.MediaPlayer(url)
if(urllib.urlopen(url).getcode()!=200):
	pygame_val=1

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
	url = "http://stream.radiosai.org:8000/"



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
		

def bhajans_play(vlc_val):
    #we are modifing the part here directly using radio sai stream we are playing the bhajans
    while(value!=0 ):        
        if(pygame_val==0):
            vlc_player.play()
        if(vlc_val==1):
            vlc_player.stop     ()
        else(pygame_val==1):
            global value
            pygame.mixer.music.set_volume(0.1)
            vol=pygame.mixer.music.get_volume()
            print vol	
            playlist,cur_day=day()
            for filename in playlist:
	       if value==0 and pygame_val==1:    
		     return schedule.CancelJob
	       print filename
	       play(filename,cur_day)
    	
    
def bhajans_stop():
    if(pygame_val==0):    
        vlc_player.stop()
    else:
        global value
        print('{} Now the system will exit '.format(datetime.datetime.now())) #this works ok
        pygame.mixer.music.stop()
        value=0
        schedule.clear('daily-tasks')	
        sys.exit()
        return scheduke.CancelJob	
       
def pause():
    vlc_player.stop()
    if(pygame_val==0):    
        vlc_player.stop()
    else:       
     	   pygame.mixer.music.pause()


def unpause():
    vlc_player.play()
    if(pygame_val==0):    
        vlc_player.play()
    else:
        pygame.mixer.music.unpause()

def exit():
    print('{} Now the system will exit '.format(datetime.datetime.now())) #this works ok
    if(pygame_val==0):    
            vlc_player.stop()
    else:
            pygame.mixer.music.stop() 		    
    sys.exit()



def user_box(msg):
	title = "Login Information"
	fieldNames = [ "User Name", "Password"]
	fieldValues = []  
	fieldValues = multpasswordbox(msg,title, fieldNames)	
	print fieldValues[0]
	
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
  	#valid(fieldValues)
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
	print fieldValues
	val=valid(fieldValues)
	while 1:

		msg="Hello Admin";
		choices= ["pause","play","stop","help"]
		reply=buttonbox(msg,choices=choices,title="SAIRAM")
		print reply
		if reply is "pause": 
		#pause the bhajans being played.
			p.pause()
			#pygame.mixer.music.pause()
		elif reply is "play":
		#unpause or play the music stopped
			p.play()
#			pygame.mixer.music.unpause()
		elif reply is "stop":
		#stop the bahjans played (ie pause the bhajans.)
			p.stop()
			#pygame.mixer.music.pause()
		elif reply is "help":
			#open 
			webbrowser.open("./help.html") 
			#pass
		   
#def avas():
#authenticates the user for logging in.
def authenticate_user(credentials):
	#session['username']=credentials['uname']
	fp = open('user/user_details.txt','r')
	details = fp.readlines()
	for row in details:
		values=row.strip().split(':')
		if credentials['uname']==values[0] and credentials['passwd']==values[1]:
			session['logged_in']=True	
			return True
	return False

#main function call
@app.route("/")
def main():
	global flg
	flg=1
	#bhajans_play()
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
	if session['logged_in']==False:
		return render_template('login.html')	
	if flg==0:
		return render_template('login.html')
	#flg=1	
	session['logged_in']=True
	blood_group_list = ['O+','O-','A+','A-','B-','B+','AB-','AB+','ALL']
	return render_template('home.html',blood_group_list=blood_group_list)	

#route for logging out
@app.route("/logout",methods=['POST'])
def Exit():
	session.clear()
	session.pop('logged_in',None)	
	global flg
	flg=0
	return redirect(url_for('main'))

@app.route("/stop",methods=['GET','POST'])
def stop():
	global str_var
	str_var=0
	unpause()
	blood_group_list = ['O+','O-','A+','A-','B-','B+','AB-','AB+','ALL']	
	return render_template('home.html',blood_group_list=blood_group_list)	


@app.route("/adduser",methods=['POST'])
def adduser():
	return render_template('adduser.html');	



@app.route("/Admin",methods=['GET','POST'])
def admin():
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
	if not session.get('logged_in'):
       		return redirect(url_for('main'))
	blood_group_list = ['O+','O-','A+','A-','B-','B+','AB-','AB+','ALL']	
	return render_template('home.html',blood_group_list=blood_group_list)	
	
@app.route("/addusers",methods=['POST'])
def addusers():
	if not session.get('logged_in'):
       		return redirect(url_for('main'))
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
	play_audio('audio/2.wav')
	play_audio('audio/7.wav')
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
		#stop_thread(bhajans_play)
		global flag
		flag=0
		print result == {}
		if result ==  {}:			
			blood_group_list = ['O+','O-','A+','A-','B-','B+','AB-','AB+','ALL']	
			return render_template('home.html',blood_group_list=blood_group_list)
		pause()

		flag=1
		devices = AudioUtilities.GetSpeakers()
		interface = devices.Activate(
		IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
		volume = cast(interface, POINTER(IAudioEndpointVolume))
		volume.GetMute()
		volume.GetMasterVolumeLevel()
		volume.GetVolumeRange()
		volume.SetMasterVolumeLevel(-10.0, None)	
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
		volume.SetMasterVolumeLevel(-20.0, None)	
		
		unpause()
		return render_template('after_announ.html')
	

def run_thread(job_fun):
	try:	
		job_thread= threading.Thread(target=job_fun)
		job_thread.start()
		return job_thread
            
	except (KeyboardInterrupt, SystemExit):
		print '\n! Received keyboard interrupt, quitting threads.\n'

def stop_thread(job_thread):
		job_thread= threading.Thread(target=job_fun)
		job_thread.stop()           		
def avas():
	
	print "The SSSIHMS-AVAS Server Started"
	try:
 	       if __name__=="__main__":
                 app.secret_key = '3sdadsdad4'
                 app.run(host='0.0.0.0',threaded=True)
      #           bhajans_play()
	except KeyboardInterrupt:
        # **** THIS PART NEVER EXECUTES. ****
        	print "You cancelled the program!"
        	sys.exit(1)	
            

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()



def avas_stop():
		shutdown_server()



 
  


run_thread(avas)
run_thread(bhajans_play)


#schedule.every().day.at("20:49").do(assign)
#schedule.every().day.at("20:49").do(run_thread,avas)
#schedule.every().day.at("20:49").do(run_thread,bhajans_play)
#schedule.every().day.at("20:49").do(run_thread,Admin_box)
#schedule.every().day.at("20:50").do(run_thread,bhajans_stop)
#schedule.every().day.at("8:58").do(run_thread,avas)
#schedule.every().day.at("14:14").do(assign)
#schedule.every().day.at("14:14").do(run_thread,bhajans_play)
#schedule.every().day.at("14:15").do(run_thread,avas)
#schedule.every().day.at("14:16").do(run_thread,bhajans_stop)


#while True:
#	schedule.run_pending()
#	time.sleep(1)	
	




 
