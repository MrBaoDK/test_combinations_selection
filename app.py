# Import the modules
from tkinter import Tk, Label, Entry, Button, StringVar
from tkinter.filedialog import askopenfilename, asksaveasfilename

# Import selection script
from comb_selection import TCS

# Create a root window
root = Tk()
root.title('Test Combinations Selector')

# Limit file extensions
filetypes = [('Csv files', ".csv")]

# Create a label and an entry for the input file name
inputfilename = StringVar()
l51 = Label(root, text="Input File Name:")
e31 = Entry(root, textvariable=inputfilename)

# Create a function to open the file dialog and get the file name
def select_input_file():
   # Use askopenfilename to show an "Open" dialog and return the file name
   inputfilename.set(askopenfilename(filetypes=filetypes))

# Create a button to trigger the file dialog
button31 = Button(root, text="Select File", command=select_input_file)

# Create a label and an entry for the output file name
outputfilename = StringVar()
l52 = Label(root, text="Output File Name:")
e32 = Entry(root, textvariable=outputfilename)

# Create a function to open the file dialog and get the file name
def select_output_file():
   # Use askopenfilename to show an "Open" dialog and return the file name
   outputfilename.set(asksaveasfilename(filetypes=filetypes))

# Create a button to trigger the file dialog
button32 = Button(root, text="Select File", command=select_output_file)

def valid_license():
   from datetime import datetime
   expired = datetime(2024,5,9,11,59,59)

   if datetime.now() < expired:
      return True
   
   return False

def run_selection():
   from tkinter import messagebox
   if valid_license():
      tcs = TCS(inputfilename.get(), outputfilename.get())
      try:
         tcs.execute()
         messagebox.showinfo('Successfully saved', f'Check your result at {outputfilename.get()}')
      except Exception as e:
         messagebox.showerror('Happed error', str(e))
   else:
      messagebox.showerror('Expired License', 'Please contact mrbaodk@hotmail.com')



button33 = Button(root, text="Run", command=run_selection)

# Use grid to arrange the widgets
l51.grid(row=0, column=0)
e31.grid(row=1, column=0)
button31.grid(row=1, column=1)
l52.grid(row=2, column=0)
e32.grid(row=3, column=0)
button32.grid(row=3, column=1)
button33.grid(row=5, column=0)

# Start the main loop
root.mainloop()