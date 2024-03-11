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
    table_path = "/home/rapha/Documents/Tutorials/LaTeX_Report_Measuring/scripts/table_test.csv"

    image_path = '/home/rapha/Documents/Tutorials/LaTeX_Report_Measuring/scripts/progress_plot.png'

    main_tex_folder = "/home/rapha/Documents/Tutorials/LaTeX_Report_Measuring/"
    main_tex_name = "main.tex"

    main_pdf_path = "/home/rapha/Documents/Tutorials/LaTeX_Report_Measuring/main.pdf"

    git_folder = "/home/rapha/Documents/Tutorials/LaTeX_Report_Measuring/"
    ###################################################################

    table_exists = exists(table_path)

    # This part initializes the table if it doesn't exist
    if not table_exists:
        with open(table_path, 'w', newline='', encoding="utf8") as file:
            writer = csv.writer(file)
            # You can customize other fields you want to
            # monitor in this part
            header = ["days_from_init","pages","words","diffs"]
            writer.writerow(header)

    # Calculating the first column
    days_from_init = get_days(init_date)
    print(f"Today it has been {days_from_init} days since the start of the tracking.")

    # Calculating the second column
    words = get_words(main_tex_folder,main_tex_name)
    print(f"This commit has a total of {words} words.")

    # Calculating the third column
    pages = get_pages(main_pdf_path)
    print(f"This commit has a total of {pages} pages.")

    # Calculating the fourth column
    diffs = get_diffs(git_folder)
    print(f"This commit has a total of {diffs} changes.")


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

    # you have to change this part if you want to add new stuff
    if index_redo.size == 0:
        newline = np.array([days_from_init,pages,words,diffs], dtype=str)
        table = np.vstack([table, newline])
    else:
        # this col should not be overriden
        # but rather added to the previous
        old_diffs = table[index_redo.item(),3]

        diff_sum = int_zero_assumption(diffs) + int_zero_assumption(old_diffs)
        newline = np.array([days_from_init,pages,words,diff_sum], dtype=str)

        table[index_redo.item(),:] = newline

    # saving the new array
    np.savetxt(table_path, table, delimiter=',', fmt='%s')


    plotting(table,image_path)

    print(f"Table written at:\n\t{table_path}")
    print(f"Image written at:\n\t{image_path}")

    return 0

######################## Helper functions ###########################
def get_days(date_init):
    """
    Calculates the number of days between the given initial date and the current date.

    Args:
        date_init (datetime.date): The initial date.

    Returns:
        int: The number of days between the initial date and the current date.

    Raises:
        ValueError: If the initial date is after the current date.
    """
    cur_date = date.today()
    if cur_date < date_init:
        raise ValueError("Init date has to come before or equal to today.")
    return (cur_date - date_init).days

def get_words(main_tex_folder: str, main_tex_name: str) -> str:
    """
    Get the total number of words in a LaTeX document.

    Args:
        main_tex_folder (str): The folder where the main LaTeX file is located.
        main_tex_name (str): The name of the main LaTeX file.

    Returns:
        str: The total number of words in the LaTeX document.

    Raises:
        subprocess.CalledProcessError: If the `texcount` or `awk` commands fail to execute.

    Note:
        The `texcount` command is part of the TeX Live distribution.
        `awk` is used to filter the sum of words from the texcount output.
    """
    texcount = ["texcount", main_tex_name, "-inc", "-total", "-sum"]
    awk = ["awk", "/Sum count:/ {print $NF}"]

    p = subprocess.Popen(texcount, cwd=main_tex_folder, stdout=subprocess.PIPE)
    output = subprocess.check_output(awk, stdin=p.stdout)
    p.wait()

    return output.decode().rstrip()

def get_pages(main_pdf_path: str) -> str:
    """
    Get the number of pages in a PDF file.

    Args:
        main_pdf_path (str): The path to the main PDF file.

    Returns:
        str: The number of pages in the PDF file.
        
    Raises:
        subprocess.CalledProcessError: If the `pdfinfo` or `awk` commands fail to execute.
    
    Note:
        The `pdfinfo` command is part of the poppler-utils package.
        `awk` is used to filter the number of pages from the pdfinfo output.
    """
    pdfinfo = ["pdfinfo", main_pdf_path]
    awk = ["awk", "/Pages:/ {print $NF}"]

    p = subprocess.Popen(pdfinfo, stdout=subprocess.PIPE)
    output = subprocess.check_output(awk, stdin=p.stdout)
    p.wait()

    return output.decode().rstrip()

def get_diffs(git_folder: str) -> str:
    """
    Get the total number of file changes, insertions, and deletions in a git repository.

    Args:
        git_folder (str): The path to the git repository folder.

    Returns:
        str: The total number of file changes, insertions, and deletions.

    Raises:
        subprocess.CalledProcessError: If the git command or awk command fails.
        
    Note:
        The `git` command is part of the git package.
        `awk` is used to filter the sum of changes from the git output.
    """
    # the --shortstat argument makes the report a single line
    diff = ["git", "diff", "HEAD", "--shortstat", git_folder]
    # files changes + insertions + deletions
    awk = ["awk", "{print $0+$4+$6}"]

    p = subprocess.Popen(diff, stdout=subprocess.PIPE)
    output = subprocess.check_output(awk, stdin=p.stdout)
    p.wait()

    return output.decode().rstrip()

def plotting(table: np.ndarray, image_path: str) -> int:
    """
    Plot the data from the given table and save the plot as an image.

    Parameters:
        table (np.ndarray): The input table containing the data to be plotted.
        image_path (str): The path where the plot image will be saved.

    Returns:
        int: 0 if the plot is successfully saved.

    """
    plot_table = table[1:,:].astype(int)
    plot_days = plot_table[:,0]
    plot_pages = plot_table[:,1]
    plot_words = plot_table[:,2]
    plot_diffs = plot_table[:,3]

    plt.rcParams.update({'font.size': 14})

    _, (axpages, axwords, axdiffs) = plt.subplots(3, 1, sharex=True,figsize=(10,10))

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

def int_zero_assumption(value: str) -> int:
    """
    Converts the given value to an integer. If the value is not a valid number,
    it assumes zero and returns it.

    Args:
        value (str): The value to be converted to an integer.

    Returns:
        int: The converted integer value or zero if the value is not a valid number.
    """
    try:
        return int(value)
    except ValueError:
        print("Value was an invalid number, assuming zero")
        return 0


if __name__ == "__main__":
    print("################### ~~ LaTeX Report Tracker ~~ ###################")
    main()
    print("################### ~~~~ End of execution ~~~~ ###################")
