import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring

from main import login_naver, get_comments, extract_comments, save_to_excel


def naver_login():
    try:
        login_naver()
    except Exception as e:
        messagebox.showerror("Error", "Login failed")

def create_excel():
    new_window = tk.Toplevel(root)
    new_window.geometry("300x200")
    new_window.title("구매자 분석")

    def execute():
        blog_post_url = url_entry.get()
        try:
            soup = get_comments(blog_post_url)
            comments = extract_comments(soup)
            save_to_excel(comments)
        except Exception as e:
            messagebox.showerror("Error", "Excel creation failed")

    url_label = tk.Label(new_window, text="Posting URL:")
    url_label.pack()

    url_entry = tk.Entry(new_window)
    url_entry.pack()

    generate_button = tk.Button(new_window, text="Create\nExcel", command=execute)
    generate_button.pack()

def send_book():
    # Function to send the book goes here.
    pass

root = tk.Tk()
root.geometry("400x300")

login_button = tk.Button(root, text="Naver\nLogin", command=naver_login)
login_button.pack()

create_excel_button = tk.Button(root, text="Create\nExcel", command=create_excel)
create_excel_button.pack()

send_button = tk.Button(root, text="Send\nE-Book", command=send_book)
send_button.pack()

root.mainloop()
