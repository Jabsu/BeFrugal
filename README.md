# BeFrugal

Import your bank transactions from your clipboard or from a file. Create categories for payers and recipients. Keep track of your monthly savings/spendings and yearly averages. Be smart. BeFrugal.

**Work in progress! Current status: *alpha*, for what it's worth. The main functionality is implemented, though. See TODO.md for upcoming features/fixes.**

## Features
- Clean UI — achieved with ~~CryEngine~~ Qt (PySide)
- Intelligent data importing
    - Import from a text file or clipboard: almost no formatting restrictions, the only requirement is that the entries should be separated by newlines
    - Smart formatting detection: tries to guess the value separator, the indexes for date/amount/entity values, and the date formatting
    - If the above fails, you can configure the indexes and date format yourself; the program validates these for you so you don't have to worry too much about making mistakes
    - Configuration presets: if the formatting in your imports tends to vary, no need to adjust the configurations every time
- Create categories for entities (payers/recipients) and keep track of the monthly differences and yearly averages
- Quickly calculate how long it would take to save X amount of money according to your net averages

## Installation
1. Install Python 3.8+ 
2. Clone the repository: `git clone https://github.com/Jabsu/BeFrugal.git`
3. Install the required modules: `pip install -U -r requirements.txt`
4. Run the program: `python main.py`
