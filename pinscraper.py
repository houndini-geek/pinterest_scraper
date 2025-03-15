from tkinter import Tk, Entry, Label, Button, StringVar,messagebox, filedialog

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException

from selenium.webdriver.chrome.options import Options 

import threading

from selenium.common.exceptions import NoSuchElementException 
import time
import os
import requests

import random
from fake_useragent import UserAgent

def random_number():
    return random.randint(1, 50000)

# Set up User-Agent
ua = UserAgent()
headers = {'User-Agent': ua.random}

#Add colorful print for better readability AGAHHAHAAHA
from colorama import Fore

#Import webdriver manager
from webdriver_manager.chrome import ChromeDriverManager

folder_path = os.path.expanduser('~'+'/Downloads/pinterest_images')

#Create a folder
def create_folder():
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    else:
        print(Fore.RED + "Folder already exists")
        #feedback.set("Folder already exists")
        print(Fore.WHITE)
        return
create_folder()

def change_folder():
    global folder_path
    folder_path = filedialog.askdirectory(title='Create or choose a folder',initialdir=os.path.expanduser('~'+'/Downloads/'))
 



def scrap_images():
    global folder_path
     
    submit_button.config(state='disabled')
    scroll_count = iteration_entry.get()
    url = url_entry.get()
    
    if not scroll_count.isnumeric():
        return messagebox.showerror(title='Invalid iteration count', message='Iteration count must be a number !')
    
    try:
         #Create a new instance of the Chrome driver
        browser = webdriver.Chrome()
                #Open the URL
        print(Fore.GREEN + "Opening URL")
        print(Fore.WHITE)
        feedback.set("Opening URL")
        browser.maximize_window()
        
        if url:
          browser.get(url)
        else:
          browser.get(f'https://www.pinterest.com/search/pins/?q={search_entry.get()}&rs=ac&len=3&source_id=VlHVRFnM&eq=pro&etslf=4987')

        print(Fore.GREEN + "URL opened")
        print(Fore.WHITE)
        feedback.set("URL opened")
        print("\n")
    except WebDriverException as e:
        messagebox.showerror(title='Uknown error', message=f"e")
        print(Fore.LIGHTRED_EX,f'{e}')

            
  
   
   
    
    #Find images container 
    wait = WebDriverWait(browser, 10)
    container = wait.until(lambda browser: browser.find_element(By.CSS_SELECTOR, '.masonryContainer'))
    if container:
      print(Fore.GREEN + "Container found")
      print(Fore.WHITE)
      feedback.set("Container found")
    else:
        print(Fore.RED + "Container not found")
        print(Fore.WHITE)
        feedback.set("Container not found")
        messagebox.showerror("Error", "Container not found")
        return  
    images = []
     # Scroll until we reach a specific condition
    try:
        for i in range(int(scroll_count)):  # Increase scroll iterations to load more images
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(Fore.GREEN + f"Scrolling... Iteration {i + 1}")
            print(Fore.WHITE)
            # Add a timeout to the feedback label
            feedback.set(f"Scrolling... Iteration {i + 1}")

            #Timeout between each iteration
            time.sleep(10)

            all_images = container.find_elements(By.CSS_SELECTOR, 'img')
            print(Fore.GREEN + f"Found {len(all_images)} images on the {i + 1} iteration")
            time.sleep(2)
            if all_images:
                for img in all_images:
                    #Get the image source
                    src = img.get_attribute('src')
                    images.append({'src': src})
                print(Fore.GREEN + f"Added {len(images)} images to the list on the {i + 1} iteration")
                feedback.set(f"Added {len(images)} images to the list on the {i + 1} iteration")
                time.sleep(2)
            else:
                print(Fore.RED + "No images found in the container")
                print(Fore.WHITE)
                feedback.set("No images found")
                messagebox.showerror("Error", "No images found in the container")
                browser.quit()
                return
            
        print(Fore.GREEN + "Scrolling finished")
        feedback.set("Scrolling finished")
    except Exception as e:
        print(Fore.RED + f"Failed to scroll: {e}")
        print(Fore.WHITE)
        feedback.set("Failed to scroll")
        messagebox.showerror("Error", f"Failed to scroll: {e}")
        return
     
    if images:
        print(Fore.GREEN + "Downloading images")
        print(Fore.WHITE)
        feedback.set("Downloading images")
        print(Fore.GREEN,f"{len(images)} images found")
        print(Fore.WHITE)
        feedback.set(f"{len(images)} images found")
        print(Fore.GREEN, "Please wait...")
        feedback.set("Please wait...")
        print(Fore.WHITE)

        # Update the image download section with headers
        for i, img in enumerate(images):
            try:
                response = requests.get(img['src'], headers=headers, timeout=10)
                response.raise_for_status()  # Check if the request was successful
                image_extension = img['src'].split('.')[-1]
                with open(f"{folder_path}/image_{random_number()}.{image_extension}", "wb") as file:
                    file.write(response.content)
                    print(Fore.GREEN + f"Image {i} downloaded")
                    feedback.set(f"Downloading: {i}/{len(images)}")
            except requests.exceptions.RequestException as e:
                print(Fore.RED + f"Failed to download image {i}: {e}")
                print(Fore.WHITE)
                messagebox.showerror("Error", f"Failed to download image {i}: {e}")
                feedback.set("Failed to download image")
                continue
        print(Fore.GREEN + "All images downloaded")
        feedback.set("All images downloaded")
        messagebox.showinfo("Success", f"All images downloaded to the folder '{folder_path}'")
        submit_button.config(state='normal')
    else:
        print(Fore.RED + "No images to download")
        print(Fore.WHITE)
        feedback.set("No images found")  
        messagebox.showerror("Error", "No images to download")
        return
        
    #Close the browser
    browser.quit()
    print(Fore.GREEN + "Browser closed")
    print(Fore.WHITE)
    feedback.set("Browser closed")


#Create a GUI

root = Tk()
root.title("PinScraper")
root.geometry("400x270")
root.config(padx=7)


search_label = Label(root, text="Enter search term", anchor='w')
search_label.pack(fill="both")

search_entry = Entry(root)
search_entry.config(width=50, font=("Arial", 12), 
                    borderwidth=2, 
                    relief="groove",
                    justify="left", 
                    fg="black", 
                    bg="white",
                    cursor="xterm")
search_entry.pack(ipady=5)





url_label = Label(root, text="Paste a Pinterest URL", anchor='w')
url_label.pack(fill="both")

url_entry = Entry(root)
url_entry.config(width=50, font=("Arial", 12), 
                    borderwidth=2, 
                    relief="groove",
                    justify="left", 
                    fg="black", 
                    bg="white",
                    cursor="xterm")
url_entry.pack(ipady=5)









iteration_label = Label(root, text="Enter iteration scroll (Default 5)",anchor='w')
iteration_label.pack(fill='both')

iteration_entry = Entry(root)
iteration_entry.insert(0,int(5))
iteration_entry.config(width=50, font=("Arial", 12), 
                    borderwidth=2, 
                    relief="groove",
                    justify="left", 
                    fg="black", 
                    bg="white",
                    cursor="xterm")
iteration_entry.pack()




#Feedback label for the user to know what is happening in the background 
feedback = StringVar()
feedback.set("Nothing to download")
feedback_label = Label(root, textvariable=feedback)
feedback_label.config(font=("Arial", 12), 
                      fg="black",
                      cursor="xterm",
                      )
feedback_label.pack()



submit_button = Button(root, text="Submit", 
                       cursor="hand2", 
                          font=("Arial", 12),
                            fg="#F1F1F1",
                            bg="#262626",
                            width=30,
                            relief="raised",
                            borderwidth=2,

                       command=lambda: threading.Thread(target=scrap_images).start())
submit_button.pack(ipady=3)

create_folder_btn = Button(text='Change download folder',command=change_folder)
create_folder_btn.config(cursor='hand2',relief='flat')
create_folder_btn.pack()

root.resizable(False, False)
root.mainloop()