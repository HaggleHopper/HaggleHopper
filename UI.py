import tkinter as tk
from tkinter.messagebox import askyesno as tkaskyesno
import Backend
import asyncio
import threading
import time

class Chat:
    """This is the chat window that appears for each ISP. It handles the chatbot and ISP bridge and displays the messages in a tkinter window."""
    def __init__(self, parent, name, callback) -> None:
        self.parent = parent

        # Create the container
        self.container = tk.Frame(parent, bg="#555555")

        # Store information about the ISP
        self.name = name
        self.callback = callback
        self.address = callback.address
        self.houseNumber = callback.houseNumber
        self.userName = callback.name
        self.messages=[]

        # Instantiate the backend for the ISP
        self.Hopper = Backend.Hopper(self.userName, self.name, self.callback.prices, self.address, self)

        # Create the tkinter window
        self.initTk()
    
    def initTk(self) -> None:
        """Initialise the tkinter window"""
        self.container.grid_columnconfigure(0, weight=1, uniform=True)
        self.container.grid_columnconfigure(1, weight=30, uniform=True)
        self.container.grid_columnconfigure(2, weight=1, uniform=True)
        self.container.grid_rowconfigure(0, weight=1, uniform=True)
        self.container.grid_rowconfigure(1, weight=5, uniform=True)
        self.container.grid_rowconfigure(2, weight=30, uniform=True)
        self.container.grid_rowconfigure(3, weight=3, uniform=True)
        self.container.grid_rowconfigure(4, weight=5, uniform=True)
        self.container.grid_rowconfigure(5, weight=1, uniform=True)

        label = tk.Label(self.container, text=self.name,bg="#555555", fg="white", font=("Arial", 40))
        label.grid(row=1, column=1, sticky="nsew")

        self.input = tk.Text(self.container, bg="#777777", fg="#ffffff", insertbackground="#ffffff")
        self.input.grid(row=4, column=1, sticky="nsew")
        self.takeControlButton = tk.Button(self.container, text="Take Control", command=self.takeControl)
        self.takeControlButton.grid(row=3, column=1, sticky="nsew")

        self.chatWindow = tk.Text(self.container, bg="#777777", fg="#ffffff", insertbackground="#ffffff")
        self.chatWindow.grid(row=2, column=1, sticky="nsew")

        self.displayChat()

    def grid(self,r,c):
        """Called by tkinter to possition the window in the grid. This is a wrapper for the grid method of the container."""
        self.container.grid(row=r, column=c, sticky="nsew")

    def takeControl(self):
        """Called when the user wants to take manual control of the chatbot."""
        self.takeControlButton.destroy()
        self.input.bind("<Return>", self.sendMessage)
        self.input.focus()

        # Terminate the chatbot's mainloop
        self.Hopper.auto=False
    
    def sendMessage(self, event):
        """Handles the manual sending of messages to the chatbot."""
        message = self.input.get("1.0", tk.END).strip()
        self.input.delete("1.0", tk.END)
        self.Hopper.responceOveride=message


    def displayChat(self):
        """Displays the chat messages in the chat window."""
        self.chatWindow.delete("1.0", tk.END)
        owned=True
        for message in self.messages:
            self.chatWindow.insert(tk.END, "Haggle Hopper:\n" if owned else self.name+":\n")
            self.chatWindow.insert(tk.END, message+"\n\n")
            owned = not owned
        self.chatWindow.see(tk.END)
    
    def acceptDeal(self,json) -> bool:
        """Called by chatbot when a deal is offered. This method asks the user if they want to accept the deal. If they do, it sends an acept message and then takes control of the chatbot. If they don't, it returns False."""
        
        # If another chatbot has already found a deal that was accepted just freeze until the deal is cancelled
        while self.callback.foundPrices:
            time.sleep(1) # hang as user has chosen another deal

        # Wait until the user has made a decision on the prevuous deal so they dont get flooded with popups
        while self.callback.CurrentlyPopupOpen:
            time.sleep(1)

        # Set the flag to indicate that a popup is open
        self.callback.CurrentlyPopupOpen=True

        # Ask the user if they want to accept the deal
        r=tkaskyesno(title=f"{self.name} offered a deal:",message=f"Do you want to accept a deal from {self.name}:\n{json}\n\nAccept?")

        # Set the flag to indicate that the popup is closed
        self.callback.CurrentlyPopupOpen=False
        
        if r:
            self.callback.foundPrices=True
            self.takeControl()
        return r
    
    async def mainloop(self):
        async for m in self.Hopper.run():
            self.messages.append(m)
            self.displayChat()

    def startChat(self):
        asyncio.run(self.mainloop())


class UI:
    def __init__(self) -> None:
        """Initialise the UI. This is the main class for the UI. It handles the main window and the chat windows. It also handles the mainloop for the UI."""
        self.prices=""
        self.foundPrices=False # Has a deal been found and accepted
        self.CurrentlyPopupOpen=False # Is a confirmation popup open

    def initTk(self) -> None:
        """Create the main window for the UI. This is the first window that appears when the program is run. It is the main window that contains the chat windows."""
        self.root = tk.Tk()
        self.root.title("HaggleHopper")
        self.root.state('zoomed')
        self.root.resizable(False, False)
        self.scene = tk.Canvas(self.root)
        self.scene.pack(fill=tk.BOTH, expand=1)
        self.startScreen()
        self.root.mainloop()

    def startScreen(self) -> None:
        """This is where the start screen is created. It is the first screen that appears when the program is run. It contains the start button and the title."""
        self.scene.delete("all")

        # Grid possitioning
        self.scene.grid_columnconfigure(0, weight=1, uniform=True)
        self.scene.grid_columnconfigure(1, weight=4, uniform=True)
        self.scene.grid_columnconfigure(2, weight=1, uniform=True)
        self.scene.grid_rowconfigure(0, weight=2, uniform=True)
        self.scene.grid_rowconfigure(1, weight=4, uniform=True)
        self.scene.grid_rowconfigure(2, weight=1, uniform=True)

        container = tk.Frame(self.scene, bg="#555555")
        container.grid(row=1, column=1, sticky="nsew")

        # Grid possitioning
        container.grid_rowconfigure(0, weight=1, uniform=True)
        container.grid_rowconfigure(1, weight=1, uniform=True)
        container.grid_rowconfigure(2, weight=2, uniform=True)
        container.grid_rowconfigure(3, weight=1, uniform=True)
        container.grid_rowconfigure(4, weight=2, uniform=True)
        container.grid_rowconfigure(5, weight=1, uniform=True)
        container.grid_rowconfigure(6, weight=2, uniform=True)
        container.grid_rowconfigure(7, weight=1, uniform=True)
        container.grid_rowconfigure(8, weight=2, uniform=True)
        container.grid_rowconfigure(9, weight=1, uniform=True)
        container.grid_rowconfigure(10, weight=3, uniform=True)
        container.grid_rowconfigure(11, weight=1, uniform=True)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=10)
        container.grid_columnconfigure(2, weight=1)

        # Title
        label = tk.Label(self.scene, text="Haggle Hopper", fg="black", font=("Arial", 100))
        label.grid(row=0, column=1, sticky="nsew")

        # Create all of the input boxes
        self.addressBox = tk.Entry(container,bg="#777777", fg="white", font=("Arial", 25), justify=tk.CENTER)
        self.addressBox.grid(row=2, column=1, sticky="nsew")

        label = tk.Label(container, text="Enter your postcode:", bg="#555555", fg="white", font=("Arial", 25))
        label.grid(row=1, column=1, sticky="nsew")

        self.houseNumberBox = tk.Entry(container,bg="#777777", fg="white", font=("Arial", 25), justify=tk.CENTER)
        self.houseNumberBox.grid(row=4, column=1, sticky="nsew")

        label = tk.Label(container, text="Enter your house no.:", bg="#555555", fg="white", font=("Arial", 25))
        label.grid(row=3, column=1, sticky="nsew")

        self.nameBox = tk.Entry(container,bg="#777777", fg="white", font=("Arial", 25), justify=tk.CENTER)
        self.nameBox.grid(row=6, column=1, sticky="nsew")

        label = tk.Label(container, text="Enter your name:", bg="#555555", fg="white", font=("Arial", 25))
        label.grid(row=5, column=1, sticky="nsew")

        self.currentISP = tk.Entry(container,bg="#777777", fg="white", font=("Arial", 25), justify=tk.CENTER)
        self.currentISP.grid(row=8, column=1, sticky="nsew")

        label = tk.Label(container, text="Enter your current ISP name:", bg="#555555", fg="white", font=("Arial", 25))
        label.grid(row=7, column=1, sticky="nsew")


        # Start button
        self.start = tk.Button(container,bg="#777777", fg="white", font=("Arial", 40), justify=tk.CENTER,text="Start", command=lambda:self.started())
        self.start.grid(row=10, column=1, sticky="nsew")

        # Padding
        label = tk.Label(container, text="", bg="#555555", fg="white", font=("Arial", 25))
        label.grid(row=9, column=1, sticky="nsew")
        label = tk.Label(container, text="", bg="#555555", fg="white", font=("Arial", 25))
        label.grid(row=11, column=1, sticky="nsew")

        # Default values used for testing
        self.addressBox.insert(0, "CB1 8PX") 
        self.houseNumberBox.insert(0, "97") 
        self.nameBox.insert(0, "John") 
        self.currentISP.insert(0, "Virgin Media") 

    def started(self) -> None:
        """This function is called when the start button is pressed. It gets the values from the input boxes and calls the obtainingPrices function."""
        self.address = self.addressBox.get()
        self.houseNumber = self.houseNumberBox.get()
        self.name = self.nameBox.get()
        self.currentISP = self.currentISP.get()
        self.obtainingPrices()

    async def obtainPrices(self) -> None:
        for attempt in range(3): # Try 3 times to get the prices if not then ignore this step
            try:
                self.prices = await Backend.GetPrices(self.address, self.houseNumber)
                return
            except IndexError:
                pass
        self.prices=""

    def obtainingPrices(self) -> None:
        """This function is called when the start button is pressed. It displays a loading screen and calls the obtainPrices function. If the prices are obtained it calls the displayPrices function."""
        self.scene.destroy()

        self.scene = tk.Canvas(self.root)
        self.scene.pack(fill=tk.BOTH, expand=1)

        # Grid configuration
        self.scene.grid_columnconfigure(0, weight=1, uniform=True)
        self.scene.grid_columnconfigure(1, weight=100, uniform=True)
        self.scene.grid_columnconfigure(2, weight=1, uniform=True)
        self.scene.grid_rowconfigure(0, weight=1, uniform=True)
        self.scene.grid_rowconfigure(1, weight=100, uniform=True)
        self.scene.grid_rowconfigure(2, weight=30, uniform=True)
        self.scene.grid_rowconfigure(3, weight=1, uniform=True)

        label = tk.Label(self.scene, text="Obtaining Prices...", fg="black", font=("Arial", 100))
        label.grid(row=1, column=1, sticky="nsew")
        label = tk.Label(self.scene, text="This may take a while.", fg="black", font=("Arial", 30))
        label.grid(row=2, column=1, sticky="nsew")

        self.root.update()
        self.root.update_idletasks()

        # Start a new thread to obtain the prices
        threading.Thread(target=lambda:asyncio.run(self.obtainPrices())).start()

        # Check if the prices have been obtained
        self.checkIfFinnishedObtainingPrices()

    def checkIfFinnishedObtainingPrices(self) -> None:
        """Repetatively checks if the prices have been obtained. If they have it calls the mainScreen function. If not it calls itself again after 1 seccond."""
        if not self.prices:
            self.root.after(1000, self.checkIfFinnishedObtainingPrices)
            return

        self.mainScreen()

    def mainScreen(self) -> None:
        """This function is called when the prices have been obtained. It displays the main screen with the prices and the chat boxes."""
        self.scene.destroy()
        
        self.scene = tk.Canvas(self.root)
        self.scene.pack(fill=tk.BOTH, expand=1)

        # Grid configuration
        self.scene.grid_columnconfigure(0, weight=1, uniform=True)
        col=1
        for isp in Backend.ISPs:
            self.scene.grid_columnconfigure(col, weight=20, uniform=True)
            self.scene.grid_columnconfigure(col+1, weight=1, uniform=True)
            col+=2
        self.scene.grid_rowconfigure(0, weight=1, uniform=True)
        self.scene.grid_rowconfigure(1, weight=40, uniform=True)
        self.scene.grid_rowconfigure(2, weight=1, uniform=True)

        # Create all the chat windows dynamically
        self.chats=[]
        col=1
        for isp in Backend.ISPs:
            chat = Chat(self.scene, isp, self)
            chat.grid(1, col)
            self.chats.append(chat)
            col+=2

        # Start each chat in a new thread
        for chat in self.chats:
            threading.Thread(target=lambda:chat.startChat()).start()
        

def run():
    """Starts the UI."""
    ui=UI()
    ui.initTk()

if __name__ == "__main__":
    """If the file is run directly then start the UI."""
    run()