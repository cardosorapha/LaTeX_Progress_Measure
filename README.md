# LaTeX Progress Measure

This repository contains:
- Sample LaTeX code for testing;
- Scripts for LaTeX compilation and measuring some useful metadada.

At the moment, we measure days since the start, number of pages, words, and modifications. The main script is located at `scripts/update_measures.py`. This script has some requirements:

- Unix operating system (Linux or Mac)
- LaTeX (I used Texlive), poppler, awk installed 
- Python 3 with numpy and matplotlib libraries. The others should be installed by default

You can execute the python script manually, but I have also included a pre-commit hook in the `scripts` folder that git will execute everything automatically if you follow the instructions ahead.

---

# How to use

1) Clone this repository

```
git clone https://github.com/cardosorapha/LaTeX_Progress_Measure.git
```

2) Navigate to the main repository folder

```
cd LaTeX_Progress_Measure
```

3) Make the pre-commit hook executable

```
chmod +x ./scripts/pre-commit
```

4) Copy the pre-commit hook to the appropriate git folder

```
cp ./scripts/pre-commit .git/hooks/pre-commit
```

Steps 1-4 only need to be executed once. Then, you can work with your files normally. To trigger the pre-commit hook, use

```
git commit
```

without any message. The scripts will executed and you will be prompted to write a message.

Furthermore, to avoid incorrect measurements, include logs and temporary files in `.gitignore`. I have already included a few. 

---

Measurements for this repository

<p align="center">
  
<img src="/scripts/progress_plot.png" alt="Measured progress"/>

</p>

---
If you have any questions, feel free to ask as an Issue or email me at cardosodeoliveir@gmail.com.

