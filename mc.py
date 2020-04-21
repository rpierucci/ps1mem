import tkinter as tk
from tkinter import filedialog
import os
import io
import codecs
import binascii
import array

folderPath = 'C:/'
root = tk.Tk()
folderPathLabel = tk.Label(root, text=folderPath)
files = []

def loadConfig():
    try:
        file = open(os.path.join(os.path.dirname(__file__), 'settings.txt'), 'r')
        with file:
            folderPathLabel['text'] = file.readline()
    except:
        print('settings not found')
        pass

def setMemoryCardDirectory():
    folderPath = filedialog.askdirectory(initialdir='C:/')
    file = open(os.path.join(os.path.dirname(__file__), 'settings.txt'), 'w')
    file.write(folderPath)
    folderPathLabel['text'] = folderPath
    # for files in os.walk(folder):
    #     print(files)

def scanMemoryCards():
    countryCode = None
    productCode = None
    identifier = None
    iconDisplayFlag = None # 00 = no icon, 11 = icon has 1 frame (static), 12 = icon has 2 frames (animated), 13 = icon has 3 frames
    blockCount = None
    saveTitle = None
    bitmap = None

    file = open(os.path.join(os.path.dirname(__file__), 'test.mcr'), 'rb')
    with file:
        file.seek(0x0008A)
        byte = file.read(2)
        countryCode = byte

        file.seek(0x0008C)
        byte = file.read(10)
        productCode = byte

        file.seek(0x00096)
        byte = file.read(8)
        identifier = byte

        file.seek(0x02002)
        byte = file.read(1)
        iconDisplayFlag = byte

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

        print((0b10101100) & 0x1F << 3)
        print(((0b11111001) & 0x3 << 6) | ((0b10101100) & 0xE0 >> 2))
        print(((0b11111001) & 0x7C) << 1)
        print(((0b11111001) & 0x80))

        # file.seek(0x02080)
        # byte = file.read(128)
        # bitmap = byte
        # hex values = every pair is flipped, each number represents pixel in table
        
        # hexadecimal = binascii.hexlify(byte)
        # decimal = int(hexadecimal, 16)
        # binary = bin(decimal)[2:].zfill(8)
        # print("hex: %s, decimal: %s, binary: %s" % (hexadecimal, decimal, binary))



    print("Country Code: " + str(countryCode))
    print("Product Code: " + str(productCode))
    print("Identifier: " + str(identifier))
    print("File Name: " + str(countryCode) + str(productCode) + str(identifier))
    print("Icon Display Flag: " + str(iconDisplayFlag))
    print("Block Count: " + str(blockCount))
    # print "Save Title: " + saveTitle
    # print "Bitmap: " + bitmap

    file.close()

def exitProgram():
    root.quit()

def about():
    pass

def window(root):
    root.title('PS1 Mem Organizer')
    root.geometry('1280x720')

    menu = tk.Menu(root)
    fileMenu = tk.Menu(menu, tearoff=0)
    fileMenu.add_command(label='Set MCR Directory', command=setMemoryCardDirectory)
    fileMenu.add_command(label='Scan MCR Files', command=scanMemoryCards)
    fileMenu.add_command(label='Exit', command=exitProgram)
    menu.add_cascade(label='File', menu=fileMenu)

    helpMenu = tk.Menu(menu, tearoff=0)
    helpMenu.add_command(label='About', command=about)
    menu.add_cascade(label="Help", menu=helpMenu)

    root.config(menu=menu)
    
   
    folderPathLabel.place(relx=1.0, rely=1.0, anchor='se')

loadConfig()


window(root)
root.mainloop()

