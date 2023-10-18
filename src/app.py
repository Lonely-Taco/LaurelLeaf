import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, askokcancel
import os
import shutil
from bs4 import BeautifulSoup
import re

# Create the root window
root = tk.Tk()
root.title('Choose Folder')
root.resizable(False,False)

window_width = 500
window_height = 250

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    root.geometry(f"{width}x{height}+{x}+{y}")
    
def remove_head_scripts(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    head = soup.find('head')
    if head:
        scripts = head.find_all('script')
        for script in scripts:
            script.extract()  # Remove the script tag
    return str(soup)

def remove_nav_and_div(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove <nav></nav> tags
    nav = soup.find('nav')
    if nav:
        nav.extract()
    
    # Check for a second <header>
    headers = soup.find_all('header')
    if len(headers) > 0:
        second_header = headers[0]
        divs = second_header.find_all('div')
        for div in divs:
            div.extract()  # Remove <div></div> tags in the second header
    
    return str(soup)

def remove_string_from_links(html_content, string_to_remove):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('link')
    for link in links:
        if string_to_remove in link['href']:
            link['href'] = link['href'].replace(string_to_remove, '')
    return str(soup)

def remove_string_from_images(html_content, string_to_remove):
    soup = BeautifulSoup(html_content, 'html.parser')
    images = soup.find_all('img')
    for image in images:
        if string_to_remove in image.get('src', ''):
            image['src'] = image.get('src', '').replace(string_to_remove, '')
    return str(soup)

def remove_url_from_anchor_tags(html_content):
        
    github_pattern = r'https:\/\/github\.com\/[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+'
    
   # Find all links in the modified content
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a')
        
        # Filter links that match the GitHub repository pattern and keep them
    for link in links:
        href = link.get('href')
        if href and re.match(github_pattern, href) and skip_github_urls_var.get():
            continue  # Keep the link
        else:
            link['href'] = ''
    return str(soup)

def process_files(folder):
    html_files = [f for f in os.listdir(folder) if f.endswith(".html")]
    
    # Create the "_files" folder if it doesn't exist
    files_folder = os.path.join(folder, "_files")
    if not os.path.exists(files_folder):
        os.makedirs(files_folder)
    
    
     
    for file_name in html_files:
        file_path = os.path.join(folder, file_name)
        
        # Extract the filename without the ".html" extension
        base_filename = os.path.splitext(file_name)[0]
        
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        modified_content = remove_head_scripts(html_content)
        modified_content = remove_nav_and_div(modified_content)
        modified_content = remove_string_from_links(modified_content, base_filename)
        modified_content = remove_string_from_images(modified_content, base_filename)
        
        if remove_urls_var.get():
            modified_content = remove_url_from_anchor_tags(modified_content)
            
        print(base_filename)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
            
def get_subfolders(root_folder):
    subfolders = [f for f in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, f))]
    return subfolders

def get_files(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return files

def copy_files(files, source_folder, destination_folder):
    for filename in files:
        source_file = os.path.join(source_folder, filename)
        destination_file = os.path.join(destination_folder, filename)
        if os.path.exists(destination_file):
            os.remove(destination_file)  # Remove existing file
        shutil.copy2(source_file, destination_file)  # Copy the file
        
def delete_subfolder_with_confirmation(subfolder_path):
    # Ask the user for confirmation before deleting the subfolder
    confirm_delete = askokcancel("Confirmation", f"Do you want to delete '{subfolder_path}'?")
    if confirm_delete:
        shutil.rmtree(subfolder_path)
    else:
        print(f"Deletion of '{subfolder_path}' canceled.")

def confirm_selection(folder):
    confirm_selection = askokcancel("Confirmation", f"Confirm path: '{folder}'")
    return confirm_selection
    

def select_folder():
    folder = fd.askdirectory(
        title='Select a Folder',
        initialdir='/'
    )
    if folder:
        folder_path_label.config(text=f"Chosen Folder: {folder}")  # Update the label with the chosen folder path

    if folder and confirm_selection(folder):
        
        process_files(folder)
        destination_folder = os.path.join(folder, "_files")
        subfolders = get_subfolders(folder)
        if subfolders:
            for subfolder in subfolders:
                 if subfolder != "_files" and not skip_subfolders_var.get(): 
                    files_path = os.path.join(folder, subfolder)
                    files = get_files(files_path)
                    copy_files(files, files_path ,destination_folder)
                    print(f"Subfolder: {subfolder}")
                    
                     # Prompt the user to delete the subfolder
                    delete_subfolder_with_confirmation(files_path)
                  
        else:
            showinfo(
                title='Nothing found',
                message=f'No subfolders in directory.'
            )
    showinfo(
            title='Processing Complete',
            message=f'Process complete.'
        )   
    
skip_subfolders_var = tk.BooleanVar(value=False)  # Default value is False
remove_urls_var = tk.BooleanVar(value=True)  # Default value is False
skip_github_urls_var = tk.BooleanVar(value=True)  # Default value is False

check_can_remove_external_links = ttk.Checkbutton(
    root,
    text='Remove links to external sources?',
   variable=remove_urls_var
)

check_can_remove_github_links = ttk.Checkbutton(
    root,
    text='Skip links to GitHub?',
    variable=skip_github_urls_var,
)

open_button = ttk.Button(
    root,
    text='Select a Folder',
    command=select_folder
)


skip_subfolders_checkbox = ttk.Checkbutton(
    root,
    text='Skip Subfolders',
    variable=skip_subfolders_var,
)


check_can_remove_external_links.grid(row=0, column=0, sticky="w", padx=10)
check_can_remove_github_links.grid(row=1, column=0, sticky="w", padx=10)
skip_subfolders_checkbox.grid(row=2, column=0, sticky="w", padx=10)

# Create a Label widget to display the chosen folder path
folder_path_label = ttk.Label(root, text="Chosen Folder: None")
folder_path_label.grid(row=9, column=0, columnspan=5, padx=10)

tk.Label(root, text="").grid(row=3)

open_button.grid(columnspan=4)

center_window(root, window_width, window_height)

root.mainloop()
