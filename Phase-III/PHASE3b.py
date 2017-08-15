###PHASE 3 GROUP 57
import pymysql
from tkinter import *
import urllib.request
import base64
from tkinter import ttk
import sys
import calendar, datetime
import random
import re


class GUI:
      
            
            
      def connect(self):
            ##This function attempt to connect to the course database
            ## Display error Message if failure
            ##return pymysql Object( db)
            ##

            try:
            
                  db = pymysql.connect( host = 'academic-mysql.cc.gatech.edu',
                  passwd = 'ea_DMrZ8', user = 'cs4400_Group_57', db='cs4400_Group_57')##conecting to the course database

                  return db #retuning a pymysql object

            except:
                  messagebox.showerror('connection problem', 'There was an error with this connection.')
                  


      def loginCheck(self):
            ##This function checks if a person is clear to Login
            ##If the there exist  the user name associated with the given password within the database
            ##return none
            db=self.connect()##connect return a the pymysql Created above
            if db is not None:
                  self.username=self.EntryLoginUser.get()#get the user entered in the entry box as a sting
                  self.password=self.EntryLoginPass.get()#get the Password the user entered

                  c=db.cursor()#creating a Cursor object which will allow us to execute The SQL COMMAND
                  a=0#setting a to something
                  
                  #SQL Statment that check if there exist such a Usrname associated with the password typed by the user within the database
                  n1=c.execute('SELECT * FROM CUSTOMER WHERE Username=%s AND Password=%s',(self.username,self.password))
                  n2=c.execute('SELECT * FROM MANAGEMENT WHERE Mgm_Username=%s AND Password=%s',(self.username,self.password))
                  
                  if n1==0 and n2==0:##No show error
                        messagebox.showerror('Access Denied','Invalid Username and/or Password')
                  if n1==1 or n2==1:##yes SAY access granted
                        a=messagebox.showinfo('Access Granted','You have logged in')
                  if a=='ok' and n1==1:
                        
                        self.win.withdraw()##if the acess is granted destroy the win root
                        self.Custfunctionality()
                  if a=='ok' and n2==1:
                        
                        self.win.withdraw()##if the acess is granted destroy the win root
                        self.Manafunctionality()
                  c.close()      ##close the cursor
                  ##no need to commit the change because no change has been made
                  db.close()# close the pymysql Object
            #print(username,password)
      def cancel(self):
            
            db=self.connect()
            c=db.cursor()
            sql='UPDATE RESERVATION SET Cancel_Flag = 1,Total_Cost=%s WHERE Rsv_ID = %s'
            c.execute(sql,(self.r2,self.cancelEntry.get()))
            messagebox.showinfo('Sucess',' Your Reservation Has been Canceled')
 #           ExistingRsv=c.fetchone()
            c.close()
            db.commit()
            db.close()
                  
      def cancelInfo(self):
            
            db=self.connect()
            c=db.cursor()
            n1=c.execute('SELECT * FROM RESERVATION WHERE Cust_Username=%s AND Cancel_Flag=0 AND Rsv_ID=%s',(self.username,self.cancelEntry.get()))
            ExistingRsv=c.fetchone()
            
            
            
            
            try:
                  self.cancelFrame.destroy()
                  
            except:
                  pass
            try:
                  self.cancelFrame.destroy()
                  
            except:
                  pass
            self.cancelFrame=Frame(self.cancelPage,relief=RAISED, borderwidth=1 )
            self.cancelFrame.pack()

            frame1=Frame(self.cancelFrame)
            frame1.pack()
            
            frame2=Frame(self.cancelFrame)
            frame2.pack()

            frame3=Frame(self.cancelFrame)
            frame3.pack()

            frame4=Frame(self.cancelFrame)

            frame4.pack()
            
            if n1==1 :
##                  self.searchRsvframe=Frame(self.updatePage,relief=RAISED, borderwidth=1 )
##                  self.searchRsvframe.pack()
                  n=c.execute('SELECT * FROM ROOM NATURAL JOIN RESERVES WHERE Rsv_ID =%s',(self.cancelEntry.get()))
                  reservedRoom=c.fetchall()
                  now=datetime.datetime.now()
                  delta=str(datetime.datetime.strptime(str(ExistingRsv[1]), '%Y-%m-%d')-datetime.datetime.now())

                  days=int(delta.partition(' ')[0])
                  #print(days)

                  now1=str(datetime.datetime.now()).partition(' ')[0]
                  #print(now)
                            

                  #refund=0
                  if days<=1:
                        refund=0
                  if days==3 or days==2:
                        refund=0.8
                  if days>=4:
                        refund=1

                  Label(frame1, text='RSV Start Date').grid(row=0,column=0)
                  self.curSdateEntry=Entry(frame1)
                  self.curSdateEntry.grid(row=0, column=1)
                  self.curSdateEntry.insert(0,ExistingRsv[1])
                  self.curSdateEntry.config(state='disabled')
                  
                        
                  
                  
                  Label(frame1, text='RSV End Date').grid(row=0,column=2)
                  self.curEdateEntry=Entry(frame1)
                  self.curEdateEntry.grid(row=0, column=3)
                  self.curEdateEntry.insert(0,ExistingRsv[2])
                  self.curEdateEntry.config(state='disabled')
                  
                  i=1
                  Label(frame2, text='Room Number ',relief=RAISED, borderwidth=1).grid(row=0,column=0)
                  Label(frame2, text='Room Category ',relief=RAISED, borderwidth=1).grid(row=0,column=1)
                  Label(frame2, text='#persons Allowed ',relief=RAISED, borderwidth=1).grid(row=0,column=2)
                  Label(frame2, text='Cost per day ',relief=RAISED, borderwidth=1).grid(row=0,column=3)
                  Label(frame2, text='cost of Extra Bed ',relief=RAISED, borderwidth=1).grid(row=0,column=4)
                  Label(frame2, text='Extra Bed',relief=RAISED, borderwidth=1).grid(row=0,column=5)


                  Label(frame3, text='Total Cost of Reservation',).grid(row=0,column=0)
                  Label(frame3, text='Date of Cancellation',).grid(row=1,column=0)
                  Label(frame3, text='Amount to be refunded',).grid(row=2,column=0)

                  Tcost=Entry(frame3)
                  Tcost.grid(row=0, column=1)
                  Tcost.insert(0,ExistingRsv[3])
                  Tcost.config(state='disabled')
                      

                  Cdate=Entry(frame3)
                  Cdate.grid(row=1, column=1)
                  Cdate.insert(0,now1)
                  Cdate.config(state='disabled')

                  self.r= float(ExistingRsv[3])*float(refund)
                  self.r2=float(ExistingRsv[3] )- float(ExistingRsv[3])*float(refund)

                  refund1=Entry(frame3)
                  refund1.grid(row=2, column=1)
                  refund1.insert(0,self.r)
                  refund1.config(state='disabled')

                  Button(frame4, text='cancel',command=self.cancel).grid()
                  

                  


                  for tup in reservedRoom:
                       # print(tup)
                        
                  
                  
                  
                        #print(i)
                        self.v2=IntVar()
                        
                        Label(frame2, text=str(tup[0])).grid(row=i,column=0)
                        Label(frame2, text=str(tup[3])).grid(row=i,column=1)
                        Label(frame2, text=str(tup[5])).grid(row=i,column=2)
                        Label(frame2, text='$'+str(tup[2])).grid(row=i,column=3)
                        
                        Label(frame2, text='$'+str(tup[4])).grid(row=i,column=4)
                        if tup[-1]==0:
                              c=Checkbutton(frame2,text=str(i),variable=self.v2)
                              c.grid(row=i,column=5)
                              c.config(state=DISABLED)
                        else:
                              c=Checkbutton(frame2,text=str(i),variable=self.v2)
                              c.grid(row=i,column=5)
                              c.select()
                              c.config(state=DISABLED)
                        
      #                       self.vars.append(self.v2)
                        i=i+1
            else:
                  Label(frame1, text='No such RSV Found').grid(row=0,column=0)
                  
            
            
      def cancelReservation(self):
            self.cancelPage=Toplevel()
            frame1=Frame(self.cancelPage)
            frame1.pack()
            
            #frame1=Frame(self.cancelPage).

            Label(frame1, text='Reservation ID').grid(row=0,column=0)
            self.cancelEntry=Entry(frame1)
            self.cancelEntry.grid(row=0, column=1)
            Button(frame1,text='Search', command=self.cancelInfo).grid(row=0, column=2)
            
      def totalUpdate(self):
            delta=str(datetime.datetime.strptime(self.newEdateEntry.get(), '%Y/%m/%d')-datetime.datetime.strptime(self.newSdateEntry.get(), '%Y/%m/%d'))

            days=int(delta.partition(' ')[0])
 #           selectedBed=list(map((lambda c: c.get()), self.vars2))
            roomCost=0
            bedcost=0
            t=1
            for i in self.roomdata:
                  roomCost=roomCost+i[2]
                  if i[-1]==1:
                        bedcost=bedcost+i[4]
                  t=t+1
            uptotalCost=roomCost*days + bedcost*days
            return uptotalCost

      def saveUpdate(self):
            try:
                  self.searchAvframe.destroy()
            except:
                  pass

            db=self.connect()
            c=db.cursor()

            sql='UPDATE RESERVATION SET Check_In_Date=%s, Check_Out_Date=%s, Total_Cost=%s WHERE rsv_id =%s'
            c.execute(sql,(self.newSdateEntry.get(),self.newEdateEntry.get(),self.newAmount,self.roomdata[0][6]))

            

            c.close()
            db.commit()
            db.close()
            messagebox.showinfo('Sucess',' Your Reservation Has been Upadated')
            
      def searchAv(self):
            try:
                  self.searchAvframe.destroy()
            except:
                  pass

            

            db=self.connect()
            c=db.cursor()
            n1=c.execute('SELECT * FROM ROOM NATURAL JOIN RESERVES WHERE Rsv_ID =%s',(self.updateEntry.get()))
            Info=c.fetchall()
            self.roomdata=Info
            info1=Info[0]
            location=info1[1]
           # print(Info)
            #print(info1)
            try:
                  
                  
                 
                  datetime.datetime.strptime(self.newSdateEntry.get(), '%Y/%m/%d')
                  datetime.datetime.strptime(self.newEdateEntry.get(), '%Y/%m/%d')
            except:
                  #print('1')
                  messagebox.showerror('Date Error', 'Not a valid Date(s)')
                  #self.roomPage.deiconify()
                  return
            now=datetime.datetime.now()
            #print(now.date())
            if datetime.datetime.strptime(self.newSdateEntry.get(), '%Y/%m/%d')< datetime.datetime.strptime(self.newEdateEntry.get(), '%Y/%m/%d') and  now <= datetime.datetime.strptime(self.newSdateEntry.get(), '%Y/%m/%d'):
                  sql='SELECT * FROM ROOM NATURAL JOIN RESERVES WHERE Location =%s AND Rsv_ID=%s AND (Room_Num, Location) NOT IN (SELECT Room_Num, Location FROM RESERVES NATURAL JOIN RESERVATION  WHERE Cancel_Flag=0 AND Rsv_ID<>%s AND ( (Check_In_DATE < %s) AND  (Check_Out_DATE > %s)))'
       #           sql1='
                  n=c.execute(sql,(location,self.updateEntry.get(),self.updateEntry.get(), self.newEdateEntry.get(),self.newSdateEntry.get()))
                  availableRoom=c.fetchall()
                  self.searchAvframe=Frame(self.updatePage,relief=RAISED, borderwidth=1 )
                  self.searchAvframe.pack()
                  #print(availableRoom)
                  i=1
                  #print(availableRoom)
                  #print(len(availableRoom))

                  if len(availableRoom)>0 and n1==n:
                                   
                        
                        
                        Label(self.searchAvframe, text='Room Number ',relief=RAISED, borderwidth=1).grid(row=0,column=0)
                        Label(self.searchAvframe, text='Room Category ',relief=RAISED, borderwidth=1).grid(row=0,column=1)
                        Label(self.searchAvframe, text='#persons Allowed ',relief=RAISED, borderwidth=1).grid(row=0,column=2)
                        Label(self.searchAvframe, text='Cost per day ',relief=RAISED, borderwidth=1).grid(row=0,column=3)
                        Label(self.searchAvframe, text='cost of Extra Bed ',relief=RAISED, borderwidth=1).grid(row=0,column=4)
                        Label(self.searchAvframe, text='Extra Bed',relief=RAISED, borderwidth=1).grid(row=0,column=5)


                        for tup in availableRoom:
                             # print(tup)
                              
                        
                        #print(selectedRoom[1])
                        
                              #print(i)
                              self.v2=IntVar()
                              
                              Label(self.searchAvframe, text=str(tup[0])).grid(row=i,column=0)
                              Label(self.searchAvframe, text=str(tup[3])).grid(row=i,column=1)
                              Label(self.searchAvframe, text=str(tup[5])).grid(row=i,column=2)
                              Label(self.searchAvframe, text='$'+str(tup[2])).grid(row=i,column=3)
                              
                              Label(self.searchAvframe, text='$'+str(tup[4])).grid(row=i,column=4)
                              if tup[-1]==0:
                                    c=Checkbutton(self.searchAvframe,text=str(i),variable=self.v2)
                                    c.grid(row=i,column=5)
                                    c.config(state=DISABLED)
                              else:
                                    c=Checkbutton(self.searchAvframe,text=str(i),variable=self.v2)
                                    c.grid(row=i,column=5)
                                    c.select()
                                    c.config(state=DISABLED)
                              
            #                       self.vars.append(self.v2)
                              i=i+1
                        
                        
                        Label(self.searchAvframe,text='Total cost Update').grid(row=1000, column=0,columnspan=3,sticky=E)
                        cost=Entry(self.searchAvframe)
                        try:
                              cost.delete(0,END)
                        except:
                              pass
                        
                              
                        self.newAmount=self.totalUpdate()
                        
                        cost.grid(row=1000, column=3,columnspan=2)
                        cost.insert(0,self.newAmount)
                        cost.config(state=DISABLED)
                        Button(self.searchAvframe,text='Submit',command=self.saveUpdate).grid(row=1001, column=4)
                  else:
                        Label(self.searchAvframe, text='We are sorry! One of the Room(s) you have reserved  previously is (are) not available for the new dates').grid(row=0)
                        Label(self.searchAvframe, text='Click One of the below to cancel or create a new Reservation').grid(row=1)
                        Button(self.searchAvframe, text=' Cancel Reservation',command=self.cancelReservation).grid(row=2,column=0)

                        Button(self.searchAvframe, text=' Create  a new Reservation',command=self.searchRoom).grid(row=2,column=1)
                        
            
            else:
                  #print('2')
                  messagebox.showerror('Date Error', 'Not a valid Dates')
                  
                  
                  
            
      def searchRsv(self):
            db=self.connect()
            c=db.cursor()
            n=c.execute('SELECT * FROM RESERVATION WHERE Cust_Username=%s AND Rsv_ID=%s',(self.username, self.updateEntry.get()))
            ExistingRsv=c.fetchone()
            try:
                  self.searchRsvframe.destroy()
                  
            except:
                  pass
            try:
                  self.searchAvframe.destroy()
                  
            except:
                  pass
            if n==1:
                  self.searchRsvframe=Frame(self.updatePage,relief=RAISED, borderwidth=1 )
                  self.searchRsvframe.pack()

                  Label(self.searchRsvframe, text='Current Start Date').grid(row=0,column=0)
                  self.curSdateEntry=Entry(self.searchRsvframe)
                  self.curSdateEntry.grid(row=0, column=1)
                  self.curSdateEntry.insert(0,ExistingRsv[1])
                  self.curSdateEntry.config(state='disabled')
                  
                        
                  
                  
                  Label(self.searchRsvframe, text='Current End Date').grid(row=0,column=2)
                  self.curEdateEntry=Entry(self.searchRsvframe)
                  self.curEdateEntry.grid(row=0, column=3)
                  self.curEdateEntry.insert(0,ExistingRsv[2])
                  self.curEdateEntry.config(state='disabled')
                  
                  Label(self.searchRsvframe, text='New Start Date').grid(row=1,column=0)
                  self.newSdateEntry=Entry(self.searchRsvframe)
                  self.newSdateEntry.grid(row=1, column=1)
                  self.newSdateEntry.insert(0,'yyyy/mm/dd')
                  
                  
                  Label(self.searchRsvframe, text='New End Date').grid(row=1,column=2)
                  self.newEdateEntry=Entry(self.searchRsvframe)
                  self.newEdateEntry.grid(row=1, column=3)
                  self.newEdateEntry.insert(0,'yyyy/mm/dd')
                  

                  Button(self.searchRsvframe,text='Search Availability', command=self.searchAv).grid(row=3, column=2)
            else:
                  self.searchRsvframe=Frame(self.updatePage,relief=RAISED, borderwidth=1 )
                  self.searchRsvframe.pack()
                  Label(self.searchRsvframe, text='No coresponding Reservation has been found, very your Rsv ID').grid()
                  
      
                  
            

      def updateReservation(self):
            self.updatePage=Toplevel()
            frame1=Frame(self.updatePage,relief=RAISED, borderwidth=1 )
            frame1.pack()

            Label(frame1, text='Reservation ID').grid(row=0,column=0)
            self.updateEntry=Entry(frame1)
            self.updateEntry.grid(row=0, column=1)
            Button(frame1,text='Search', command=self.searchRsv).grid(row=0, column=2)

            
            
            
            

                  
            
                  
      def searchRoom(self):
            #Search Room
                  self.place.iconify()
                  self.roomPage=Toplevel()
                  self.roomPage.title('Room Search')

                  frame1=Frame(self.roomPage )
                  frame1.grid(row=0, columnspan=2)
                  Label(frame1, text="Fill the below information for you Reservation").grid(row=0,column=0)

                  Label(frame1, text="Choose a Location").grid(row=1,column=0)
                  
                  self.location = StringVar(self.roomPage)
                  self.location.set("Atlanta")
                  cityList =  OptionMenu(frame1,self.location,"Atlanta", "Charlotte","Savannah", "Orlando", "Miami")
                  cityList.grid(row=2,column=0)

                  ##Start Date

                  frame2=Frame(self.roomPage,relief=RAISED, borderwidth=1 )
                  frame2.grid(row=2,column=0)
                  Label(frame2, text='Start Date', ).grid(row=0,column=1)

                  Label(frame2, text='Month', ).grid(row=1,column=1)
                  Label(frame2, text='Day',).grid(row=1,column=2)
                  Label(frame2, text='Year',).grid(row=1,column=3)

                  self.sday = StringVar(self.roomPage)
                  self.sday.set('01')
                  day1List =  OptionMenu(frame2,self.sday,'01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31')
                  day1List.grid(row=2,column=2)

                  self.smonth = StringVar(frame2)
                  self.smonth.set('01')
                  month1List =  OptionMenu(frame2,self.smonth,"01", "02", '03', '04', '05', '06', '07', '08','09','10', '11', '12')
                  month1List.grid(row=2,column=1)

                  self.syear = IntVar(frame2)
                  self.syear.set(2015)
                  year1List =  OptionMenu(frame2,self.syear,2015,2016)
                  year1List.grid(row=2,column=3)
                  ##middle part
                  frame5=Frame(self.roomPage)
                  frame5.grid(row=1,column=1,columnspan=2)
                  Label(frame5,text=' ').grid(row=1)
                  Label(frame5,text=' ').grid(row=2)
                  
                  frame4=Frame(self.roomPage)
                  frame4.grid(row=2,column=1)

                  Label(frame4, text='    |    ').grid(row=0,column=0)
                  Label(frame4, text='    |    ').grid(row=1,column=0)
                  Label(frame4, text='    |    ').grid(row=2,column=0)
                  Label(frame4, text='    |    ').grid(row=3,column=0)
                  Label(frame4, text='         ').grid(row=4,column=0)

                  frame6=Frame(self.roomPage)
                  frame6.grid(row=3,column=1,columnspan=2)

                  searchButton= Button(frame6, text='Search', command=self.makeReservation)
                  searchButton.grid()

                  

                  ##End Date

                  frame3=Frame(self.roomPage,relief=RAISED, borderwidth=1)
                  frame3.grid(row=2,column=2)
                  Label(frame3, text='END Date').grid(row=0,column=1,columnspan=3)

                  Label(frame3, text='Month', ).grid(row=1,column=1)
                  Label(frame3, text='Day',).grid(row=1,column=2)
                  Label(frame3, text='Year', ).grid(row=1,column=3)

                  self.eday = StringVar(self.roomPage)
                  self.eday.set('01')
                  day1List =  OptionMenu(frame3,self.eday,'01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31')
                  day1List.grid(row=2,column=2)

                  self.emonth = StringVar(frame3)
                  self.emonth.set('01')
                  month1List =  OptionMenu(frame3,self.emonth,"01", "02", '03', '04', '05', '06', '07', '08','09','10', '11', '12')
                  month1List.grid(row=2,column=1)

                  self.eyear = IntVar(frame3)
                  self.eyear.set(2015)
                  year1List =  OptionMenu(frame3,self.eyear,2015,2016)
                  year1List.grid(row=2,column=3)




            

                  
                  

                  ##Calendar
                  

                  
                  #for city in ["Atlanta", "Charlotte","Savannah", "Orlando", "Miami"]:
                     #listbox.insert(END, city)
                  
                  
     
            
            
      def finalOption(self):
            
            selectedRoom2=list(map((lambda v: v.get()), self.vars2))

            return selectedRoom2
      def saveCard(self):

            CCFname=self.EntryCardFName.get()
            CCLname=self.EntryCardLName.get()
            CCnum=self.EntryCardnum.get()
            CCex=self.EntryCardEx.get()
            Cvv=self.EntryCvv.get()
            try:
                  datetime.datetime.strptime(CCex, '%Y/%m/%d')
                  #datetime.datetime.strptime(self.edate, '%Y/%m/%d')
            except:
                  messagebox.showerror('Date Error', 'Not a valid Date')
                  #self.roomPage.deiconify()
                  return

            now=datetime.datetime.now()
            if now.date() > datetime.datetime.strptime(CCex, '%Y/%m/%d').date():
                  messagebox.showerror('error','the date you entered is in the past')
                  return
                  
            
            db=self.connect()
            if db is not None:
                  c= db.cursor()
                  n=c.execute('SELECT * FROM CREDIT_CARD WHERE Cust_Username=%s AND CC_Num=%s', (self.username,CCnum))

                  if CCFname!='' and CCFname!='' and len(CCnum)==16 and len(Cvv)==3 and len(CCex)!='' and n==0:
                        try:
                              #self.frame2.destroy()
                              int(CCnum)
                              int(Cvv)
                              
                              c.execute('INSERT INTO CREDIT_CARD (Cust_First_Name,Cust_Last_Name,Cust_Username, CC_Num, Exp_Date,CCV_NUM) VALUES (%s,%s,%s,%s,%s,%s)',(CCFname,CCLname,self.username,CCnum,CCex,Cvv))
                              R=messagebox.showinfo('Sucess',' You have entered a new card')
                              if R=='ok':
                                    self.makeReservation()
                                    self.reservationDetail()
                                    
                              
                        except:
                              
                              messagebox.showerror('Error!!', 'Credit Requirments not met!/or This credit Card is already in the system')
                        
                              
                  else:
                        
                        messagebox.showerror('Error!!', 'Credit Requirments not met!/or This credit Card is already in the system')
                        
                  
 #                 c.execute('INSERT INTO CUSTOMER (First_Name,Last_Name, Username, Password, Email) VALUES (%s,%s,%s,%s,%s)',(First_Name,Last_Name,Username,passwd,Email))
                  c.close()
                  db.commit()
                  db.close()

      def delCard(self):
            db=self.connect()
            
            if db is not None:
                  c=db.cursor()
                  n1=c.execute('SELECT * FROM RESERVATION WHERE Cust_Username=%s AND DATEDIFF(Check_Out_Date,CURDATE())>0 AND CC_num LIKE %s LIMIT 1',(self.username,"%" + str(self.variable2.get())))
 #                 print(n1)

                  if n1>0:
                        messagebox.showinfo('Error', 'you cannot delete this card because it being used for a reservation')
                        c.close()
                        db.close()
                  else:
                        
                                     
                        n=c.execute('DELETE FROM CREDIT_CARD WHERE Cust_Username=%s AND CC_num LIKE %s LIMIT 1',(self.username,"%" + str(self.variable2.get())))

                        

                        c.close()
                        db.commit()
                        db.close()
                        ok=messagebox.showinfo('Succes','Your card Has been deleted')
                        #print(n)
                        if ok=='ok':
                              self.cardPage.destroy()
       #                       self.paymentInfo()
                              self.reservationDetail()
##                        
            
                        
                        
            #pass

      def paymentInfo(self):
            try:
                  self.cardPage.destroy()
            except:
                  pass
                  
            
            self.cardPage=Toplevel()
            self.cardPage.title("Payment Information")
            frame1=Frame(self.cardPage,relief=RAISED, borderwidth=1)
            frame1.grid(row=0,column=0)

            Label(frame1, text='ADD CARD').grid(row=0,column=0, columnspan=2, sticky=W)

            Label(frame1, text='Firts Name on Card').grid(row=1,column=0,sticky=W)
            Label(frame1, text='Last Name on Card').grid(row=2,column=0,sticky=W)
            Label(frame1, text='Card Number').grid(row=3,column=0,  sticky=W)
            Label(frame1, text='Expiration Date').grid(row=4,column=0, sticky=W)
            Label(frame1, text='CVV').grid(row=5,column=0,  sticky=W)

            self.EntryCardFName=Entry(frame1,width=30)
            self.EntryCardFName.grid(row=1,column=1)

            self.EntryCardLName=Entry(frame1,width=30)
            self.EntryCardLName.grid(row=2,column=1)

            self.EntryCardnum=Entry(frame1,width=30)
            self.EntryCardnum.grid(row=3,column=1)

            self.EntryCardEx=Entry(frame1,width=30)
            self.EntryCardEx.grid(row=4,column=1)
            self.EntryCardEx.insert(0, 'yyyy/mm/dd')

            self.EntryCvv=Entry(frame1,width=10)
            self.EntryCvv.grid(row=5,column=1)

            

            

      

            Button(frame1,text='save', command=self.saveCard).grid(row=6)

            frame2=Frame(self.cardPage,relief=RAISED, borderwidth=1)
            frame2.grid(row=0,column=1)

            Label(frame2, text='DELETE CARD').grid(row=0,column=0, sticky=W)
            Label(frame2, text=' ').grid(row=1,column=0, sticky=W)
            Label(frame2, text='Card Number:').grid(row=2,column=0, sticky=W)

 #           if db is not None:
            
      
 #                 n=c.execute('SELECT * FROM CREDIT_CARD WHERE Cust_Username=%s',(self.username))
 #                 self.UserCreditCard=c.fetchall()

    
            b=Button(frame2, text='DELETE',command=self.delCard)
            b.grid(row=3,column=0)
            b.config(state=DISABLED)
            
            if len(self.UserCreditCard)>0:
                  b.config(state=NORMAL)
                  
 #                 self.submitButton.config(state="normal")
                  ccnum=[]
                  for i in self.UserCreditCard:
                        ccnum.append(i[0])

                  cc4num=[]

                  for i in ccnum:
                        cc4num.append(i[12:])
                  self.variable2 = StringVar(frame2)
                  self.variable2.set(cc4num[0])
                  w = OptionMenu(frame2, self.variable2,*cc4num)
                  w.grid(row=2,column=1)
            else:
                  b.config(state=DISABLED)
                  self.variable2 = StringVar(frame2)
                  w = OptionMenu(frame2, self.variable2,'No Card')
                  w.grid(row=2,column=1)
                  

 #           Button(frame2, text='DELETE',command=self.delCard).grid(row=3,column=0)
                  


                  

                  
      def RsvIdGenerator(self):
            rn=random.randint(100000,999999)
            db=self.connect()

            if db is not None:
                  c=db.cursor()
                  n=c.execute('SELECT * FROM RESERVATION WHERE Rsv_ID=%s',(rn))
                  if n==0:
                        c.close()
                        db.close()
                        
                        return rn
                        
                  else:
                        self.RsvIdGenerator
                        
 #           return 
            
      def confirmReservation(self):
            
            db=self.connect()
            c=db.cursor()
            self.submitButton.config(state="disabled")
            
            c.execute('SELECT CC_num FROM CREDIT_CARD WHERE Cust_Username=%s AND CC_num LIKE %s LIMIT 1',(self.username,"%" + str(self.variable.get())))
            cc_num=c.fetchone()
           # print(cc_num)
            
            
            if db is not None:
                  rn=self.RsvIdGenerator()
                  sql='INSERT INTO RESERVATION (Rsv_ID, Check_In_Date, Check_Out_Date, Total_Cost, Cust_Username, CC_Num) VALUES  (%s, %s, %s,%s, %s, %s)'

                  c.execute(sql,(rn,self.sdate,self.edate,self.totalCost, self.username,cc_num[0]))

                  

                  sql1='INSERT INTO RESERVES (Room_Num, Location, Rsv_ID,Extra_Bed) VALUES (%s,%s,%s,%s)'
                  selectedBed=list(map((lambda c: c.get()), self.vars2))
                  i=0

                  for tup in self.selectedRoomList:
                        c.execute(sql1,(tup[0],tup[1],rn,selectedBed[i]))

                        i=i+1
                                        

                  

            
            

            self.ConfirmScreen=Toplevel()
            

            self.ConfirmScreen.title('Confirmation Screen')

            frame = Frame(self.ConfirmScreen)
            frame.pack()

            Label(frame, text='Your Reservation ID').grid(row=0,column=0)

            e=Entry(frame)
            e.grid(row=0,column=1)

            e.insert(0,rn)
            e.config(state='disabled')

            frame1=Frame(self.ConfirmScreen)
            frame1.pack()
            

            Label(frame1, text='Please save this reservation ID for all further Communication').grid(row=0)

            Button(frame1, text='Return to main page',command=self.Custfunctionality).grid(row=1,column=1)
            
            
            
            #pass

            c.close()
            db.commit()
            db.close()
                   
            
            
            
            
      def total(self):
            if len(self.UserCreditCard)>0:
                  self.submitButton.config(state="normal")
            else:
                  self.submitButton.config(state="disabled")
                  
            stayDelta=str(datetime.datetime.strptime(self.edate, '%Y/%m/%d')-datetime.datetime.strptime(self.sdate, '%Y/%m/%d'))
            
            days=int(stayDelta.partition(' ')[0])
            selectedBed=list(map((lambda c: c.get()), self.vars2))
            roomCost=0
            bedcost=0
            t=1
            for i in self.selectedRoomList:
                  roomCost=roomCost+i[2]
                  if selectedBed[t-1]==1:
                        bedcost=bedcost+i[4]
                  t=t+1
            self.totalCost=roomCost*days + bedcost*days
            #print(self.totalCost, days)
            
                  

            self.EntryTcost.configure(state=NORMAL)
            try:
                  self.EntryTcost.delete(0,END)
            except:
                  pass

            self.EntryTcost.insert(0,self.totalCost)
            self.EntryTcost.configure(state='disabled')
            

      def reservationDetail(self):
            
            try:
                  self.frame2.destroy()
            except:
                  pass
            selectedRoom=list(map((lambda v: v.get()), self.vars))
            #print(list(map((lambda v: v.get()), self.vars)))
            #return( map((lambda var: var.get(), self.vars)))
            self.frame2=Frame(self.reservationPage,relief=RAISED, borderwidth=1)
            self.frame2.pack()

            frame3=Frame(self.frame2)
            frame3.pack()
            #print(selectedRoom[1])
            stayDelta=datetime.datetime.strptime(self.edate, '%Y/%m/%d')-datetime.datetime.strptime(self.sdate, '%Y/%m/%d')
            days=int(str(stayDelta)[0])
            #print(selectedRoom)
            
            if sum(selectedRoom)==0:
                  
                  
                  Label(frame3, text='None of the Above Has been Selected').grid()
            else:
                  Label(frame3, text='Room Number ',relief=RAISED, borderwidth=1).grid(row=0,column=0)
                  Label(frame3, text='Room Category ',relief=RAISED, borderwidth=1).grid(row=0,column=1)
                  Label(frame3, text='#persons Allowed ',relief=RAISED, borderwidth=1).grid(row=0,column=2)
                  Label(frame3, text='Cost per day ',relief=RAISED, borderwidth=1).grid(row=0,column=3)
                  Label(frame3, text='cost of Extra Bed ',relief=RAISED, borderwidth=1).grid(row=0,column=4)
                  Label(frame3, text='Extra Bed',relief=RAISED, borderwidth=1).grid(row=0,column=5)
                  i=1
                  self.vars2=[]
                  self.selectedRoomList=[]
                  for tup in self.availableRoom:
                        
                        
                        if selectedRoom[i-1]==1:
                              #print(i)
                              self.selectedRoomList.append(tup)
                              self.v2=IntVar()
                              
                              Label(frame3, text=str(tup[0])).grid(row=i,column=0)
                              Label(frame3, text=str(tup[3])).grid(row=i,column=1)
                              Label(frame3, text=str(tup[5])).grid(row=i,column=2)
                              Label(frame3, text='$'+str(tup[2])).grid(row=i,column=3)
                              Label(frame3, text='$'+str(tup[4])).grid(row=i,column=4)
                              Checkbutton(frame3,text=str(i),variable=self.v2).grid(row=i,column=5)
                              self.vars2.append(self.v2)
                              i=i+1
                        else:
                              i=i+1
                  #Button(frame3,text='Proceed to Payment',command=self.finalOption).grid(row=i+1)
                  self.frame44=Frame(self.frame2)
                  self.frame44.pack()

                 # print(self.selectedRoomList)

                  Label(self.frame44, text='Start Date').grid(row=0,column=0)
                  Label(self.frame44, text='Total Cost').grid(row=1,column=0)
                  Label(self.frame44, text='Use Card').grid(row=2,column=0)

                  

                  #print(selectedRoomList)
##                  roomCost=0
##                  bedcost=0
##                  t=1
##                  for i in self.selectedRoomList:
##                        roomCost=roomCost+i[2]
##                        if selectedBed[t-1]==1:
##                              bedcost=bedcost+i[4]
##                  totalCost=roomCost*days + bedcost

                  #print(totalCost=self.total())
                              
                              
                        

                  

                  
                  
                        

                  Label(self.frame44, text='End Date').grid(row=0,column=2)
                  
                  



                  EntrySdate=Entry(self.frame44,width=15)
                  EntrySdate.grid(row=0,column=1)
                  EntrySdate.insert(0,self.sdate)
                  EntrySdate.configure(state='disabled')
                  
                  EntryEdate=Entry(self.frame44,width=15)
                  EntryEdate.grid(row=0,column=3)
                  EntryEdate.insert(0,self.edate)
                  EntryEdate.configure(state='disabled')

                  self.EntryTcost=Entry(self.frame44,width=15)
                  self.EntryTcost.grid(row=1,column=1)
                  self.EntryTcost.configure(state='disabled')

                  Button(self.frame44,text='GetCost',command=self.total).grid(row=3,column=2)
                  
                  db=self.connect()##connect return a the pymysql Created above
                  if db is not None:
                        c=db.cursor()
                        ##SELECT * FROM RESERVATION WHERE Cust_Username=%s AND DATEDIFF(Check_Out_Date,CURDATE())>0 

                  
                        n=c.execute('SELECT * FROM CREDIT_CARD WHERE Cust_Username=%s AND DATEDIFF(Exp_Date,CURDATE())>=0',(self.username))
                        self.UserCreditCard=c.fetchall()

                        self.submitButton=Button(self.frame44, text='Submit',command=self.confirmReservation)
                        self.submitButton.grid(row=3,column=3)
                        self.submitButton.config(state="disabled")
                        
                        if len(self.UserCreditCard)>0:
#                              self.submitButton.config(state="normal")
                              ccnum=[]
                              for i in self.UserCreditCard:
                                    ccnum.append(i[0])

                              cc4num=[]

                              for i in ccnum:
                                    cc4num.append(i[12:])
                              self.variable = StringVar(self.frame44)
                              self.variable.set(cc4num[0])
                              w = OptionMenu(self.frame44,  self.variable,*cc4num)
                              w.grid(row=2,column=1)
                        else:
                              self.submitButton.config(state="disabled")
                                    

                        
                              
                              
                        

                  #self.location = StringVar(self.roomPage)
                  #self.location.set("Atlanta")
                  #cityList =  OptionMenu(frame1,self.location,"Atlanta", "Charlotte","Savannah", "Orlando", "Miami")
                  #cityList.grid(row=2,column=0)

                  addCardButton=Button(self.frame44, text='Add Card',command=self.paymentInfo)
                  
                  addCardButton.grid(row=2,column=2)
                  c.close()
                  db.commit()
                  db.close()

 #                 submitButton=Button(frame4, text='Submit')
 #                 submitButton.grid(row=3,column=3)
                  
                  
                  
            
                              



      def makeReservation(self):
            
            #if datetime.datetime.strptime(self.newSdateEntry.get(), '%Y/%m/%d')< datetime.datetime.strptime(self.newEdateEntry.get(), '%Y/%m/%d') and  now <= datetime.datetime.strptime(self.newSdateEntry.get(), '%Y/%m/%d'):
                  
                  

            
                  
                  #self.roomPage.withdraw()
                  
                  

                  db=self.connect()
                  if db is not None:
                        c=db.cursor()
                        location=str(self.location.get())
                        self.sdate=str(self.syear.get())+'/'+str(self.smonth.get())+'/'+str(self.sday.get())
                        self.edate=str(self.eyear.get())+'/'+str(self.emonth.get())+'/'+str(self.eday.get())
                        
                        try:
                              datetime.datetime.strptime(self.sdate, '%Y/%m/%d')
                              datetime.datetime.strptime(self.edate, '%Y/%m/%d')
                        except:
                              messagebox.showerror('Date Error', 'Not a valid Date')
                              self.roomPage.deiconify()
                              return
                        now=datetime.datetime.now()
                        if datetime.datetime.strptime(self.sdate, '%Y/%m/%d')< datetime.datetime.strptime(self.edate, '%Y/%m/%d') and  now.date() <= datetime.datetime.strptime(self.sdate, '%Y/%m/%d').date():
                                   
                              sql='SELECT * FROM ROOM WHERE Location =%s AND (Room_Num, Location) NOT IN (SELECT Room_Num, Location FROM RESERVES NATURAL JOIN RESERVATION  WHERE Cancel_Flag=0 AND ((Check_In_DATE < %s) AND  (Check_Out_DATE > %s)))'
                              n=c.execute(sql,(location,self.edate.replace('/',''),self.sdate.replace('/','')))
                              self.availableRoom=c.fetchall()
                              #print(alist)
                              self.reservationPage=Toplevel() ## Reservation Page
                              self.reservationPage.title("Make a Reservation")
                              frame1=Frame(self.reservationPage,relief=RAISED, borderwidth=2)
                              frame1.pack()
                              if n==0:
                                    Label(frame1, text='No available Room has been found').grid()
                              else:
                                    Label(frame1, text='Room Number ',relief=RAISED, borderwidth=1).grid(row=0,column=0)
                                    Label(frame1, text='Room Category ',relief=RAISED, borderwidth=1).grid(row=0,column=1)
                                    Label(frame1, text='#persons Allowed ',relief=RAISED, borderwidth=1).grid(row=0,column=2)
                                    Label(frame1, text='Cost per day ',relief=RAISED, borderwidth=1).grid(row=0,column=3)
                                    Label(frame1, text='cost of Extra Bed ',relief=RAISED, borderwidth=1).grid(row=0,column=4)
                                    Label(frame1, text='Select Room',relief=RAISED, borderwidth=1).grid(row=0,column=5)
                                    i=1
                                    self.vars=[]
             #                       self.v.set(1)
                        
                  ## two radio buttons for deposit and withrwa
      #                 rb1=Radiobutton(frame1,text='Withdraw',variable=self.v, value=1,bg='gray')
      #                 rb1.grid(row=3,column=0)

                                    for tup in self.availableRoom:
                                          self.v=IntVar()
                                          
                                          Label(frame1, text=str(tup[0])).grid(row=i,column=0)
                                          Label(frame1, text=str(tup[3])).grid(row=i,column=1)
                                          Label(frame1, text=str(tup[5])).grid(row=i,column=2)
                                          Label(frame1, text='$'+str(tup[2])).grid(row=i,column=3)
                                          Label(frame1, text='$'+str(tup[4])).grid(row=i,column=4)
                                          Checkbutton(frame1,text=str(i),variable=self.v).grid(row=i,column=5)
                                          self.vars.append(self.v)
                                          i=i+1
             #                             Label(frame1, text='Select Room').grid(row=i,column=5)
             
             
                                    
                                    Button(frame1,text='Check Details',command=self.reservationDetail).grid(row=i+1)
                        else:
                              messagebox.showerror('Date Error', 'Not a valid Date(s)')
                              

                        c.close()
                        db.commit()
                        db.close()
                        

            
      
      

            

            
            
            
                        
                  
      def toLogin2(self):
            ## to login window
            ## call when logout button is clicked
            self.place.destroy()##destroy
            
            self.win.deiconify()

      def rsvReport(self):
            try:
                  self.rsvReportPage.destroy()
            except:
                  pass
                  
            self.rsvReportPage=Toplevel()

            self.rsvReportPage.title('Reservation Report')

            frame1=Frame(self.rsvReportPage)
            frame1.grid(row=0,column=0,columnspan=3)

            Label(frame1, text='Month',relief=RAISED, borderwidth=1).grid(row=0, column=0)
            Label(frame1, text='Location',relief=RAISED, borderwidth=1).grid(row=0, column=1)
            Label(frame1, text='Total Number Of reservation',relief=RAISED, borderwidth=1).grid(row=0, column=2)

            db=self.connect()
            if db is not None:
                  c=db.cursor()
                  sql='SELECT Month(Check_In_Date) AS "Month", Location ,COUNT(*) AS "Total Number Of Reservations" FROM RESERVATION NATURAL JOIN RESERVES GROUP BY Month(Check_In_Date), Location ORDER BY Month(Check_In_Date), Location'
                  n=c.execute(sql)
                  report=c.fetchall()

                  #print(report)
                  

                  monthInbd=[]
                  if len(report)>0:
                        #print(report[0][0])
                        frameAug=Frame(self.rsvReportPage)
                        frameAug.grid(row=1,column=0)
 #                       Label(frame1, text='Nov').grid(row=1,column=0)

                        frameAug2=Frame(self.rsvReportPage)
                        frameAug2.grid(row=1,column=0)
                        j=1
                        Aug=0
                        Sep=0
                        Oct=0
                        Nov=0
                        Dec=0
                        Jan=0
                        
                        ##August
                        for i in report:
                              if Aug==0 and i[0]==8:
                                    Label(frame1, text='August').grid(row=j,column=0)
                              
                              if i[0]==8:
                                    Aug=1
                                    Label(frame1, text=i[1]).grid(row=j,column=1)
                                    Label(frame1, text=str(i[2])).grid(row=j,column=2)
                                    j=j+1
                              else:
                                    Aug=0
                        ##September

                        for i in report:
                              if Sep==0 and i[0]==9:
                                    Label(frame1, text='September').grid(row=j+1,column=0)
                                    Label(frame1, text='------------').grid(row=j,columnspan=3)
                                    
                              
                              if i[0]==9:
                                    Sep=1
                                    j=j+1
                                    Label(frame1, text=i[1]).grid(row=j,column=1)
                                    Label(frame1, text=str(i[2])).grid(row=j,column=2)
                                    j=j+1
                              else:
                                    Sep=0
                        ##October


                        for i in report:
                              if Oct==0 and i[0]==10:
                                    Label(frame1, text='October').grid(row=j+1,column=0)
                                    Label(frame1, text='------------').grid(row=j,columnspan=3)
                              
                              if i[0]==10:
                                    Oct=1
                                    j=j+1
                                    Label(frame1, text=i[1]).grid(row=j,column=1)
                                    Label(frame1, text=str(i[2])).grid(row=j,column=2)
                                    j=j+1
                              else:
                                    Oct=0
                        ##November

                        for i in report:
                              if Nov==0 and i[0]==11:
                                    Label(frame1, text='November').grid(row=j+1,column=0)
                                    Label(frame1, text='------------').grid(row=j,columnspan=3)
                              
                              if i[0]==11:
                                    Nov=1
                                    j=j+1
                                    Label(frame1, text=i[1]).grid(row=j,column=1)
                                    Label(frame1, text=str(i[2])).grid(row=j,column=2)
                                    j=j+1
                              else:
                                    Nov=0
                        ##December

                        for i in report:
                              if Dec==0 and i[0]==12:
                                    Label(frame1, text='December').grid(row=j+1,column=0)
                                    Label(frame1, text='------------').grid(row=j,columnspan=3)
                              
                              if i[0]==12:
                                    Dec=1
                                    j=j+1
                                    Label(frame1, text=i[1]).grid(row=j,column=1)
                                    Label(frame1, text=str(i[2])).grid(row=j,column=2)
                                    j=j+1
                              else:
                                    Dec=0

                        for i in report:
                              if Jan==0 and i[0]==1:
                                    Label(frame1, text='January').grid(row=j+1,column=0)
                                    Label(frame1, text='------------').grid(row=j,columnspan=3)
                              
                              if i[0]==1:
                                    Jan=1
                                    j=j+1
                                    Label(frame1, text=i[1]).grid(row=j,column=1)
                                    Label(frame1, text=str(i[2])).grid(row=j,column=2)
                                    j=j+1
                              else:
                                    Jan=0

                                    

                              
                              
                        
                  #print(n)

            
            
      def popRoom(self):
            try:
                  self.popRoomPage.destroy()
            except:
                  pass
                  
            self.popRoomPage=Toplevel()

            self.popRoomPage.title('Popular Room-Category')

            frame1=Frame(self.popRoomPage)
            frame1.grid(row=0,column=0,columnspan=3)

            Label(frame1, text='Month',relief=RAISED, borderwidth=1).grid(row=0, column=0)
            Label(frame1, text='Top Room-Category',relief=RAISED, borderwidth=1).grid(row=0, column=1)
            Label(frame1, text='Location',relief=RAISED, borderwidth=1).grid(row=0, column=2)
            Label(frame1, text='Total # of reservation/ cat',relief=RAISED, borderwidth=1).grid(row=0, column=3)

            db=self.connect()
            if db is not None:
                  c=db.cursor()
                  sql='SELECT month( Check_In_Date ) AS  "Month", Room_Category, Location,count(*) as "Total" FROM RESERVATION NATURAL JOIN ROOM NATURAL JOIN RESERVES where Month(`Check_In_Date`)=8 GROUP BY Room_Category, location ORDER BY Total DESC LIMIT 5'

                  
                  n=c.execute(sql)
                  report=c.fetchall()
                  

                  print(report)
                  

                  monthInbd=[]
                  if len(report)>0:
                        #print(report[0][0])
                        frameAug=Frame(self.popRoomPage)
                        frameAug.grid(row=1,column=0)
 #                       Label(frame1, text='Nov').grid(row=1,column=0)

                        frameAug2=Frame(self.popRoomPage)
                        frameAug2.grid(row=1,column=0)
                        j=1
                        Aug=0
                        Sep=0
                        Oct=0
                        Nov=0
                        Dec=0
                        Jan=0
                        
                        ##August
                        for i in report:
                              if Aug==0 and i[0]==8:
                                    Label(frame1, text='August').grid(row=j,column=0)
                              
                              if i[0]==8:
                                    Aug=1
                                    Label(frame1, text=i[1]).grid(row=j,column=1)
                                    Label(frame1, text=i[2]).grid(row=j,column=2)
                                    Label(frame1, text=str(i[3])).grid(row=j,column=3)
                                    
                                    j=j+1
                              else:
                                    Aug=0
                        ##September

                        for i in report:
                              if Sep==0 and i[0]==9:
                                    Label(frame1, text='September').grid(row=j+1,column=0)
                                    Label(frame1, text='------------').grid(row=j,columnspan=3)
                                    
                              
                              if i[0]==9:
                                    Sep=1
                                    j=j+1
                                    Label(frame1, text=i[1]).grid(row=j,column=1)
                                    Label(frame1, text=i[2]).grid(row=j,column=2)
                                    Label(frame1, text=str(i[3])).grid(row=j,column=3)
                                    j=j+1
                              else:
                                    Sep=0
                        ##October


                        for i in report:
                              if Oct==0 and i[0]==10:
                                    Label(frame1, text='October').grid(row=j+1,column=0)
                                    Label(frame1, text='------------').grid(row=j,columnspan=3)
                              
                              if i[0]==10:
                                    Oct=1
                                    j=j+1
                                    Label(frame1, text=i[1]).grid(row=j,column=1)
                                    Label(frame1, text=i[2]).grid(row=j,column=2)
                                    Label(frame1, text=str(i[3])).grid(row=j,column=3)
                                    j=j+1
                              else:
                                    Oct=0
                        ##November

                        for i in report:
                              if Nov==0 and i[0]==11:
                                    Label(frame1, text='November').grid(row=j+1,column=0)
                                    Label(frame1, text='------------').grid(row=j,columnspan=3)
                              
                              if i[0]==11:
                                    Nov=1
                                    j=j+1
                                    Label(frame1, text=i[1]).grid(row=j,column=1)
                                    Label(frame1, text=i[2]).grid(row=j,column=2)
                                    Label(frame1, text=str(i[3])).grid(row=j,column=3)
                                    j=j+1
                              else:
                                    Nov=0
                        ##December

                        for i in report:
                              if Dec==0 and i[0]==12:
                                    Label(frame1, text='December').grid(row=j+1,column=0)
                                    Label(frame1, text='------------').grid(row=j,columnspan=3)
                              
                              if i[0]==12:
                                    Dec=1
                                    j=j+1
                                    Label(frame1, text=i[1]).grid(row=j,column=1)
                                    Label(frame1, text=i[2]).grid(row=j,column=2)
                                    Label(frame1, text=str(i[3])).grid(row=j,column=3)
                                    j=j+1
                              else:
                                    Dec=0

                        for i in report:
                              if Jan==0 and i[0]==1:
                                    Label(frame1, text='January').grid(row=j+1,column=0)
                                    Label(frame1, text='------------').grid(row=j,columnspan=3)
                              
                              if i[0]==1:
                                    Jan=1
                                    j=j+1
                                    Label(frame1, text=i[1]).grid(row=j,column=1)
                                    Label(frame1, text=i[2]).grid(row=j,column=2)
                                    Label(frame1, text=str(i[3])).grid(row=j,column=3)
                                    j=j+1
                              else:
                                    Jan=0
      def revenueReport(self):
            try:
                  self.revenuePage.destroy()
            except:
                  pass
                  

            self.revenuePage=Toplevel()

            self.revenuePage.title('Revenue Report')

            frame1=Frame(self.revenuePage)
            frame1.grid(row=0,column=0,columnspan=3)

            Label(frame1, text='Month',relief=RAISED, borderwidth=1).grid(row=0, column=0)
            Label(frame1, text='Location',relief=RAISED, borderwidth=1).grid(row=0, column=1)
            Label(frame1, text='Revenue',relief=RAISED, borderwidth=1).grid(row=0, column=2)

            sql='SELECT Month(Check_In_Date), Location, Sum(Total_Cost) AS "Total Revenue of Reservations" FROM RESERVATION  NATURAL JOIN RESERVES  NATURAL JOIN ROOM GROUP BY Month(Check_In_Date), Location'

            db=self.connect()
            n=c=db.cursor()
            c.execute(sql)
            report=c.fetchall()
            #print(revenue)
            if len(report)>0:
                        #print(report[0][0])
                        #frameAug=Frame(self.rsvReportPage)
                        #frameAug.grid(row=1,column=0)
 #                       Label(frame1, text='Nov').grid(row=1,column=0)

 #                       frameAug2=Frame(self.rsvReportPage)
#                        frameAug2.grid(row=1,column=0)
                        j=1
                        Aug=0
                        Sep=0
                        Oct=0
                        Nov=0
                        Dec=0
                        Jan=0
                        
                        ##August
                        for i in report:
                              if Aug==0 and i[0]==8:
                                    Label(frame1, text='August').grid(row=j,column=0)
                              
                              if i[0]==8:
                                    Aug=1
                                    Label(frame1, text=i[1]).grid(row=j,column=1)
                                    Label(frame1, text=str(i[2])).grid(row=j,column=2)
                                    j=j+1
                              else:
                                    Aug=0
                        ##September

                        for i in report:
                              if Sep==0 and i[0]==9:
                                    Label(frame1, text='September').grid(row=j+1,column=0)
                                    Label(frame1, text='------------').grid(row=j,columnspan=3)
                                    
                              
                              if i[0]==9:
                                    Sep=1
                                    j=j+1
                                    Label(frame1, text=i[1]).grid(row=j,column=1)
                                    Label(frame1, text=str(i[2])).grid(row=j,column=2)
                                    j=j+1
                              else:
                                    Sep=0
                        ##October


                        for i in report:
                              if Oct==0 and i[0]==10:
                                    Label(frame1, text='October').grid(row=j+1,column=0)
                                    Label(frame1, text='------------').grid(row=j,columnspan=3)
                              
                              if i[0]==10:
                                    Oct=1
                                    j=j+1
                                    Label(frame1, text=i[1]).grid(row=j,column=1)
                                    Label(frame1, text=str(i[2])).grid(row=j,column=2)
                                    j=j+1
                              else:
                                    Oct=0
                        ##November

                        for i in report:
                              if Nov==0 and i[0]==11:
                                    Label(frame1, text='November').grid(row=j+1,column=0)
                                    Label(frame1, text='------------').grid(row=j,columnspan=3)
                              
                              if i[0]==11:
                                    Nov=1
                                    j=j+1
                                    Label(frame1, text=i[1]).grid(row=j,column=1)
                                    Label(frame1, text=str(i[2])).grid(row=j,column=2)
                                    j=j+1
                              else:
                                    Nov=0
                        ##December

                        for i in report:
                              if Dec==0 and i[0]==12:
                                    Label(frame1, text='December').grid(row=j+1,column=0)
                                    Label(frame1, text='------------').grid(row=j,columnspan=3)
                              
                              if i[0]==12:
                                    Dec=1
                                    j=j+1
                                    Label(frame1, text=i[1]).grid(row=j,column=1)
                                    Label(frame1, text=str(i[2])).grid(row=j,column=2)
                                    j=j+1
                              else:
                                    Dec=0

                        for i in report:
                              if Jan==0 and i[0]==1:
                                    Label(frame1, text='January').grid(row=j+1,column=0)
                                    Label(frame1, text='------------').grid(row=j,columnspan=3)
                              
                              if i[0]==1:
                                    Jan=1
                                    j=j+1
                                    Label(frame1, text=i[1]).grid(row=j,column=1)
                                    Label(frame1, text=str(i[2])).grid(row=j,column=2)
                                    j=j+1
                              else:
                                    Jan=0


            

                                    
            
      def Manafunctionality(self):
            self.win.withdraw()
            self.manaPage=Toplevel()##toplevel
            self.manaPage.geometry("400x400")
            
            self.manaPage.title("Choose Functionality")
            frame1=Frame(self.manaPage,relief=SUNKEN,bg='gray')
            frame1.pack(fill=BOTH, expand=1)
            label11=Label(frame1,text='Welcome!',bg='gray')

      
            label11.pack(fill=BOTH, expand=1)
            ## balance label
            ttk.Style().configure('green/black.TButton', foreground='blue', background='gray')

#                 self.balance=float(UserInfo[-1])
            
            b1=ttk.Button(frame1, text='View reservation Report',style='green/black.TButton',command=self.rsvReport)
            b1.pack(fill=BOTH, expand=1)

            #Label(frame1,text='',bg='gray').pack(fill=BOTH, expand=1)

            b2=ttk.Button(frame1, text='View Popular room catecogryReport',style='green/black.TButton',command=self.popRoom)
            b2.pack(fill=BOTH, expand=1)

#                 Label(frame1,text='',bg='gray').pack(fill=BOTH, expand=1)

            b3=ttk.Button(frame1, text='View Revenue Report',style='green/black.TButton', command=self.revenueReport)
            b3.pack(fill=BOTH, expand=1)


      def insertRev(self):
            #print(self.comment.get(1.0, END))
            #print(type(self.comment.get(1.0, END)))
            db=self.connect()
            c=db.cursor()
            
            sql='INSERT INTO REVIEW (Location, Rating, Comment, Cust_Username) VALUES (%s, %s, %s,%s)'

            c.execute(sql,(self.locationRev.get(),self.ratingRev.get(),self.comment.get(1.0, END),self.username))
            messagebox.showinfo('Sucess',' Thanks for your feedback')

            c.close()
            db.commit()
            db.close()
            
                      
                  

      def provideRev(self):
            self.provideRevPage=Toplevel()
            frame1=Frame(self.provideRevPage,relief=RAISED, borderwidth=1)
            frame1.pack()
            Label(frame1, text='Hotel Location').grid(row=0,column=0)
            self.locationRev = StringVar(self.provideRevPage)
            self.locationRev.set("Atlanta")
            cityList =  OptionMenu(frame1,self.locationRev,"Atlanta", "Charlotte","Savannah", "Orlando", "Miami")
            cityList.grid(row=0,column=1)

            Label(frame1, text='Rating').grid(row=1,column=0)
            self.ratingRev = StringVar(self.provideRevPage)
            self.ratingRev.set("Excellent")
            cityList =  OptionMenu(frame1,self.ratingRev,"Excellent","Good", "Bad", "Very Bad","Neutral")
            cityList.grid(row=1,column=1)

            self.comment=Text(frame1,width=50,height=10, relief=SUNKEN, borderwidth=1)
            self.comment.grid(row=2,columnspan=2)
 #           comment.geometry("70*70")
            


            Button(frame1, text='Submit' ,command=self.insertRev).grid(row=5)
            
            
      def getRev(self):
            frame2=Frame(self.viewPage,relief=RAISED, borderwidth=1)
            frame2.pack()
            sql='SELECT Rating, Comment FROM REVIEW WHERE Location =%s ORDER BY Rating'

            db=self.connect()
            

            if db is not None:
                  c=db.cursor()

                  c.execute(sql,self.locationRev.get())
                  allrev=c.fetchall()
                  
                  i=0
                  e=0
                  g=0
                  n=0
                  b=0
                  vb=0
                  #print(allrev)

                  if len(allrev)>0:

                        for tup in allrev:
                              

                         
                        
                              if tup[0]=='Excellent':
                                    if e==0:
                                          Label(frame2,text='Excellent').grid(row=i,column=0)
                                    #else:
                                          e=1
            
                                    Label(frame2,text= tup[1]).grid(row=i,column=1)
                                    i=i+1
                        i=i+1


                        for tup in allrev:

                         
                        
                              if tup[0]=='Good':
                                    if g==0:
                                          Label(frame2,text='Good').grid(row=i,column=0)
                                    #else:
                                          g=1
            
                                    Label(frame2,text= tup[1]).grid(row=i,column=1)
                                    i=i+1
                        i=i+1


                        for tup in allrev:

                         
                        
                              if tup[0]=='Neutral':
                                    if n==0:
                                          Label(frame2,text='Neutral').grid(row=i,column=0)
                                   # else:
                                          n=1
            
                                    Label(frame2,text= tup[1]).grid(row=i,column=1)
                                    i=i+1
                        i=i+1

                        for tup in allrev:

                         
                        
                              if tup[0]=='Bad':
                                    if b==0:
                                          Label(frame2,text='Bad').grid(row=i,column=0)
                                   # else:
                                          b=1
            
                                    Label(frame2,text= tup[1]).grid(row=i,column=1)
                                    i=i+1
                        i=i+1

                        for tup in allrev:

                         
                        
                              if tup[0]=='Very Bad':
                                    if vb==0:
                                          Label(frame2,text='Very Bad').grid(row=i,column=0)
                                    #else:
                                          vb=1
            
                                    Label(frame2,text= tup[1]).grid(row=i,column=1)
                                    i=i+1
                        i=i+1
                  

            #pass
            
                  
      def viewReview(self):
            self.viewPage=Toplevel()
            frame1=Frame(self.viewPage,relief=RAISED, borderwidth=1)
            frame1.pack()
            Label(frame1, text='Hotel Location').grid(row=0,column=0)
            self.locationRev = StringVar(self.viewPage)
            self.locationRev.set("Atlanta")
            cityList =  OptionMenu(frame1,self.locationRev,"Atlanta", "Charlotte","Savannah", "Orlando", "Miami")
            cityList.grid(row=0,column=1)

            Button(frame1, text='Check Review' ,command=self.getRev).grid(row=1)

            frame2=Frame(self.viewPage,relief=RAISED, borderwidth=1)
            frame2.pack()

      def Custfunctionality(self):
            try:
                  self.reservationPage.destroy()
                  self.ConfirmScreen.destroy()
                  self.roomPage.destroy()
            except:
                  pass
            ##Market place GUI
            self.win.withdraw()
 
            self.place=Toplevel()##toplevel
            self.place.geometry("400x400")
            
            self.place.title("Choose Functionality")
            
            db=self.connect()
            if db is not None:
                  #Get the full name of the User who logged in
                  c=db.cursor()
                  c.execute('SELECT * FROM CUSTOMER WHERE Username=%s AND Password=%s',(self.username,self.password))
                  UserInfo=c.fetchone()
                  ##print(UserInfo)
                  ## welcome frame
                  frame1=Frame(self.place,relief=SUNKEN,bg='gray')
                  frame1.pack(fill=BOTH, expand=1)
                  frame2=Frame(self.place,relief=SUNKEN,bg='gray')
                  frame2.pack()
                  if UserInfo[0]==None:
                        label11=Label(frame1,text='Welcome!',bg='gray')
                  else:
                        label11=Label(frame1,text='Welcome, '+UserInfo[2] ,bg='gray')


                  label11.pack(fill=BOTH, expand=1)
                  ## balance label
                  ttk.Style().configure('green/black.TButton', foreground='blue', background='gray')

 #                 self.balance=float(UserInfo[-1])
                  
                  b1=ttk.Button(frame1, text='Make a new reservation',style='green/black.TButton',command=self.searchRoom)
                  b1.pack(fill=BOTH, expand=1)

                  #Label(frame1,text='',bg='gray').pack(fill=BOTH, expand=1)

                  b2=ttk.Button(frame1, text='Update your Reservation',style='green/black.TButton',command=self.updateReservation)
                  b2.pack(fill=BOTH, expand=1)

 #                 Label(frame1,text='',bg='gray').pack(fill=BOTH, expand=1)

                  b3=ttk.Button(frame1, text='Cancel your Reservation',style='green/black.TButton',command=self.cancelReservation)
                  b3.pack(fill=BOTH, expand=1)

 #                 Label(frame1,text='',bg='gray').pack(fill=BOTH, expand=1)

                  b4=ttk.Button(frame1, text='Provide feedback',style='green/black.TButton', command=self.provideRev)
                  b4.pack(fill=BOTH, expand=1)

 #                 Label(frame1,text='',bg='gray').pack(fill=BOTH, expand=1)

                  b5=ttk.Button(frame1, text='View Feedback',style='green/black.TButton',command=self.viewReview)
                  b5.pack(fill=BOTH, expand=1)
                  

                  

                  
                  

                  

     
                  

                  self.v=IntVar()
                  self.v.set(9)
                  
                  ## two radio buttons for deposit and withrwa
 #                 rb1=Radiobutton(frame1,text='Withdraw',variable=self.v, value=1,bg='gray')
 #                 rb1.grid(row=3,column=0)

 #                 rb2=Radiobutton(frame1,text='Deposit',variable=self.v, value=2,bg='gray')
 #                 rb2.grid(row=3,column=1)

 
                  ##frame2 entry widget, button sand labels

 
                  
                  ##frame3 entry widget, button sand labels

                  bLogout=Button(frame2, text='Logout',command=self.toLogin2,bg='gray')
                  bLogout.grid(row=0,column=0, sticky=E+W)

 #                 bStat=Button(frame2, text='Statistics',command=self.Statistics)
 #                 bStat.grid(row=0,column=1, sticky=W)

                  c.close()
                  db.commit()
                  db.close()
                

      def toLogin(self):
            ##this function control the switching between the two main Wndow
            ##return None
            ## called when cancel button has been clicked on the register window and
            
            self.top.destroy()##destroy
            
      
            
            self.win.deiconify()##make the Login main window reapper again
      def registerCheck(self):
            ## This function register new user into the data base if sufficient condition are met
            ##Return None
            ##Is called when Register Button of the top level is clicked
            db=self.connect()## pymysql object return by self.connect function
            if db is not None:
                  c=db.cursor()## c as cursor object 
                  First_Name=self.EntryRegister1.get()## gets text within the full Name entry box
                  Last_Name=self.EntryRegister2.get()# gets text within the Username entrybox
                  Username=self.EntryRegister3.get()## typed email

                  passwd=self.EntryRegister4.get()##password typed the entry box labeled password
                  confirmedPasswd=self.EntryRegister5.get()## typed confirmed password
                  Email=self.EntryRegister6.get()## typed email

                  ##Checks if the user name is nor used already
                  ## return an integer
                  n=c.execute('SELECT * FROM CUSTOMER WHERE Username=%s', (Username))
                  n2=c.execute('SELECT * FROM CUSTOMER WHERE Email=%s', (Email))
                  #print(n,n2)
                  ok=0##setting variable ok to something( can be anything)
                  if not re.match(r"[^@]+@[^@]+\.[^@]+", Email):
                        messagebox.showerror('Error!!', 'Email not valid')
                        return
                        
                        

                  for i in passwd:
                        if i in '0123456789' and len(passwd)>=5 :#checking if their is digit inside the password
                              ok=1
                  
                  #checking if all condition have been met
                  if Last_Name!='' and First_Name!='' and n==0 and ok==1 and n2==0  and passwd==confirmedPasswd:
                        #if yes create a new user with new regard in the table inside the database
                        c.execute('INSERT INTO CUSTOMER (First_Name,Last_Name, Username, Password, Email) VALUES (%s,%s,%s,%s,%s)',(First_Name,Last_Name,Username,passwd,Email))
                        R=messagebox.showinfo('Sucess',' You are sucessfully registed now')
                        # and display a success notification
                        if R=='ok':
                              self.toLogin()
                              #call toLogin if ok of the message box has been clicked
                  ##checking if all condition has been met without be given a full name
                  
##                  elif fullName==''and n==0 and ok==1 and passwd==confirmedPasswd:
##                        ##do the exact same thing as the abobe if statement
##                        #with diferent condition
##
##
##                        
##                        #null=None
##                        c.execute('INSERT INTO CUSTOMER (Fullname,Username, Password, Balance) VALUES (%s,%s,%s,%s)',(None,username,passwd,50))
##                        R=messagebox.showinfo('Sucess',' You are sucessfully registed now')
##                        if R=='ok':
##                              self.toLogin()
                  
                  else:
                        #if conditions not met Display error message
                        messagebox.showerror('Error!!', 'Requirments not met')##if 
                        
                  c.close()# close cursor object
                  db.commit()# saves changes made within the data base
                  db.close()# clase the pymysql object
                  

      def toRegister(self):
            ## this function create a Toplevel of the Register window
            ## return None
            ## is called when Register button of LOGIN page is cliked
            self.win.withdraw()# hide the main login window
            self.top=Toplevel()## Top levelwindow
            self.top.title('FANCY HOTEL Register Page')##setting title
            f=Frame(self.top,bg='gray')#creating a frame that with backgroud colored gray
            f.pack(expand=True, fill='both')
            try:
                  
                  label = Label(f, image=self.image,bg='gray')
                  label.grid(row=0,column=0,columnspan=2,padx=5,sticky=W)
            except:
                  pass
            
            ##First Name name label and entry widget
            label1=Label(f,text='Firt Name:',bg='gray')# label Text
            label1.grid(row=1 ,column=0, sticky=E)

            self.EntryRegister1=Entry(f,width=30,highlightbackground='gray')# entry widget
            self.EntryRegister1.grid(row=1, column=1,sticky=W,padx=5, pady=5)

            ##lAST NAME name label and entry widget
            label1=Label(f,text='Last Name:',bg='gray')# label Text
            label1.grid(row=2 ,column=0, sticky=E)

            self.EntryRegister2=Entry(f,width=30,highlightbackground='gray')# entry widget
            self.EntryRegister2.grid(row=2, column=1,sticky=W,padx=5, pady=5)
            
            ##Username label and entry widget
            label2=Label(f,text='Username:',bg='gray')# label Text
            label2.grid(row=3 ,column=0, sticky=E)
            self.EntryRegister3=Entry(f,width=30,highlightbackground='gray')# entry widget
            self.EntryRegister3.grid(row=3, column=1,sticky=W,padx=5, pady=5)
            
            ##Password label and entry widget
            label3=Label(f,text='Password:',bg='gray')# label Text
            label3.grid(row=4 ,column=0, sticky=E)
            self.EntryRegister4=Entry(f,width=30,highlightbackground='gray')# entry widget
            self.EntryRegister4.grid(row=4, column=1,sticky=W,padx=5, pady=5)
            
            ## Confirmed Password label and entry widget
            label4=Label(f,text='Confirm Password:',bg='gray')#label
            label4.grid(row=5 ,column=0, sticky=E)
            self.EntryRegister5=Entry(f,width=30,highlightbackground='gray')# entry widget
            self.EntryRegister5.grid(row=5, column=1,sticky=W,padx=5, pady=5)

            ## Email
            label4=Label(f,text='Email:',bg='gray')#label
            label4.grid(row=6 ,column=0, sticky=E)
            self.EntryRegister6=Entry(f,width=30,highlightbackground='gray')# entry widget
            self.EntryRegister6.grid(row=6, column=1,sticky=W,padx=5, pady=5)

            ##Bottons frame 
            f2= Frame(f,relief=RAISED)#frame
            f2.grid(row=7,column=0,columnspan=3,sticky=E+W)# Layout

            button2=Button(f2,text='Register',bg='grey',command=self.registerCheck)#Register Button
            button2.pack(side=RIGHT)#pack Layout 
                  
            button1=Button(f2,text='Cancel',bg='grey',command=self.toLogin)##Cancel Button
            button1.pack(side=RIGHT)
                  

      
            
      
      def __init__(self,rootin):
                  ## Main Login window define in this window
                  ## Init function
                  ## return None
                  self.win=rootin##TK OBJECT
                  self.win.title('Fancy HOTEL Login Page')##main page title
                  self.win.geometry("400x400")
                  f=Frame(self.win,bg="gray")# frame
                  f.pack(fill=BOTH, expand=1)
                  try:
                  ## downloading Gatech logo from the link below
                        u = urllib.request.urlopen("http://www.montsemorales.com/images/Places2eso/hotel.gif")
                        img = u.read()# data read
                        u.close()
                        
                        dataB = base64.encodebytes(img)# image data processing
                        self.image = PhotoImage(data=dataB)# image data processing
                        label = Label(f, image=self.image,bg='gray')# inserting the image in the window
                        label.grid(row=0,column=1,columnspan=3,sticky=W+E,padx=5)
                  except:
                        pass

                  ##Username label and entry widget

                  label1=Label(f,text='Username:',bg='gray')# Label
                  label1.grid(row=1 ,column=0, sticky=E+W)
                  

                  self.EntryLoginUser=Entry(f,width=30,highlightbackground='gray')# entry Widget
                  self.EntryLoginUser.grid(row=1, column=1,sticky=E,padx=5, pady=5,columnspan=2)

                  
                  ##Password label and entry widget
                  label2=Label(f,text='Password:',bg='gray')
                  label2.grid(row=2 ,column=0, sticky=E)

                  self.EntryLoginPass=Entry(f,width=30,highlightbackground='gray')
                  self.EntryLoginPass.grid(row=2, column=1,sticky=W,padx=5, pady=5)
                  
                  f2= Frame(self.win, bg='gray')
                  f2.pack(fill=BOTH, expand=1)

                  #Buttons 

                  button2=Button(f2,text='Login',command=self.loginCheck)# Login Button
                  button2.grid(row=1,column=1 ,sticky=W+E)##Pack right
                  
                  button1=Button(f2,text='Register',command=self.toRegister)# Register Button
                  button1.grid(row=1,column=2)## pack right
                  





root=Tk()
t=GUI(root)

root.mainloop()

      

