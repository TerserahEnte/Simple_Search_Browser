import tkinter as tk
from tkinter import ttk
import webbrowser
import requests
from PIL import Image, ImageTk
import re
from tkinter import messagebox
import webview
from tkinter.simpledialog import askstring

class History:
    def __init__(self, frame):
        self.clicked_urls = []
        self.clicked_urls_container = ttk.Frame(frame)
        self.clicked_urls_container.grid(row=2, column=5, columnspan=50, padx=(740, 0), pady=(0, 450))
        self.clicked_urls_container.grid_remove()
    
        self.clicked_urls_listbox = tk.Listbox(self.clicked_urls_container, width=35, height=20, font=('Arial', 10))
        self.clicked_urls_listbox.grid(row=0, column=0, sticky=tk.NSEW)

        scrollbar = tk.Scrollbar(self.clicked_urls_container, orient=tk.VERTICAL, command=self.clicked_urls_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)

        self.clicked_urls_listbox.config(yscrollcommand=scrollbar.set)
        
        self.history_image = Image.open("history.png")
        self.history_image = self.history_image.resize((20, 20))
        self.history_photo = ImageTk.PhotoImage(self.history_image)
        self.history_button = ttk.Button(frame, image=self.history_photo, command=self.create_container)
        self.history_button.grid(row=0, column=9, padx=5)
       
        self.clicked_urls_listbox.config(yscrollcommand=scrollbar.set)

        self.delete_button = ttk.Button(self.clicked_urls_container, text="Hapus", command=self.delete_clicked_url)
        self.delete_button.grid(row=1, column=0, columnspan=2, pady=5)  

    def create_container(self):
        if self.clicked_urls_container.winfo_ismapped():
            self.clicked_urls_container.grid_remove()
        else:
            self.clicked_urls_container.grid()
            self.show_urls()

    def show_urls(self):
        self.clicked_urls_listbox.delete(0, tk.END)
        for url in self.clicked_urls:
            if url not in self.clicked_urls_listbox.get(0, tk.END):
                self.clicked_urls_listbox.insert(tk.END, url)
        self.clicked_urls_listbox.bind("<Double-Button-1>", self.open_clicked_url)

    def open_clicked_url(self, event):
        if event.num == 1:  # Check if it's a single-click
            index = self.clicked_urls_listbox.nearest(event.y)
            if index is not None:
                url = self.clicked_urls[index]
                tampilWeb(url)

    def add_to_history(self, url):
        self.show_urls()
    
    def delete_clicked_url(self):
        # Dapatkan indeks yang dipilih
        selected_index = self.clicked_urls_listbox.curselection()
        if selected_index:
            # Hapus URL dari daftar dan perbarui tampilan
            del self.clicked_urls[selected_index[0]]
            self.show_urls()
    

class UserAuthentication:
    def __init__(self):
        self.users = {'user1': 'password1', 'user2': 'password2'}  # Replace with your user data

    def authenticate(self, username, password):
        return username in self.users and self.users[username] == password


class SignInDialog:
    def __init__(self, parent, authentication, web_browser):
        self.top = tk.Toplevel(parent)
        self.top.title("Sign In")

        self.authentication = authentication
        self.web_browser = web_browser

        self.username_label = ttk.Label(self.top, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=5)

        self.username_entry = ttk.Entry(self.top, font=('Arial', 12))
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        self.password_label = ttk.Label(self.top, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5)

        self.password_entry = ttk.Entry(self.top, show="*", font=('Arial', 12))
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.sign_in_button = ttk.Button(self.top, text="Sign In", command=self.sign_in)
        self.sign_in_button.grid(row=2, column=0, columnspan=2, pady=10)

    def sign_in(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.authentication.authenticate(username, password):
            messagebox.showinfo("Success", "Sign in successful")
            self.top.destroy()
            self.web_browser.sign_in_button.grid_forget()
           
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
class Tab:
    def __init__(self, root, notebook):
        self.root = root
        self.notebook = notebook


        self.frame = ttk.Frame(self.notebook)
        self.notebook.add(self.frame, text="New Tab")
        self.notebook.select(self.frame)
        self.notebook.pack(pady=5,padx=(5,0))



        self.entry = ttk.Entry(self.frame, width=100, font=('Arial', 12))
        self.entry.grid(row=0, column=5, padx=10, pady=10)
        self.entry.bind("<Return>", self.display_results)
        self.entry.insert(0, "Search or enter web address")
        self.entry.bind("<FocusIn>", self.clear_placeholder)
       
        self.search_image = Image.open("search.png")
        self.search_image = self.search_image.resize((20, 20))
        self.search_photo = ImageTk.PhotoImage(self.search_image)
        self.search_button = ttk.Button(self.frame, image=self.search_photo, command=self.display_results)
        self.search_button.grid(row=0, column=6, padx=10, pady=10)
        
        self.newtab_image = Image.open("newtab.png")
        self.newtab_image = self.newtab_image.resize((20, 20))
        self.newtab_photo = ImageTk.PhotoImage(self.newtab_image)

        self.new_tab_button = ttk.Button(self.frame, image=self.newtab_photo, command=self.create_browser_tab)
        self.new_tab_button.grid(row=0, column=7, padx=10, pady=10)

        self.closetab_image = Image.open("closetab.png")
        self.closetab_image = self.closetab_image.resize((20, 20))
        self.closetab_photo = ImageTk.PhotoImage(self.closetab_image)

        self.close_tab_button = ttk.Button(self.frame, image=self.closetab_photo, command=self.close_browser_tab)
        self.close_tab_button.grid(row=0, column=8, padx=10, pady=10)

        self.authentication = UserAuthentication()
        self.signIn_image = Image.open("profile.png")
        self.signIn_image = self.signIn_image.resize((20, 20))
        self.signIn_photo = ImageTk.PhotoImage(self.signIn_image)
        self.sign_in_button = ttk.Button(self.frame, text="Sign in ", image=self.signIn_photo,compound="right", command=self.show_sign_in_dialog)
        self.sign_in_button.grid(row=0, column=10, padx=5, pady=10)
        
        self.browser_frame = ttk.Frame(self.frame)
        self.browser_frame.grid(row=2, column=2, columnspan=15, pady=10, padx=50)
        self.browser_frame.grid_remove()


        
        self.navigation = Navigation(self)
        self.history = History(self.frame)
        self.search = Search(self)
        
        self.shortcut = Shortcut(self)
        
        

        self.results_canvas = tk.Canvas(self.browser_frame, width=1024, height=768)
        self.results_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.results_scrollbar = ttk.Scrollbar(self.browser_frame, orient=tk.VERTICAL, command=self.results_canvas.yview)
        self.results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(200, 0), pady=(0, 50))

        self.results_canvas.configure(yscrollcommand=self.results_scrollbar.set)
        self.results_canvas.bind("<Configure>", lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all")))

        self.results_frame_inner = ttk.Frame(self.results_canvas)
        self.results_canvas.create_window((0, 0), window=self.results_frame_inner, anchor="nw")

    def close_browser_tab(self):
        current_tab_index = self.notebook.index(self.notebook.select())
        self.notebook.forget(current_tab_index)

        if not self.notebook.tabs():
            self.root.destroy()

    def show_sign_in_dialog(self):
        sign_in_dialog = SignInDialog(self.root, self.authentication, self)
        self.root.wait_window(sign_in_dialog.top)

    def create_browser_tab(self):
        Tab(self.root, self.notebook)
    
    def clear_placeholder(self, event):
        if self.entry.get() == "Search or enter web address":
            self.entry.delete(0, tk.END)

    def update_tab_label(self, label_text):
        current_tab_index = self.notebook.index(self.notebook.select())
        self.notebook.tab(current_tab_index, text=f"{label_text[:15]} - Search") 
    
    def display_results(self, event=None):
        self.search.display_results(event)
        self.shortcut.remove()


    def clear_results(self):
        self.search.clear_results()
    
    def open_link(self, url):
        tampilWeb(url)
        self.history.clicked_urls.append(url)
        self.history.show_urls()
        
class Search:
    def __init__(self, tab):
        self.tab = tab
    
    def search(self, query):
        api_key = "[Secret_Key]"
        cx = "[Secret_CX]"
        url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={query}"
        response = requests.get(url)
        data = response.json()
        return data['items']
    
    def display_results(self, event=None):
        query = self.tab.entry.get()
        if not query == "Search or enter web address":
            if re.match(r"(https?://|www\.)\S+", query):
                self.tab.open_link(query)
            else:
                results = self.search(query)

            for widget in self.tab.results_frame_inner.winfo_children():
                widget.destroy()
                
            for item in results:
                title = item.get('title', 'No Title')
                link = item.get('link', 'No Link')

                if 'snippet' in item:
                    snippet = item['snippet']
                    max_snippet_length = 150
                    if len(snippet) > max_snippet_length:
                        snippet = snippet[:max_snippet_length] + '...'
                else:
                    snippet = item['title']

                title_label = ttk.Label(self.tab.results_frame_inner, text=title, foreground='blue',
                                        font=('Arial', 16, 'bold'), cursor='hand2')
                title_label.pack(anchor='w')
                title_label.bind("<Button-1>", lambda event, url=link: self.tab.open_link(url))

                ttk.Label(self.tab.results_frame_inner, text=snippet).pack(anchor='w')
                link_label = ttk.Label(self.tab.results_frame_inner, text=link, foreground='blue',
                                       cursor='hand2')
                link_label.pack(anchor='w')
                link_label.bind("<Button-1>", lambda event, url=link: self.tab.open_link(url))

                ttk.Separator(self.tab.results_frame_inner, orient='horizontal').pack(fill='x', pady=10)

            self.tab.browser_frame.grid()
            self.tab.results_frame_inner.update_idletasks()
            self.tab.results_canvas.configure(
                scrollregion=self.tab.results_canvas.bbox("all"))

            self.tab.search_displayed = True
            self.tab.navigation.update_history(query)
            self.tab.history.add_to_history(query)

            # Update the tab label
            self.tab.update_tab_label(query)

    def clear_results(self):
        self.tab.browser_frame.grid_remove()
        self.tab.search_displayed = False

class WebBrowser:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Web Browser")

        style = ttk.Style()
        style.configure("TNotebook", padding=(5, 5), foreground="black", background="green")

        self.notebook = ttk.Notebook(self.root, style="TNotebook")
        self.notebook.pack(fill='both', expand=True)

        Tab(self.root, self.notebook)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        self.root.destroy()
    
class Navigation:
    def __init__(self, search):
        self.search = search

        self.forward_image = Image.open("R.png")
        self.forward_image = self.forward_image.resize((20, 20))
        self.forward_photo = ImageTk.PhotoImage(self.forward_image)

        self.backward_image = Image.open("L.png")
        self.backward_image = self.backward_image.resize((20, 20))
        self.backward_photo = ImageTk.PhotoImage(self.backward_image)

        self.reload_image = Image.open("refresh.png")
        self.reload_image = self.reload_image.resize((20, 20))
        self.reload_photo = ImageTk.PhotoImage(self.reload_image)
        
        self.reload_button = ttk.Button(search.frame, image=self.reload_photo, command=self.reload_page)
        self.reload_button.grid(row=0, column=4, padx=5)

        self.forward_button = ttk.Button(search.frame, image=self.forward_photo, command=self.forward)
        self.forward_button.grid(row=0, column=3, padx=5)

        self.backward_button = ttk.Button(search.frame, image=self.backward_photo, command=self.backward)
        self.backward_button.grid(row=0, column=2, padx=5)

        self.history = []
        self.current_index = -1
            
    def forward(self):
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            url = self.history[self.current_index]
            self.search.entry.delete(0, tk.END)
            self.search.entry.insert(0, url)
            self.search.display_results()
            self.search.shortcut.remove()

    def backward(self):
        if self.search.search_displayed:
            self.search.clear_results()
            self.search.entry.delete(0, tk.END)
            self.search.entry.insert(0, "Search or enter web address")
            self.search.shortcut.tampil()
            
        elif self.current_index > 0:
            
            self.current_index -= 1
            url = self.history[self.current_index]
            self.search.entry.delete(0, tk.END)
            self.search.entry.insert(0, "Search or enter web address")

    
    def reload_page(self):
        self.search.results_frame_inner.destroy()
        self.search.results_frame_inner = ttk.Frame(self.search.results_canvas)
        self.search.results_canvas.create_window((0, 0), window=self.search.results_frame_inner, anchor="nw")
        if not self.search == "Search or enter web address":
            self.search.display_results()
            self.search.shortcut.remove()
            

    def update_history(self, url):
        self.history.append(url)

class Shortcut:
    def __init__(self, shortcut):
        self.shortcut = shortcut
        
        self.google_image = Image.open("google.png")
        self.google_image = self.google_image.resize((20, 20))
        self.google_photo = ImageTk.PhotoImage(self.google_image)
        
        self.google_button = ttk.Button(shortcut.frame, image=self.google_photo, command=self.google)
        self.google_button.grid(row=2, column=6, padx=10)
        
        self.youtube_image = Image.open("youtube.png")
        self.youtube_image = self.youtube_image.resize((20, 20))
        self.youtube_photo = ImageTk.PhotoImage(self.youtube_image)
        
        self.youtube_button = ttk.Button(shortcut.frame, image=self.youtube_photo, command=self.youtube)
        self.youtube_button.grid(row=2, column=7, padx=10)
    
        self.facebook_image = Image.open("facebook.png")
        self.facebook_image = self.facebook_image.resize((20, 20))
        self.facebook_photo = ImageTk.PhotoImage(self.facebook_image)
        
        self.facebook_button = ttk.Button(shortcut.frame, image=self.facebook_photo, command=self.facebook)
        self.facebook_button.grid(row=2, column=8, padx=10)
        
        self.ytmusic_image = Image.open("ytmusic.png")
        self.ytmusic_image = self.ytmusic_image.resize((20, 20))
        self.ytmusic_photo = ImageTk.PhotoImage(self.ytmusic_image)
        
        self.ytmusic_button = ttk.Button(shortcut.frame, image=self.ytmusic_photo, command=self.ytmusic)
        self.ytmusic_button.grid(row=2, column=9, padx=10)
        
    def google(self):
        tampilWeb("https://google.com")
    
    def youtube(self):
        tampilWeb("https://youtube.com")

    def facebook(self):
        tampilWeb("https://facebook.com")
        
    def ytmusic(self):
        tampilWeb("https://music.youtube.com")    
        
    
    def remove(self):
        self.google_button.grid_forget()
        self.youtube_button.grid_forget()
        self.facebook_button.grid_forget()
        self.ytmusic_button.grid_forget()
    
    def tampil(self):
        self.google_button.grid(row=2, column=6, padx=10)
        self.youtube_button.grid(row=2, column=7, padx=10)
        self.facebook_button.grid(row=2, column=8, padx=10)
        self.ytmusic_button.grid(row=2, column=9, padx=10)
        
        
class tampilWeb:
    def __init__(self, url):
        self.url = url
        webview.create_window(width=1280, height=720, title=url, url=url)
        webview.start()
        

if __name__ == "__main__":
    webbrowser = WebBrowser()


#Garis new tab ganti warna
#ketika di back shortcut hilnag
