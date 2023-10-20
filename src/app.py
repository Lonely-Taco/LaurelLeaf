import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, askokcancel
import os
import shutil
from bs4 import BeautifulSoup
import re
import pdfkit
import json

root = tk.Tk()
root.title('LaurelLeaf')
root.resizable(False,False)

window_width = 600
window_height = 400

def load_settings():
    settings = {}
    try:
        with open("settings.json", "r") as file:
            settings = json.load(file)
            print(settings)
    except FileNotFoundError:
        pass
    return settings

def save_settings(settings):
   config = {
        "wkhtmltopdf_path": settings,
   }
   with open("settings.json", "w") as file:
        json.dump(config, file, indent=4)
        
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
            
    print(f"Removed scripts from header: {len(scripts)} script tags")
    return str(soup)

def remove_head_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    head = soup.find('head')
    if head:
        scripts = head.find_all('link')
        for script in scripts:
            script.extract()  # Remove the script tag
            
    print(f"Removed head links: {len(scripts)} link tags")
    
    return str(soup)

def remove_head_meta_tags(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    head = soup.find('head')
    if head:
        scripts = head.find_all('meta')
        for script in scripts:
            script.extract()  # Remove the script tag
            
    meta_tag = '<meta content="text/html; charset=UTF-8" http-equiv="Content-Type"/>'
    
    meta_element = BeautifulSoup(meta_tag, 'html.parser')

    head.insert(position=0, new_child=meta_element)
    
    print(f"Removed head meta tags: {len(scripts)} meta tags. (Keeping meta tag with charset for better pdf converstion)")
    
    return str(soup)

def remove_style_tags_with_data_emotion(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    style_tags = soup.find_all('style', attrs={'data-emotion': True})
    
    for style_tag in style_tags:
        style_tag.extract()  # Remove the style tag from the HTML content

    print(f"Removed: {len(style_tags)} style tags with data-emotion")

    return str(soup)

def add_extra_div_after_body(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')    
    body = soup.find('body')
    
    if body:
        div = '<div></div>'
        div_element = BeautifulSoup(div, 'html.parser')    
        body.insert_after(div_element)
        body.insert(position=0, new_child=div_element)
        
    return str(soup) 
  
def remove_attributes_from_div_section_main_tags(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove attributes from div tags
    div_tags = soup.find_all('div')
    for div_tag in div_tags:
        for attribute in list(div_tag.attrs):
            del div_tag[attribute]
    
    # Remove attributes from section tags
    section_tags = soup.find_all('section')
    for section_tag in section_tags:
        for attribute in list(section_tag.attrs):
            del section_tag[attribute]
    
    # Remove attributes from main tags
    main_tags = soup.find_all('main')
    for main_tag in main_tags:
        for attribute in list(main_tag.attrs):
            del main_tag[attribute]

    print(f"Removed attributes from divs, sections, and main tags: {len(div_tags)}, {len(section_tags)},  {len(main_tags)}")

    return str(soup)

def remove_iframe_tags(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    iframes = soup.find_all('iframe')
    if iframes:
        for frame in iframes:
            frame.extract()
            
    print(f"Changed: {len(iframes)} iframes")
    
    return str(soup)

def remove_hidden_button(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove button tags
    button_tags = soup.find_all('button')
    for button_tag in button_tags:
        button_tag.extract()  # Remove the button element

    print(f"Buttons removed: {len(button_tags)}")
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
    print(f"Changed: {len(links)} links")
    
    return str(soup)

def remove_string_from_images(html_content, string_to_remove):
    soup = BeautifulSoup(html_content, 'html.parser')
    images = soup.find_all('img')
    for image in images:
        if string_to_remove in image.get('src', ''):
            image['src'] = image.get('src', '').replace(string_to_remove, '')
    
    print(f"Changed: {len(images)} imgs")
    
    return str(soup)

def remove_string_from_script_tags(html_content, string_to_remove):
    soup = BeautifulSoup(html_content, 'html.parser')
    script_tags = soup.find_all('script')

    for script_tag in script_tags:
        src = script_tag.get('src', '')
        if string_to_remove in src:
            script_tag['src'] = src.replace(string_to_remove, '')

    print(f"Changed: {len(script_tags)} script tags")
    
    return str(soup)

def remove_url_from_anchor_tags(html_content):   
    github_pattern = r'https:\/\/github\.com\/[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+'
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if href and re.match(github_pattern, href) and skip_github_urls_var.get():
            continue  # Keep the link
        else:
            link['href'] = ''
    
    print(f"Removed: {len(links)} links")
    return str(soup)

def process_files(folder):
    html_files = [f for f in os.listdir(folder) if f.endswith(".html")]
    files_folder = os.path.join(folder, "_files")
    if not os.path.exists(files_folder):
        os.makedirs(files_folder)
    
    
     
    for file_name in html_files:
        file_path = os.path.join(folder, file_name)
        base_filename = os.path.splitext(file_name)[0]
        
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        modified_content = remove_head_scripts(html_content)
        modified_content = remove_nav_and_div(modified_content)
        modified_content = remove_head_links(modified_content)
        modified_content = remove_head_meta_tags(modified_content)
        modified_content = remove_string_from_links(modified_content, base_filename)
        modified_content = remove_string_from_images(modified_content, base_filename)
        modified_content = remove_string_from_script_tags(modified_content, base_filename)
        modified_content = remove_iframe_tags(modified_content)
        modified_content = add_extra_div_after_body(modified_content)
        modified_content = remove_attributes_from_div_section_main_tags(modified_content)
        modified_content = remove_hidden_button(modified_content)
        # modified_content = remove_style_tags_with_data_emotion(modified_content)
        
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
    confirm_delete = askokcancel("Confirmation", f"Do you want to delete '{subfolder_path}'?")
    if confirm_delete:
        shutil.rmtree(subfolder_path)
    else:
        print(f"Deletion of '{subfolder_path}' canceled.")

def confirm_selection(folder):
    confirm_selection = askokcancel("Confirmation", f"Confirm path: '{folder}'")
    return confirm_selection
    
def convert_to_pdf(input_folder, output_folder, wkhtmltopdf_path):
    # settings = load_settings()
    # if 'wkhtmltopdf_path' not in settings:
    #     showinfo(
    #             title='No wkhtmltopdf',
    #             message=f'No wkhtmltopdf executable found'
    #         )
    #     return
    
    options = {
        'page-size': 'Letter',
        'margin-top': '10mm',
        'margin-right': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm',
        '--debug-javascript': None,  
        '--enable-local-file-access': None,
        '--disable-external-links': None,
        '--zoom': '.9',
        '--minimum-font-size': '20',
        '--quiet': None,
    }
    # wkhtmltopdf_path = settings["wkhtmltopdf_path"]
    configuration = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

    html_files = [f for f in os.listdir(input_folder) if f.endswith(".html")]
    for html_file in html_files:
        input_path = os.path.join(input_folder, html_file)
        output_file = os.path.splitext(html_file)[0] + '.pdf'
        output_path = os.path.join(output_folder, output_file)

        try:
            pdfkit.from_file(input_path, output_path, configuration=configuration, options=options)
            print(f"{html_file} to PDF complete")
        except Exception as e:
            e = e.with_traceback(e.__traceback__)
          
            print(f"Error converting {input_path} to PDF: {repr(e)}")
  
    showinfo(
        title='Conversion Complete',           
        message=f'{len(html_files)} HTML files converted to PDF.'
    )

def select_input_folder():
    global selected_input_folder
    global asset_path
    selected_input_folder = fd.askdirectory(title="Select Input Folder", initialdir="/")    
    if selected_input_folder:
        input_folder_entry.delete(0, tk.END)
        input_folder_entry.insert(0, selected_input_folder)

def select_output_folder():
    global selected_output_folder
    selected_output_folder = fd.askdirectory(title="Select Output Folder", initialdir="/")
    if selected_output_folder:
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, selected_output_folder)
        
def select_folder():  
    folder = fd.askdirectory(
        title='Select a Folder',
        initialdir='/'
    )
    if folder:
        folder_path_label.config(text=f"Chosen Folder: {folder}")  # Update the label with the chosen folder path

    if folder and confirm_selection(folder):   
        selected_input_folder = folder
        selected_output_folder = folder
        
        output_folder_entry.delete(0, tk.END)
        input_folder_entry.delete(0, tk.END)
        
        
        output_folder_entry.insert(0, selected_output_folder)
        input_folder_entry.insert(0, selected_input_folder)
        
        process_files(folder)
        destination_folder = os.path.join(folder, "_files")
        subfolders = get_subfolders(folder)
        if subfolders:
            for subfolder in subfolders:
                 if subfolder != "_files" and not skip_subfolders_var.get(): 
                    files_path = os.path.join(folder, subfolder)
                    files = get_files(files_path)
                    copy_files(files, files_path ,destination_folder)
                    
                    print(f"Subfolder: {subfolder} containing {len(files)} copied.")
                    
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
    





def create_settings_tab(tab_control):
    settings_tab = ttk.Frame(tab_control)
    tab_control.add(settings_tab, text="Settings")

    # Create and pack or grid your widgets for settings in the settings_tab frame.
    # For example, you can add an entry field for wkhtmltopdf_path.

    wkhtmltopdf_label = tk.Label(settings_tab, text="wkhtmltopdf Path:")
    wkhtmltopdf_entry = tk.Entry(settings_tab)
    
    save_button = tk.Button(
        settings_tab, 
        text="Save Settings",
        command=lambda: save_settings(wkhtmltopdf_entry.get())
        )

    wkhtmltopdf_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    wkhtmltopdf_entry.grid(row=0, column=1, padx=10, pady=10)
    save_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

def create_main_tab(tab_control):
    global selected_input_folder
    global selected_output_folder
    
    main_tab = ttk.Frame(tab_control)
    tab_control.add(main_tab, text="LaurelLeaf")
    
    global input_folder_entry
    input_folder_entry= ttk.Entry(main_tab)
    global output_folder_entry
    output_folder_entry = ttk.Entry(main_tab)
 
    global skip_subfolders_var
    skip_subfolders_var = tk.BooleanVar(value=False)  # Default value is False
    global remove_urls_var
    remove_urls_var = tk.BooleanVar(value=True)  # Default value is False
    global skip_github_urls_var
    skip_github_urls_var = tk.BooleanVar(value=True)  # Default value is False

    open_button = ttk.Button(
        main_tab,
        text='Select a Folder',
        command=select_folder
    )

    check_can_remove_external_links = ttk.Checkbutton(
        main_tab,
        text='Remove links to external sources?',
    variable=remove_urls_var
    )

    check_can_remove_github_links = ttk.Checkbutton(
        main_tab,
        text='Skip links to GitHub?: only matters if remove links is checked.',
        variable=skip_github_urls_var,
    )

    skip_subfolders_checkbox = ttk.Checkbutton(
        main_tab,
        text='Skip Subfolders: If checked, you will be prompted before deletion.',
        variable=skip_subfolders_var,
    )
    convert_button = ttk.Button(
        main_tab,
        text='Convert to PDF',
        command=lambda: convert_to_pdf(selected_input_folder, selected_output_folder, wkhtmltopdf_path='F:\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    )

    tk.Label(main_tab, text="Step: 1 choose folder to clean").grid(row=1, sticky="w")

    # Create a Label widget to display the chosen folder path
    global folder_path_label
    folder_path_label = ttk.Label(main_tab, text="Chosen Folder: None")
    
    folder_path_label.grid(row=2, column=0, columnspan=10, sticky="w")
    open_button.grid(row=3, column=1, columnspan=1, sticky="w")

    check_can_remove_external_links.grid(row=4, column=0, sticky="w", padx=10)
    check_can_remove_github_links.grid(row=5, column=0, sticky="w", padx=10, columnspan=5)

    skip_subfolders_checkbox.grid(row=6, column=0, sticky="w", padx=10, columnspan=10)


    tk.Label(main_tab, text="Step: 2 make pdf. (optional) ").grid(row=12, sticky="w")


    input_folder_label = ttk.Label(main_tab, text="Input Folder:")
    output_folder_label = ttk.Label(main_tab, text="Output Folder:")


    input_folder_label = ttk.Label(main_tab, text="Input Folder:")
    input_folder_label.grid(row=14, column=0)

    output_folder_label = ttk.Label(main_tab, text="Output Folder:")
    output_folder_label.grid(row=15, column=0)


    input_folder_button = ttk.Button(main_tab, text="Browse", command=select_input_folder)
    input_folder_button.grid(row=14, column=2, sticky="w")
    input_folder_entry.grid(row=14, column=1)

    output_folder_button = ttk.Button(main_tab, text="Browse", command=select_output_folder)
    output_folder_button.grid(row=15, column=2, sticky="w")
    output_folder_entry.grid(row=15, column=1)

    convert_button.grid(row=16, column=1, sticky="w")

tab_control = ttk.Notebook(root)

# Create the main content tab (e.g., the file processing tab).
# Add your widgets for the main functionality here.
create_main_tab(tab_control)

# Create the settings tab.
create_settings_tab(tab_control)

# Add the Notebook to your main window.
tab_control.grid()

root.mainloop()