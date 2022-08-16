#importing necessary modules
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
import pyaudio,wave, winsound, time, datetime
#from imap_saving_attachement_gmail import *
   
fromaddr = "testsender531@gmail.com"
toaddr = "receivertest05@gmail.com"
password = "FOProjectx07"

#pane = 'vtoreceive'


   
# instance of MIMEMultipart 
msg = MIMEMultipart() 
  
# storing the senders email address   
msg['From'] = fromaddr 
  
# storing the receivers email address  
msg['To'] = toaddr 
def send_func(file_name):
    subject = "VoiceChat000:"+file_name
    # storing the subject  
    msg['Subject'] = subject
      
    # string to store the body of the mail 
    body = "Body_of_the_mail"
      
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 
      
    # open the file to be sent  
    attachment = open("C:/vdownloads/{}".format(file_name), "rb") 
      
    # instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream') 
      
    # To change the payload into encoded form 
    p.set_payload((attachment).read()) 
      
    # encode into base64 
    encoders.encode_base64(p) 
       
    p.add_header('Content-Disposition', "attachment; filename= %s" % file_name) 
      
    # attach the instance 'p' to instance 'msg' 
    msg.attach(p) 
      
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
      
    # start TLS for security 
    s.starttls() 
      
    # Authentication 
    s.login(fromaddr, password) 
      
    # Converts the Multipart msg into a string 
    text = msg.as_string() 
      
    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 
  
    # terminating the session 
    s.quit()

#voice recording function
def record_func():
    global file_name
    file_name = "a"+str( int(time.time()) )+".wav"
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    #WAVE_OUTPUT_FILENAME = "file.wav"
     
    audio = pyaudio.PyAudio()
     
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print ("recording...")
    frames = []
     
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print ("finished recording")
     
     
    # stop Recording
    stream.stop_stream() 
    stream.close()
    audio.terminate()  
    waveFile = wave.open("C:/vdownloads/{}".format(file_name),'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def play_sound():
    winsound.PlaySound("C:/vdownloads/{}".format(file_name), winsound.SND_FILENAME)


file_name = "a"+str( int(time.time()) )+".wav"
import imaplib, email,os, time, datetime,winsound
from functools import partial

#authentication credentials
imap_host = "imap.gmail.com"
pwd = "FOProjectx007"
user_name = "receivertest05@gmail.com"

filename = 'nothing'
from tkinter import *
root = Tk()

#list of saved messages
file_list = []

#button class
class b:
	def __init__(self, t, m):
		self.t = t
		self.m = m
		self.name = time.strftime("%H:%M:%S", time.localtime(int(t[1:])))
		print(self.name)
		print(type(self.name))
		print(self.t)
		p = partial(play, self.t+'.wav')
		b = Button(rframe, text = str(int(self.name[0:2])%12)+self.name[2:]+" "+self.m['From'], bg = 'black', bd = 5,fg = 'white', font = ("Gadugi", 12), command = p)
		b.pack()

def play(file_name):
	winsound.PlaySound("C:/vdownloads/{}".format(file_name), winsound.SND_FILENAME)

def create_auth():#creates the authentication screen
    global root
    root.geometry("1000x670")
    #root.wait_visibility(root)
    #root.wm_attributes('-alpha',0.75)
    global f
    f = Frame(root, bg = 'black', height = 670, width = 1000)
    f.pack_propagate(False)

    global background_image
    background_image=PhotoImage(file = 'bg2.png')
    global background_label
    background_label = Label(f, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    global sf
    sf = Frame(f, bg = 'black', height = 360, width = 495, highlightbackground = 'blue',highlightcolor = '#1F618D', highlightthickness = 4)
    sf.grid_propagate(False)
    sf.pack_propagate(False)
    sf.place(x = 255,y = 255)

    global id_label
    id_label = Label(sf, text = "Email:", bg = 'black', fg = '#1F618D', font = ('papyrus', 23))
    id_label.grid(row = 0, column = 0, sticky = W)

    global id_entry
    id_entry = Entry(sf, textvariable = user_name, width = 34, bg = 'black', fg = 'white', highlightbackground='#1F618D', highlightthickness = 2,font = ('papyrus',18) )
    id_entry.grid(row = 1, column = 0 ,padx = 3)

    global pwd_label
    pwd_label = Label(sf, text = "Password:", bg = 'black', fg = '#1F618D', font = ('papyrus', 23))
    pwd_label.grid(row = 2, column = 0, sticky = W)

    global pwd_entry
    pwd_entry = Entry(sf, textvariable = password, show = '*', width = 34, bg = 'black', fg = 'white', highlightbackground='#1F618D', highlightthickness = 2,font = ('papyrus',18) )
    pwd_entry.grid(row = 3, column = 0, padx = 3)
    global login_button
    login_button = Button(sf, text = "LOGIN", bg = '#000080', fg = 'white', bd = 6, highlightthickness = 3,font = ("papyrus", 18), width = 29, command = open_receive_screen)
    login_button.grid(row = 4, column = 0, padx = 3, pady = 4)
    f.pack()

def sort(email_list):#sorts the byte email list
    for x in range(len(email_list)-1,0,-1):
        for y in range(x):
            if email_list[y]>email_list[y+1]:
                email_list[y],email_list[y+1] = email_list[y+1],email_list[y]
    return email_list

    
def fetch_func_new():#fecthes unread messages
    
        imap = imaplib.IMAP4_SSL(imap_host)
        imap.login(user_name, pwd)
        imap.select('INBOX')
        #imap.login(user_name, pwd)
        svdir = "C:/vdownloads/"
        #if data is a single value
        result, data = imap.uid('search', None, 'HEADER Subject "VoiceChat000"', 'UNSEEN')

        email_list = data[0].split()#added

        #sorting emails
        email_list = sort(email_list)           


        for i in range(len(email_list)):#fetches all messages
                result, email_data = imap.uid('fetch', data[0].split()[i], "RFC822")
                raw_email = email_data[0][1].decode("utf-8")
                m = email.message_from_string(raw_email)

                for part in m.walk():
                        global filename
                        filename=part.get_filename()
                        if filename is not None and filename not in file_list:

                            file_list.append(filename)
                            button = b(filename[:-4],m)#my part
                            sv_path = os.path.join(svdir, filename)
                            if not os.path.isfile(sv_path):
                                print(sv_path)  
                                fp = open(sv_path, 'wb')
                                fp.write(part.get_payload(decode=True))
                                fp.close()
        print(data)
        imap.close()#closing connection

        
def ff():#creates message frame
    global rframe
    rframe = Frame(root,bg = '#212F3D',height = 603, width = 508, highlightbackground = 'black',highlightcolor = '#1F618D', highlightthickness = 7)
    rframe.grid_propagate(False)
    rframe.pack_propagate(False)
    rframe.place(x = 265, y = 0)


def open_receive_screen():#opens the receiving screen
    f.pack_forget()
    global root
    root.destroy()
    root = Tk()
    #root.wait_visibility(root)
    #root.wm_attributes('-alpha',0.95)
    root.geometry("1000x670")
    root.title("VoiceApp")
    global background_image
    background_image=PhotoImage(file = 'pppp.png')

    
    global background_label
    background_label = Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    
    #calling all functions to initiate the main process
    ff()
    fetch_func_new()

    #refresh button
    refresh_button = Button(root, text = 'REFRESH', bg = '#212F3D', fg = 'white', bd = 6,font = ("papyrus", 15), command = fetch_func_new)
    refresh_button.place(x = 265, y = 605)

#iniating program flow
create_auth()
root.mainloop()
