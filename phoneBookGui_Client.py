# @Author: Atul Sahay <atul>
# @Date:   2018-08-22T20:05:54+05:30
# @Email:  atulsahay01@gmail.com
# @Filename: phoneBook.py
# @Last modified by:   atul
# @Last modified time: 2018-08-24T20:35:17+05:30

from tkinter import *
from tkinter import messagebox
import datetime
import re
import xmlrpc.client



now = datetime.datetime.now()

class phoneBook:
    select = None
    scroll = None
    root = None
    viewList = []
    phoneList = ['0010-9934809648','1010-7003045517','1234-8282926697','1234-6394947263']
    nameList  = ['Atul Sahay','Aman Sahay','Aanchal Sahay','Pratima Sahay']
    dobList   = ['28-05-1996','13-05-1998','28-05-1996','13-05-1998']
    emailList = ['atulsahay01@gmail.com','sahayaman45@gmail.com','atulsahay01@gmail.com','sahayaman45@gmail.com']
    addList   = ['njudijvadskmkmskma','basjdcjadsjnjsc','njudijvadskmkmskma','basjdcjadsjnjsc']
    cityList  = ['Mumbai','New Delhi','Mumbai','New Delhi']
    zipList   = ['800023','800023','800023','800023']
    conn = None
    refresh = None
    def __init__(self):
        self.dbConnect()
        self.root = self.make_window()
        self.root.mainloop()
    def make_window(self):
        win = Tk()
        win.title("Phone Book")
        win.resizable(False, False)
        frame1 = Frame(win)       # Row of buttons
        frame1.pack()
        b1 = Button(frame1, text=" Add  ", command=self.add_entry)
        b1.grid(row=0, column=0, padx=50, pady=10)
        b2 = Button(frame1, text=" Search ", command=self.search_entry)
        b2.grid(row=0, column=1, padx=10, pady=10)
        # b3 = Button(frame2, text="Delete", command=delete_entry)
        # b4 = Button(frame2, text="Load  ", command=load_entry)
        # b5 = Button(frame2, text="Refresh", command=set_select)
        # b1.pack()
        # b2.pack()
        # b3.pack(side=LEFT)
        # b4.pack(side=LEFT)
        # b5.pack(side=LEFT)
        frame2 = Frame(win,padx=10, pady=10)
        frame2.pack(side=RIGHT)
        b3 = Button(frame2, text=" Edit  ", command=self.edit_entry)
        b3.grid(row=0, column=0, padx=10, pady=10)
        b4 = Button(frame2, text=" Delete ", command=self.delete_entry)
        b4.grid(row=1, column=0, padx=10, pady=10)
        self.refresh = Button(frame2, text="Back To Main", command=self.refresh)
        self.refresh.grid(row=2, column=0, padx=10, pady=10)
        self.refresh.grid_forget()
        # refresh.configure(state = DISABLED, disabledforeground = frame2.cget('bg'))
        # b3.pack(side=TOP)
        # b4.pack(side=TOP)

        frame3 = Frame(win,padx=10, pady=10)       # select of names
        frame3.pack(side=LEFT)
        self.scroll = Scrollbar(frame3, orient=VERTICAL)
        self.select = Listbox(frame3,font = 'Courier', width=50, selectmode='multiple', yscrollcommand=self.scroll.set, height=10)
        self.scroll.config(command=self.select.yview)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.select.pack(side=LEFT, fill=BOTH, expand=True)
        data = self.conn.SELECTALL()

        # for i in data:
        #     print(i)
        self.phoneList = []
        self.nameList  = []
        self.dobList   = []
        self.emailList = []
        self.addList   = []
        self.cityList  = []
        self.zipList   = []
        for i in range(len(data)):
            self.phoneList.append(data[i][1])
            self.nameList.append(data[i][0])
            self.dobList.append(data[i][6])
            self.emailList.append(data[i][4])
            self.addList.append(data[i][2])
            self.cityList.append(data[i][3])
            self.zipList.append(data[i][5])
        self.select.delete(0,END)
        for i in range(len(self.phoneList)):
            self.select.insert("end", "{0} {1}".format(self.tabify(self.nameList[i]), self.phoneList[i]))


        ####################### List Selection ###############
        self.select.bind("<<ListboxSelect>>", self.onSelect)
        self.select.event_generate("<<ListboxSelect>>")

        return win
    def refresh(self):
        self.viewList = []
        self.refresh.grid_forget()
        self.select.delete(0,END)
        for i in range(len(self.phoneList)):
            self.select.insert("end", "{0} {1}".format(self.tabify(self.nameList[i]), self.phoneList[i]))

    def onSelect(self,event):
        a = event.widget.curselection()
        curr = set(list(a)) - set(self.viewList)
        curr = list(curr)
        # print("a ",a)
        # print("current ",curr)
        # print("viewList ",self.viewList)
        if(len(a)==0):
            self.viewList = list(a)
        if(len(curr)==0):
            self.viewList = list(a)
        elif(curr[0] not in self.viewList):
            c = self.select.get(curr[0])[-15:]
            self.viewList.append(curr[0])
            for i in range(len(self.phoneList)):
                if(self.phoneList[i] == c):
                    c = i
                    break
            self.showDetails(c)
        else:
            self.viewList = list(a)
        # print("UUUviewList ",self.viewList)
    def showDetails(self,index):
        # create child window
        win = Toplevel()
        win.title("Address Details")
        win.resizable(False, False)
        # create labels and entry
        nameLabel = Label(win, text="Name")
        nameEntry = Entry(win)
        nameEntry.delete(0, END)
        nameLabel.grid(row=0,column=0,padx=5,pady=5)
        nameEntry.grid(row=0,column=1,padx=5,pady=5)
        nameEntry.insert(0,self.nameList[index])
        nameEntry.configure(state='disabled')

        dobLabel = Label(win, text="D.O.B")
        dobEntry = Entry(win,text="28-05-1996")
        dobEntry.delete(0, END)
        dobEntry.insert(0,self.dobList[index])
        dobLabel.grid(row=1,column=0,padx=5,pady=5)
        dobEntry.grid(row=1,column=1,padx=5,pady=5)
        dobEntry.configure(state='disabled')

        phLabel = Label(win, text="Phone No.")
        ccEntry = Entry(win,text="0123",width=4)
        ccEntry.delete(0, END)
        ccEntry.insert(0,self.phoneList[index][:4])
        # _Label = Label(win,text="-",width=1)
        phEntry = Entry(win,text="1234567890")
        phEntry.delete(0, END)
        phEntry.insert(0,self.phoneList[index][5:])
        phLabel.grid(row=2,column=0,padx=5,pady=5)
        ccEntry.grid(row=2,column=1,padx=5,pady=5)
        # _Label.grid(row=2,column=2)
        phEntry.grid(row=2,column =2,padx=2,pady=5)
        ccEntry.configure(state='disabled')
        phEntry.configure(state='disabled')

        emailLabel = Label(win, text="Email Id")
        emailEntry = Entry(win,text="abc@xyz.com")
        emailEntry.delete(0, END)
        emailEntry.insert(0,self.emailList[index])
        emailLabel.grid(row=3,column=0,padx=5,pady=5)
        emailEntry.grid(row=3,column=1,padx=5,pady=5)
        emailEntry.configure(state='disabled')

        addressLabel = Label(win, text=">>>>>>>>>Address Details<<<<<<<<<<<")
        addressLabel.grid(row=4,columnspan=4,padx=5,pady=5)
        # Create a Tkinter variable
        cityVar = StringVar(win)

        # Dictionary with options
        choices = {'Ahmedabad', 'Aurangabad', 'Mumbai', 'New Delhi', 'Bengaluru', 'Hyderabad', 'Shillong', 'Leh', 'Kochi', 'Port Blair'}
        cityVar.set(self.cityList[index]) # set the default option

        popupMenu = OptionMenu(win, cityVar, *choices)
        Label(win, text="City Name").grid(row = 5, column = 0)
        popupMenu.grid(row = 5, column =1)
        popupMenu.configure(state='disabled')

        addressEntry = Text(win,height=2,width=60)
        addressEntry.delete(1.0, END)
        addressEntry.insert(1.0,self.addList[index])
        addressEntry.grid(rowspan=3,columnspan=4,ipady=1,padx=5,pady=5)
        addressEntry.configure(state='disabled')
        zipLabel = Label(win, text="Zip")
        zipLabel.grid(row=9,column=0,padx=5,pady=5)

        zipEntry = Entry(win,text="800023")
        zipEntry.delete(0, END)
        zipEntry.insert(0,self.zipList[index])
        zipEntry.grid(row=9,column=1,padx=5,pady=5)
        zipEntry.configure(state='disabled')

        # quit child window and return to root window
        # the button is optional here, simply use the corner x of the child window
        Button(win, text=' Ok ', command=win.destroy).grid(row=10,columnspan = 4,padx=10,pady=5)
        # We need bind a window can be killed by many ways
        win.bind("<Destroy>",lambda x:self.root.deiconify())

    def dbConnect(self):
        self.conn = xmlrpc.client.ServerProxy('http://localhost:1830')

    def tabify(self,s, tabsize = 4):
        num = 0
        for i in self.nameList:
            if(len(i)>num):
                num = len(i)
        c = num - len(s)
        ln = ((len(str(s))/int(tabsize))+1)*tabsize
        return s.ljust(int(ln)+c)
    def add_entry(self):
        self.viewList = []
        self.refresh.grid_forget()
        self.root.withdraw()
        self.addItemWindow()

    def search_entry(self):
        self.viewList = []
        self.refresh.grid(row=2,column=0,padx=10,pady=10)
        self.root.withdraw()
        self.searchItemWindow()
    def edit_entry(self):
        self.viewList = []
        self.refresh.grid_forget()
        l = self.which_selected()
        if(len(l)>1):
            messagebox.showwarning('Warning', 'Too Many Selection')
            return
        if(len(l)==0):
            return
        self.root.withdraw()
        # print(self.select.get(l[0])[-15:])
        c = self.select.get(l[0])[-15:]
        for i in range(len(self.phoneList)):
            if(self.phoneList[i] == c):
                c = i
                break
        # print(c)
        self.editItemWindow(c)
    def delete_entry(self):
        self.viewList = []
        self.refresh.grid_forget()
        l = self.which_selected()
        a = []
        for j in range(len(l)):
            c = self.select.get(l[j])[-15:]
            for i in range(len(self.phoneList)):
                if(self.phoneList[i] == c):
                    c = i
                    break
            a.append(c)
        l = a
        if(len(l)==0):
            return
        phList = []
        for i in l:
            phList.append(self.phoneList[i])
        # print(phList)
        self.conn.DELETEENTRY(phList)
        self.nameList = self.updateList(self.nameList,l)
        self.phoneList = self.updateList(self.phoneList,l)
        self.cityList = self.updateList(self.cityList,l)
        self.addList = self.updateList(self.addList,l)
        self.emailList = self.updateList(self.emailList,l)
        self.zipList = self.updateList(self.zipList,l)
        self.dobList = self.updateList(self.dobList,l)
        self.select.delete(0,END)

        for i in range(len(self.phoneList)):
            self.select.insert("end", "{0} {1}".format(self.tabify(self.nameList[i]), self.phoneList[i]))

    def updateList(self,toUpdate,indices):
        a = []
        for i in range(len(toUpdate)):
            if(i not in indices):
                a.append(toUpdate[i])
        return a
    def which_selected(self):
        # print("At {0}".format(self.select.curselection()))
        return (self.select.curselection()[:])

    def addItemWindow(self):
        # Inside helping functions
        self.viewList = []
        def destroy():
            error = False
            nameVar = nameEntry.get()
            if(nameVar == "ABC"):
                nameVar = ""
            dobVar  = dobEntry.get()
            if(dobVar == "DD-MM-YYYY"):
                dobVar = ""
            ccVar  = ccEntry.get()
            if(ccVar == "0123"):
                ccVar = ""
            phVar  = phEntry.get()
            if(phVar == "1234567890"):
                phVar = ""
            emailVar  = emailEntry.get()
            if(emailVar == "abc@xyz.com"):
                emailVar = ""
            cityvar = cityVar.get()
            addVar  = addressEntry.get(1.0,END)
            zipVar  = zipEntry.get()
            if(zipVar == "123456"):
                zipVar = ""
            if(len(phVar)!=10 or phVar[0]=="0" or not phVar.isdigit()):
                messagebox.showwarning('Warning', 'Invalid Phone Number')
                phVar=""
                error = True
            elif(len(ccVar)!=4 or not ccVar.isdigit()):
                messagebox.showwarning('Warning', 'Invalid Country Code')
                ccVar=""
                error = True
            elif(len(zipVar)>0 and (len(zipVar)!=6 or zipVar[0]=="0" or not zipVar.isdigit())):
                messagebox.showwarning('Warning', 'Invalid Zip Code')
                zipEntry.delete(0,END)
                zipEntry.focus_set()
                error = True

            year  = now.year
            month = now.month
            day   = now.day

            if(len(emailVar)>0 and not isValidEmail(emailVar)):
                emailVar = ""
                messagebox.showwarning('Warning', 'Invalid Email')
                emailEntry.focus_set()
                emailEntry.delete(0,END)
                error = True

            if(len(dobVar)>0):
                a = dobVar.split("-")
                if(len(a)!=3 or not a[0].isdigit() or not a[1].isdigit() or not a[2].isdigit() or int(a[0])>31 or int(a[1])>12 or int(a[2])<=0):
                    messagebox.showwarning('Warning', 'DOB is invalid')
                    dobEntry.delete(0,END)
                    dobEntry.focus_set()
                    dobEntry.insert(0,"DD-MM-YYYY")
                    error = True
                else:
                    year  = int(year)  - int(a[2])
                    month = int(month) - int(a[1])
                    day   = int(day)   - int(a[0])
                    if(year>10):
                        pass
                    elif(year==10 and month>=0 and day>=0):
                        pass
                    else:
                        messagebox.showwarning('Warning', 'Not Above 10')
                        dobVar = ""
                        error = True
            if((ccVar+'-'+phVar) in self.phoneList):
                messagebox.showwarning('Warning', 'Number Already exists')
                phVar=""
                error = True
            if(len(nameVar)==0):
                nameEntry.focus_set()
                nameEntry.delete(0,END)
            elif(len(dobVar)==0):
                dobEntry.focus_set()
                dobEntry.delete(0,END)
            elif(len(ccVar)==0):
                ccEntry.focus_set()
                ccEntry.delete(0,END)
            elif(len(phVar)==0):
                phEntry.focus_set()
                phEntry.delete(0,END)
            elif(error):
                pass
            else:
                self.phoneList.append(ccVar+'-'+phVar)
                self.nameList.append(nameVar)
                self.dobList.append(dobVar)
                self.emailList.append(emailVar)
                self.addList.append(addVar)
                self.cityList.append(cityvar)
                self.zipList.append(zipVar)
                data = [[self.nameList[-1]],[self.phoneList[-1]], [self.addList[-1]], [self.cityList[-1]], [self.emailList[-1]], [self.zipList[-1]], [self.dobList[-1]]]
                # print(data)
                self.conn.INSERT(data)
                self.select.delete(0,END)
                for i in range(len(self.phoneList)):
                    self.select.insert("end", "{0} {1}".format(self.tabify(self.nameList[i]), self.phoneList[i]))
                win.destroy()

        def clear(self):
            # print(self.widget)
            if(str(self.widget)[-4:]!="text"):
                self.widget.delete(0,END)
            else:
                self.widget.delete(1.0,END)
        def isValidEmail(email):
            if(re.match(r'[\w\.-]+@[\w\.-]+',string=email)!= None):
                return True
            return False
        # create child window
        win = Toplevel()
        win.title("Add")
        win.resizable(False, False)
        # create labels and entry
        nameLabel = Label(win, text="Name")
        nameEntry = Entry(win)
        nameEntry.delete(0, END)
        nameLabel.grid(row=0,column=0,padx=5,pady=5)
        nameEntry.grid(row=0,column=1,padx=5,pady=5)
        nameEntry.insert(0,"ABC")
        nameEntry.bind("<ButtonPress-1>", clear)

        dobLabel = Label(win, text="D.O.B")
        dobEntry = Entry(win,text="28-05-1996")
        dobEntry.delete(0, END)
        dobEntry.insert(0,"DD-MM-YYYY")
        dobLabel.grid(row=1,column=0,padx=5,pady=5)
        dobEntry.grid(row=1,column=1,padx=5,pady=5)
        dobEntry.bind("<ButtonPress-1>", clear)

        phLabel = Label(win, text="Phone No.")
        ccEntry = Entry(win,text="0123",width=4)
        ccEntry.delete(0, END)
        ccEntry.insert(0,"0123")
        # _Label = Label(win,text="-",width=1)
        phEntry = Entry(win,text="1234567890")
        phEntry.delete(0, END)
        phEntry.insert(0,"1234567890")
        phLabel.grid(row=2,column=0,padx=5,pady=5)
        ccEntry.grid(row=2,column=1,padx=5,pady=5)
        # _Label.grid(row=2,column=2)
        phEntry.grid(row=2,column =2,padx=2,pady=5)
        ccEntry.bind("<ButtonPress-1>", clear)
        phEntry.bind("<ButtonPress-1>", clear)

        emailLabel = Label(win, text="Email Id")
        emailEntry = Entry(win,text="abc@xyz.com")
        emailEntry.delete(0, END)
        emailEntry.insert(0,"abc@xyz.com")
        emailLabel.grid(row=3,column=0,padx=5,pady=5)
        emailEntry.grid(row=3,column=1,padx=5,pady=5)
        emailEntry.bind("<ButtonPress-1>", clear)


        addressLabel = Label(win, text=">>>>>>>>>Address Details<<<<<<<<<<<")
        addressLabel.grid(row=4,columnspan=4,padx=5,pady=5)
        # Create a Tkinter variable
        cityVar = StringVar(win)

        # Dictionary with options
        choices = {'Ahmedabad', 'Aurangabad', 'Mumbai', 'New Delhi', 'Bengaluru', 'Hyderabad', 'Shillong', 'Leh', 'Kochi', 'Port Blair'}
        cityVar.set('Mumbai') # set the default option

        popupMenu = OptionMenu(win, cityVar, *choices)
        Label(win, text="City Name").grid(row = 5, column = 0)
        popupMenu.grid(row = 5, column =1)

        # on change dropdown value
        def change_dropdown(*args):
            print( cityVar.get() )

        # link function to change dropdown
        cityVar.trace('w', change_dropdown)

        addressEntry = Text(win,height=2,width=60)
        addressEntry.delete(1.0, END)
        addressEntry.grid(rowspan=3,columnspan=4,ipady=1,padx=5,pady=5)
        addressEntry.bind("<ButtonPress-1>", clear)

        zipLabel = Label(win, text="Zip")
        zipLabel.grid(row=9,column=0,padx=5,pady=5)

        zipEntry = Entry(win,text="800023")
        zipEntry.delete(0, END)
        zipEntry.insert(0,"123456")
        zipEntry.grid(row=9,column=1,padx=5,pady=5)
        zipEntry.bind("<ButtonPress-1>", clear)


        # quit child window and return to root window
        # the button is optional here, simply use the corner x of the child window
        Button(win, text='Submit', command=destroy).grid(row=10,columnspan = 4,padx=10,pady=5)
        # We need bind a window can be killed by many ways
        win.bind("<Destroy>",lambda x:self.root.deiconify())

    def editItemWindow(self,index):
        # Inside helping functions
        def destroy():
            error = False
            nameVar = nameEntry.get()
            if(nameVar == "ABC"):
                nameVar = ""
            dobVar  = dobEntry.get()
            if(dobVar == "DD-MM-YYYY"):
                dobVar = ""
            emailVar  = emailEntry.get()
            if(emailVar == "abc@xyz.com"):
                emailVar = ""
            cityvar = cityVar.get()
            addVar  = addressEntry.get(1.0,END)
            zipVar  = zipEntry.get()
            if(zipVar == "123456"):
                zipVar = ""

            if(len(zipVar)>0 and (len(zipVar)!=6 or zipVar[0]=="0" or not zipVar.isdigit())):
                messagebox.showwarning('Warning', 'Invalid Zip Code')
                zipEntry.delete(0,END)
                zipEntry.focus_set()
                error = True

            year  = now.year
            month = now.month
            day   = now.day

            if(len(emailVar)>0 and not isValidEmail(emailVar)):
                emailVar = ""
                messagebox.showwarning('Warning', 'Invalid Email')
                emailEntry.focus_set()
                emailEntry.delete(0,END)
                error = True

            if(len(dobVar)>0):
                a = dobVar.split("-")
                if(len(a)!=3 or not a[0].isdigit() or not a[1].isdigit() or not a[2].isdigit() or int(a[0])>31 or int(a[1])>12 or int(a[2])<=0):
                    messagebox.showwarning('Warning', 'DOB is invalid')
                    dobEntry.delete(0,END)
                    dobEntry.focus_set()
                    dobEntry.insert(0,"DD-MM-YYYY")
                    error = True
                else:
                    year  = int(year)  - int(a[2])
                    month = int(month) - int(a[1])
                    day   = int(day)   - int(a[0])
                    if(year>10):
                        pass
                    elif(year==10 and month>=0 and day>=0):
                        pass
                    else:
                        messagebox.showwarning('Warning', 'Not Above 10')
                        dobVar = ""
                        error = True

            if(len(nameVar)==0):
                nameEntry.focus_set()
                nameEntry.delete(0,END)
            elif(len(dobVar)==0):
                dobEntry.focus_set()
                dobEntry.delete(0,END)
            elif(error):
                pass
            else:
                self.nameList[index]  = (nameVar)
                self.dobList[index]   = (dobVar)
                self.emailList[index] = (emailVar)
                self.addList[index]   = (addVar)
                self.cityList[index]  = (cityvar)
                self.zipList[index]   = (zipVar)
                phList = [self.phoneList[index]]
                self.conn.DELETEENTRY(phList)
                data = [[self.nameList[index]],[self.phoneList[index]], [self.addList[index]], [self.cityList[index]], [self.emailList[index]], [self.zipList[index]], [self.dobList[index]]]
                # print(data)
                self.conn.INSERT(data)
                self.select.delete(0,END)
                for i in range(len(self.phoneList)):
                    self.select.insert("end", "{0} {1}".format(self.tabify(self.nameList[i]), self.phoneList[i]))
                win.destroy()
        def clear(self):
            # print(self.widget)
            if(str(self.widget)[-4:]!="text"):
                self.widget.delete(0,END)
            else:
                self.widget.delete(1.0,END)
        def isValidEmail(email):
            if(re.match(r'[\w\.-]+@[\w\.-]+',string=email)!= None):
                return True
            return False
        # create child window
        win = Toplevel()
        win.title("Edit")
        win.resizable(False, False)
        # create labels and entry
        nameLabel = Label(win, text="Name")
        nameEntry = Entry(win)
        nameEntry.delete(0, END)
        nameLabel.grid(row=0,column=0,padx=5,pady=5)
        nameEntry.grid(row=0,column=1,padx=5,pady=5)
        nameEntry.insert(0,self.nameList[index])
        nameEntry.bind("<ButtonPress-1>", clear)

        dobLabel = Label(win, text="D.O.B")
        dobEntry = Entry(win,text="28-05-1996")
        dobEntry.delete(0, END)
        dobEntry.insert(0,self.dobList[index])
        dobLabel.grid(row=1,column=0,padx=5,pady=5)
        dobEntry.grid(row=1,column=1,padx=5,pady=5)
        dobEntry.bind("<ButtonPress-1>", clear)

        phLabel = Label(win, text="Phone No.")
        ccEntry = Entry(win,text="0123",width=4)
        ccEntry.delete(0, END)
        ccEntry.insert(0,self.phoneList[index][:4])
        # _Label = Label(win,text="-",width=1)
        phEntry = Entry(win,text="1234567890")
        phEntry.delete(0, END)
        phEntry.insert(0,self.phoneList[index][5:])
        phLabel.grid(row=2,column=0,padx=5,pady=5)
        ccEntry.grid(row=2,column=1,padx=5,pady=5)
        # _Label.grid(row=2,column=2)
        phEntry.grid(row=2,column =2,padx=2,pady=5)
        ccEntry.bind("<ButtonPress-1>", clear)
        ccEntry.configure(state='disabled')
        phEntry.bind("<ButtonPress-1>", clear)
        phEntry.configure(state='disabled')

        emailLabel = Label(win, text="Email Id")
        emailEntry = Entry(win,text="abc@xyz.com")
        emailEntry.delete(0, END)
        emailEntry.insert(0,self.emailList[index])
        emailLabel.grid(row=3,column=0,padx=5,pady=5)
        emailEntry.grid(row=3,column=1,padx=5,pady=5)
        emailEntry.bind("<ButtonPress-1>", clear)

        addressLabel = Label(win, text=">>>>>>>>>Address Details<<<<<<<<<<<")
        addressLabel.grid(row=4,columnspan=4,padx=5,pady=5)
        # Create a Tkinter variable
        cityVar = StringVar(win)

        # Dictionary with options
        choices = {'Ahmedabad', 'Aurangabad', 'Mumbai', 'New Delhi', 'Bengaluru', 'Hyderabad', 'Shillong', 'Leh', 'Kochi', 'Port Blair'}
        cityVar.set(self.cityList[index]) # set the default option

        popupMenu = OptionMenu(win, cityVar, *choices)
        Label(win, text="City Name").grid(row = 5, column = 0)
        popupMenu.grid(row = 5, column =1)

        # on change dropdown value
        def change_dropdown(*args):
            print( cityVar.get() )

        # link function to change dropdown
        cityVar.trace('w', change_dropdown)

        addressEntry = Text(win,height=2,width=60)
        addressEntry.delete(1.0, END)
        addressEntry.insert(1.0,self.addList[index])
        addressEntry.grid(rowspan=3,columnspan=4,ipady=1,padx=5,pady=5)
        addressEntry.bind("<ButtonPress-1>", clear)

        zipLabel = Label(win, text="Zip")
        zipLabel.grid(row=9,column=0,padx=5,pady=5)

        zipEntry = Entry(win,text="800023")
        zipEntry.delete(0, END)
        zipEntry.insert(0,self.zipList[index])
        zipEntry.grid(row=9,column=1,padx=5,pady=5)
        zipEntry.bind("<ButtonPress-1>", clear)

        # quit child window and return to root window
        # the button is optional here, simply use the corner x of the child window
        Button(win, text='Update', command=destroy).grid(row=10,columnspan = 4,padx=10,pady=5)
        # We need bind a window can be killed by many ways
        win.bind("<Destroy>",lambda x:self.root.deiconify())

    def searchItemWindow(self):
        # Helping functions
        def destroy():
            queryList = []
            if(nameSelect.get() == 1):
                query="UPPER(Name) = '{}'".format(nameEntry.get().upper())
                queryList.append(query)
            if(citySelect.get() == 1):
                query="City = '{}'".format(cityVar.get())
                queryList.append(query)
            if(ageSelect.get() == 1):
                query="Age {} {}".format(ageChoiceVar.get(),ageEntry.get())
                queryList.append(query)
            finalQ = " AND ".join(queryList)
            if(len(finalQ)==0):
                messagebox.showwarning('Warning', 'No Query Generated\nPlease Select One')
            else:
                data = self.conn.SEARCH(finalQ)
                phoneList = []
                nameList  = []
                for i in range(len(data)):
                    phoneList.append(data[i][1])
                    nameList.append(data[i][0])
                self.select.delete(0,END)
                for i in range(len(phoneList)):
                    self.select.insert("end", "{0} {1}".format(self.tabify(nameList[i]), phoneList[i]))

                win.destroy()

        # create child window
        win = Toplevel()
        win.title("Search")
        win.resizable(False, False)
        nameSelect = IntVar()
        citySelect = IntVar()
        ageSelect  = IntVar()

        Checkbutton(win, text="Name", variable=nameSelect).grid(row=0,column=0,padx=5,pady=5, sticky=W)
        Checkbutton(win, text="City", variable=citySelect).grid(row=1,column=0,padx=5,pady=5, sticky=W)
        Checkbutton(win, text="Age", variable=ageSelect).grid(row=2,column=0,padx=5,pady=5, sticky=W)

        nameEntry = Entry(win)
        nameEntry.grid(row=0,column=1,padx=5,pady=5)
        # Create a Tkinter variable
        cityVar = StringVar(win)

        # Dictionary with options
        choices = {'Ahmedabad', 'Aurangabad', 'Mumbai', 'New Delhi', 'Bengaluru', 'Hyderabad', 'Shillong', 'Leh', 'Kochi', 'Port Blair'}
        cityVar.set('Mumbai') # set the default option

        popupMenu = OptionMenu(win, cityVar, *choices)
        popupMenu.grid(row = 1, column =1)

        # Create a Tkinter variable
        ageChoiceVar = StringVar(win)

        # Dictionary with options
        choices = {'>', '=', '<'}
        ageChoiceVar.set('=') # set the default option

        popupMenu = OptionMenu(win, ageChoiceVar, *choices)
        popupMenu.grid(row = 2, column =1)
        ageEntry = Entry(win)
        ageEntry.grid(row=2,column=2,padx=5,pady=5)

        Button(win, text='Search', command=destroy).grid(row=10,columnspan = 4,padx=10,pady=5)
        # We need bind a window can be killed by many ways
        win.bind("<Destroy>",lambda x:self.root.deiconify())



# Driver Function
if __name__ == '__main__':
    ph = phoneBook()
