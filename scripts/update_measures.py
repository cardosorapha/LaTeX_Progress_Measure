import csv
import subprocess
from os.path import exists
from datetime import date
import numpy as np
import matplotlib.pyplot as plt


def main():
    ############ Change this variable to your starting day ########
    init_date = date(2024,3,7)
    ###############################################################
    
    ############ Change these variables to the desired files ##########
    table_path = "./table_test.csv"
    
    image_path = './progress_plot.png'
    
    main_tex_folder = "../"
    main_tex_name = "main.tex"
    
    main_pdf_path = "../main.pdf"
    ###################################################################
    
    table_exists = exists(table_path)
    
    # This part initializes the table if it doesn't exist
    if not table_exists:
        with open(table_path, 'w', newline='') as file:
            writer = csv.writer(file)
            # You can customize other fields you want to 
            # monitor in this part
            header = ["days_from_init","pages","words","diffs"]
            writer.writerow(header)
    
    # Calculating the first column
    days_from_init = get_days(init_date)
    print(days_from_init)
    
    # Calculating the second column
    words = get_words(main_tex_folder,main_tex_name)
    print(words)
    
    # Calculating the third column
    pages = get_pages(main_pdf_path)
    print(pages)
    
    # Calculating the fourth column
    
    #todo
    diffs = 10
    
    
    # Read the whole table
    table = np.loadtxt(table_path,
                     delimiter=",", dtype=str)
    
    # Check if I have previous data on this day
    # If zero, no replace is necessary, should append
    # If one, should replace that line
    if table.ndim > 1:
        index_redo = np.argwhere(table[:,0] == str(days_from_init))
    else:
        # if first initialization, falls here
        # and should be an empty (to mimic the fact that it didn't find a match)
    	index_redo = np.array([])
    
    # this is the new line that we are going to include
    # you can customize it to match the header variable
    newline = np.array([days_from_init,pages,words,diffs], dtype=str)
    
    if index_redo.size == 0:
        table = np.vstack([table, newline])
    else:
        # this col should not be overriden
        # but rather added to the previous
        old_diffs = table[index_redo.item(),3]
        newline[3] = diffs + int(old_diffs)
        table[index_redo.item(),:] = newline
    
    # saving the new array
    np.savetxt(table_path, table, delimiter=',', fmt='%s')
    
    
    plotting(table,image_path)

def get_days(date_init):
    cur_date = date.today()
    if cur_date < date_init:
        raise Exception("Init date has to come before or equal to today.")
        return None
    else:
        return (cur_date - date_init).days

def get_words(main_tex_folder,main_tex_name):
    # assumes that the main tex file is located at
    # ./main_tex_folder/main_tex_name
    
    # texcount is found in the latex installation
    # it will give a report of words with the sum
    texcount = ["texcount", main_tex_name, "-inc", "-total", "-sum"]
    # I use awk to filter just the sum
    awk = ["awk", "/Sum count:/ {print $NF}"]
    
    p = subprocess.Popen(texcount, cwd = main_tex_folder, stdout=subprocess.PIPE)
    output = subprocess.check_output(awk, stdin=p.stdout)
    p.wait()

    words = output.decode().rstrip()
    
    return words

def get_pages(main_pdf_path):
    
    # texcount is found in the latex installation
    # it will give a report of words with the sum
    pdfinfo = ["pdfinfo", main_pdf_path]
    # I use awk to filter just the sum
    awk = ["awk", "/Pages:/ {print $NF}"]
    
    p = subprocess.Popen(pdfinfo, stdout=subprocess.PIPE)
    output = subprocess.check_output(awk, stdin=p.stdout)
    p.wait()

    pages = output.decode().rstrip()
    
    return pages

def get_diffs(git_folder):
    return diffs

def plotting(table, image_path):

    plot_table = table[1:,:].astype(int)
    plot_days = plot_table[:,0]
    plot_pages = plot_table[:,1]
    plot_words = plot_table[:,2]
    plot_diffs = plot_table[:,3]
    
    plt.rcParams.update({'font.size': 14})
    
    f, (axpages, axwords, axdiffs) = plt.subplots(3, 1, sharex=True,figsize=(10,10))
    
    axpages.plot(plot_days,plot_pages)
    axpages.set_ylabel("Total pages")
    axpages.yaxis.get_major_locator().set_params(integer=True)
    axpages.xaxis.get_major_locator().set_params(integer=True)
    
    axwords.plot(plot_days,plot_words)
    axwords.yaxis.get_major_locator().set_params(integer=True)
    axwords.set_ylabel("Total words")
    
    axdiffs.bar(plot_days,plot_diffs)
    axdiffs.yaxis.get_major_locator().set_params(integer=True)
    axdiffs.set_xlabel("Days since the start")
    axdiffs.set_ylabel("Changes per day")

    plt.savefig(image_path)
    plt.close()
    
    return 0


if __name__ == "__main__":
    main()
    
    
    
