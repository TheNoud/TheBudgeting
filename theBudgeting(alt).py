import csv
import os
import sys
import openpyxl

directory = '/Users/noudveeger/Documents/budget'
os.chdir(directory)

## Flow: take user input -> dataParse() parses it into variables which entryOutput() formats nicely and puts in csv file

# Function to edit parsed data for nicer formatting/entering categories and add them to csv file
def entryOutput(date,payee,inflow,outflow,outputWriter):
    category = ''
    # Replace date formats:
    date = date.replace(' Jan ','/1/')
    date = date.replace(' Feb ','/2/')
    date = date.replace(' Mar ','/3/')
    date = date.replace(' Apr ','/4/')
    date = date.replace(' May ','/5/')
    date = date.replace(' Jun ','/6/')
    date = date.replace(' Jul ','/7/')
    date = date.replace(' Aug ','/8/')
    date = date.replace(' Sep ','/9/')
    date = date.replace(' Oct ','/10/')
    date = date.replace(' Nov ','/11/')
    date = date.replace(' Dec ','/12/')

    # Replace unnecessary (POS, CNC) and problem causing stuff:
    payee = payee.replace('POS ', '')
    payee = payee.replace('CNC ', '')
    payee = payee.replace('(', '')
    payee = payee.replace(')', '')

    # Remove the date and all subsequent info from the payee
    splitPayee = payee.split(' ')
    for entry in splitPayee:
        if "/" in entry:
            # Make payee equal to the joining of splitPayee up until the date entry
            payee = " ".join(splitPayee[:splitPayee.index(entry)])

    # Change category and payee if it's a standard payment
    if "ARAMARK" in payee:
        payee = "ARAMARK"
        category = "Work lunch"
    if "STEAMGAMES" in payee:
        payee = "Steam Game"
        category = "Gadgets + games"
    if "Spotify" in payee:
        payee = "Spotify"
        category = "Spotify"
    if "MIP*3IRELAND" in payee:
        payee = "3 Phone Top up"
        category = "Mobile phone"
    if "SUPERVALU" in payee:
        payee = "SUPERVALU"
        category = "Groceries"       
    # Remove comma indicating thousands, as it causes problems
    if "," in inflow:
        inflow = inflow.replace(",", '')
    if "," in outflow:
        outflow = outflow.replace(",", '')

    outputDataList = [date,payee,category,'',outflow,inflow]
    print(outputDataList)
    outputWriter.writerow(outputDataList)
##    outputWriter.writerow([date+','+payee+','+ category +','+''+','+outflow+','+inflow])



# Function to parse initial data into usable variables
def dataParse(data,outputWriter):
    entry_lines = data.split("\n")
    line = 0
    max_line = len(entry_lines)-1
    
    while True:
        entry_items = entry_lines[line].split("\t")
        date = entry_items[0]
        payee=entry_items[1]
        
##try/except statement to catch error with inflow being pasted with new line
##between date and payee    
        try:
            inflow=entry_items[2]
        except IndexError:
            entry_items = entry_lines[line+1].split("\t")
            payee=entry_items[0]
            entry_items = entry_lines[line+2].split("\t")
##          In order to differentiate outflow from inflow (eg salary) pasted in new line, check if the second line is empty:
            inflow = ''
            outflow = ''
            if entry_items[1] == '':
                inflow = entry_items[0]
            else:
                outflow=entry_items[0]
            
            entryOutput(date,payee,inflow,outflow,outputWriter)
            line += 3
            continue
                
        outflow=entry_items[3]
        
##      skip if inflow/outflow is empty:
        if inflow == "" and outflow == "":
            line+=1
            continue
        entryOutput(date,payee,inflow,outflow,outputWriter)
        
        if line < max_line-1:
            line += 1
        else:
            break



# Take input from user for normal Account
print("Please paste the data here, followed by ctrl+z and Enter (Enter and ctrl+d on Mac!)")

# Prep CSV file
budgetCsvFile = open('budget-import.csv', 'w', newline='', encoding='utf-8')
budgetCsvWriter = csv.writer(budgetCsvFile, delimiter = ',')

# First row has to contain this format:    
budgetCsvWriter.writerow(['Date','Payee','Category','Memo','Outflow','Inflow'])

outputFile = budgetCsvFile
outputWriter = budgetCsvWriter
data = sys.stdin.read()
print(data)

# Go through functions flow:
dataParse(data,outputWriter)

outputFile.close()

print("\nDone! The 'budget-import.csv' file can be found in '%s'" % (os.getcwd()) )
