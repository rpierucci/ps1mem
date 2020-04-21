import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import os
import io
import codecs
import binascii
import array

def loadConfig(folderPath):
    try:
        file = open(os.path.join(os.path.dirname(__file__), 'settings.txt'), 'r')
        with file:
            gui.folderPath = file.readline()
            gui.folderPathLabel['text'] = file.readline()
        file.close()
    except:
        print('settings not found')

def setMemoryCardDirectory():
    gui.folderPath = filedialog.askdirectory(initialdir=gui.folderPathLabel['text'])
    file = open(os.path.join(os.path.dirname(__file__), 'settings.txt'), 'w')
    file.write(gui.folderPath)
    file.close()
    gui.folderPathLabel['text'] = gui.folderPath

def scanMemoryCards():
    for directory, subdirectory, files in os.walk(gui.folderPath):
        for f in files:
            if '.mcr' in f:
                file = open(directory + '/' + f, 'rb')
                countryCode = None
                productCode = None
                identifier = None
                iconDisplayFlag = None # 00 = no icon, 11 = icon has 1 frame (static), 12 = icon has 2 frames (animated), 13 = icon has 3 frames
                blockCount = None
                saveTitle = None
                bitmap = None

                with file:
                    file.seek(0x0008A)
                    byte = file.read(2)
                    countryCode = byte.decode('utf8')

                    file.seek(0x0008C)
                    byte = file.read(10)
                    productCode = byte.decode('utf8')

                    file.seek(0x00096)
                    byte = file.read(8)
                    identifier = byte.decode('utf8')

                    file.seek(0x02002)
                    byte = file.read(1)
                    iconDisplayFlag = byte.decode('utf8')

                    file.seek(0x02003)
                    byte = file.read(1)
                    blockCount = binascii.hexlify(byte)

                    # file.seek(0x02004)
                    # byte = file.read(64)
                    # saveTitle = byte

                    file.seek(0x02060)
                    byte = file.read(1)
                    palette = byte
                    hexadecimal = binascii.hexlify(byte)
                    decimal = int(hexadecimal, 16)
                    binary = bin(decimal)[2:].zfill(8)

                    # print((0b10101100) & 0x1F << 3)
                    # print(((0b11111001) & 0x3 << 6) | ((0b10101100) & 0xE0 >> 2))
                    # print(((0b11111001) & 0x7C) << 1)
                    # print(((0b11111001) & 0x80))

                    # file.seek(0x02080)
                    # byte = file.read(128)
                    # bitmap = byte
                    # hex values = every pair is flipped, each number represents pixel in table
                    
                    # hexadecimal = binascii.hexlify(byte)
                    # decimal = int(hexadecimal, 16)
                    # binary = bin(decimal)[2:].zfill(8)
                    # print("hex: %s, decimal: %s, binary: %s" % (hexadecimal, decimal, binary))
                gui.updateTable(f, countryCode, productCode, identifier)


                # print("Country Code: " + str(countryCode))
                # print("Product Code: " + str(productCode))
                # print("Identifier: " + str(identifier))
                # print("File Name: " + str(countryCode) + str(productCode) + str(identifier))
                # print("Icon Display Flag: " + str(iconDisplayFlag))
                # print("Block Count: " + str(blockCount))
                # print "Save Title: " + saveTitle
                # print "Bitmap: " + bitmap

                file.close()


def exitProgram():
    gui.master.quit()

def about():
    pass
class App():
    folderPathLabel = None
    folderPath = 'C:/'

    def __init__(self):
        self.master = tk.Tk()
        self.master.title('PS1Mem')
        self.master.geometry('1280x720')
        self.createUI()
        self.master.grid_rowconfigure(0, weight = 1)
        self.master.grid_columnconfigure(0, weight = 1)

    def createUI(self):
        self.menu = tk.Menu(self.master)
        self.fileMenu = tk.Menu(self.menu, tearoff=0)
        self.fileMenu.add_command(label='Set MCR Directory', command=setMemoryCardDirectory)
        self.fileMenu.add_command(label='Scan MCR Files', command=scanMemoryCards)
        self.fileMenu.add_command(label='Exit', command=exitProgram)
        self.menu.add_cascade(label='File', menu=self.fileMenu)
        self.helpMenu = tk.Menu(self.menu, tearoff=0)
        self.helpMenu.add_command(label='About', command=about)
        self.menu.add_cascade(label="Help", menu=self.helpMenu)    
        self.master.config(menu=self.menu)
        self.folderPathLabel = tk.Label(self.master, text=self.folderPath)
        self.folderPathLabel.place(relx=1.0, rely=1.0, anchor='se')

        tv = Treeview(self.master)
        tv['columns'] = ['countryCode', 'productCode', 'identifier']
        tv.column('#0', width = 200)
        tv.column('countryCode', width = 200)
        tv.column('productCode', width = 200)
        tv.column('identifier', width = 200)
        tv.heading('#0', text="Name")
        tv.heading('countryCode', text='Country Code')
        tv.heading('productCode', text='Product Code')
        tv.heading('identifier', text='Identifier')
        self.tv = tv
        self.tv.grid_rowconfigure(0, weight = 1)
        self.tv.grid_columnconfigure(0, weight = 1)
        self.tv.pack(side=tk.TOP,fill=tk.X)
       

    
    def updateTable(self, file, countryCode, productCode, identifier):
        self.tv.insert('', 'end', text=file, values=(countryCode, productCode, identifier))


        

    # def updateComponents(self):
    #     self.master.update_idletasks()
    #     self.master.after(1000, self.updateComponents)

gui = App()
loadConfig(gui.folderPath)
gui.master.mainloop()