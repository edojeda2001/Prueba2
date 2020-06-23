from tkinter import ttk
from tkinter import *

import sqlite3

class Program:
    
    DBname='database.db'

    def DataBase(self,query,parameter=()):
        with sqlite3.connect(self.DBname) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query,parameter)
            conn.commit()
        return result

    def GetData(self):
        record=self.tree.get_children()
        for element in record:
            self.tree.delete(element)

        query='SELECT * FROM Product'
        dbRows = self.DataBase(query)
        for row in dbRows:
            self.tree.insert('', 0, text = row[1], value = row[2])

    def Validation(self):
        val=len(self.name.get())!=0 and len(self.price.get())!=0
        return val

    def AddData(self):
        if self.Validation():
            query='INSERT INTO Product VALUES(NULL, ?, ?)'
            parameter=(self.name.get(), self.price.get())
            self.DataBase(query,parameter)
            self.message['text']='Product {} has been saved'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.message['text']='Name and price is required'
        self.GetData()

    def DeleteData(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text']='Select a product in the list'
            return
        self.message['text']=''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM Product WHERE name = ?'
        self.DataBase(query,(name,))
        self.message['text']='Product {} has been delete'.format(name)
        self.name.delete(0, END)
        self.price.delete(0, END)
        self.GetData()
    
    def EditData(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text']='Select a product in the list'
            return
        self.message['text']=''
        oldName = self.tree.item(self.tree.selection())['text']
        oldPrice = self.tree.item(self.tree.selection())['values'][0]
        self.editwind = Toplevel()
        self.editwind.title = 'Edit Product'

        frame2 = LabelFrame(self.editwind, text="Prices's changes: {}".format(oldName))
        frame2.grid(row=0,column=0,columnspan=2,pady=20)

        Label(frame2,text='Old Name: ').grid(row=1,column=0)
        self.oldname = Entry(frame2,textvariable=StringVar(self.editwind,value=oldName),state='readonly')
        self.oldname.grid(row=1, column=1)

        Label(frame2,text='New Name: ').grid(row=2,column=0)
        name=Entry(frame2)
        name.grid(row=2,column=1)
        name.focus()

        Label(frame2,text='Old Price: ').grid(row=3,column=0)
        self.oldprice = Entry(frame2,textvariable=StringVar(self.editwind,value=oldPrice),state='readonly')
        self.oldprice.grid(row=3, column=1)

        Label(frame2,text='New Price: ').grid(row=4,column=0)
        price=Entry(frame2)
        price.grid(row=4,column=1)

        Button2=ttk.Button(frame2, text='Save changes',command= lambda: self.editData(oldName,name.get(),oldPrice,price.get()))
        Button2.grid(row=5,columnspan=2,sticky=W+E)

    def editData(self,oldName,name,oldPrice,price):
        query = 'UPDATE Product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameter=(name,price,oldName,oldPrice)
        self.DataBase(query,parameter)
        self.editwind.destroy()
        self.message['text']='Product {} has been edited succefullt'.format(name)
        self.name.delete(0, END)
        self.price.delete(0, END)
        self.GetData()

    def __init__(self,window):
        self.wind=window
        self.wind.title('Products Application')

        frame = LabelFrame(self.wind, text='Register a new product')
        frame.grid(row=0,column=0,columnspan=2,pady=20)

        Label(frame,text=' ').grid(row=1,column=0)

        Label(frame,text='Name: ').grid(row=2,column=0)
        self.name = Entry(frame)
        self.name.grid(row=2,column=1)
        self.name.focus()

        Label(frame,text='Price: ').grid(row=3,column=0)
        self.price=Entry(frame)
        self.price.grid(row=3,column=1)

        Label(frame,text=' ').grid(row=4,column=0)

        ttk.Button(frame, text='Save product',command=self.AddData).grid(row=5,columnspan=2,sticky=W+E)
        self.message = Label(text='',fg='blue')
        self.message.grid(row=6,column=0,sticky=W+E,columnspan=2)

        Label(text=' ').grid(row=7,column=0)

        self.tree = ttk.Treeview(height=10,columns=2)
        self.tree.grid(row=8, column=0,columnspan=2)
        self.tree.heading('#0',text='Product',anchor=CENTER)
        self.tree.heading('#1',text='Price',anchor=CENTER)
        self.GetData()
        ttk.Button(text='Edit',command=self.EditData).grid(row=9,column=0,sticky=W+E)
        ttk.Button(text='Delete',command=self.DeleteData).grid(row=9,column=1,sticky=W+E)


if __name__ == '__main__':
    window = Tk()
    application = Program(window)
    window.mainloop()