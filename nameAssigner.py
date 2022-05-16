# imports and globals for the main program
from typing import Any
import pandas as pd
from numpy import ndarray
from numpy.random import default_rng
from pandas import Series
import os
import shutil

rng = default_rng()
bit_generator = rng.bit_generator

# check if the data directory exists. If it doesn't create it
if not os.path.exists("data"):
    os.mkdir("data")

# ask the user to put the csv file in the data directory and then press enter to continue
print("Please put the csv file in the data directory and press enter to continue ...")
input()

# Ask if user wants to format the 5th grade or 6th grade data
gradeToFormat = int(input("What grade would you like to format? Please enter a number between 1 and 6: "))
# check if the user input is valid and if not ask again
while gradeToFormat < 1 or gradeToFormat > 6:
    gradeToFormat = int(input("Please enter a number between 1 and 6."))

# check if the "output/AssignedNames" and "output/AssignedEmails" directories exist.
# If they exist empty them, and if they don't create them
if os.path.exists("output/AssignedNames"):
    shutil.rmtree("output/AssignedNames")
if os.path.exists("output/AssignedEmails"):
    shutil.rmtree("output/AssignedEmails")
os.mkdir("output/AssignedNames")
os.mkdir("output/AssignedEmails")

# ask the user to enter the name of the csv file
csvFileName = input("Please enter the name of the csv file: ")
# check if the user input ends with .csv and if not add it
if csvFileName[-4:] != ".csv":
    csvFileName += ".csv"
# check if the file exists and if not ask again
while not os.path.exists("data/" + csvFileName):
    csvFileName = input("Please enter a valid csv file name: ")
# set the path to the csv file
csvFilePath = "data/" + csvFileName
# read the csv file into a pandas dataframe
df = pd.read_csv(csvFilePath)

# sort the dataframe by the class column
df.sort_values(by=["class"], inplace=True)

# make an empty list to store the class names
classNames = []
# loop through the dataframe and add the class names to the list
for index, row in df.iterrows():
    classNames.append(row["class"])
# remove duplicates from the list
classNames = list(set(classNames))
# sort the list alphabetically
classNames.sort()

# make a variable to store the amount of classes
classAmount = len(classNames)

# set the index to the class
df.set_index("class", inplace=True)

# make a list to store the dataframes for all the classes
classDataFrames = []
# loop through the dataframe and add the dataframes to the list
for classes in classNames:
    classDataFrames.append(df.loc[classes])

# store the dataframes in a dictionary with the class names as keys
classDict = dict(zip(classNames, classDataFrames))

shuffledRows: dict[Series | None | ndarray | Any, Any] = {}
# loop through the dictionary and shuffle the rows
for key, value in classDict.items():
    # shuffle the rows
    shuffledRows[key] = value.sample(frac=1, random_state=bit_generator)

# print the shuffled rows for each class
for key, value in shuffledRows.items():
    print("\n" + key + ":")
    print(value)

# make a separate dictionary to store the names in the shuffled rows
shuffledNames = {}
# loop through the dictionary and add the names to the dictionary
for key, value in shuffledRows.items():
    # make a list to store the names
    names = []
    # loop through the rows and add the names to the list
    for index, row in value.iterrows():
        names.append(row["name"])
    # add the list to the dictionary
    shuffledNames[key] = names

# make a separate dictionary to store the emails in the shuffled rows
shuffledEmails = {}
# loop through the dictionary and add the emails to the dictionary
for key, value in shuffledRows.items():
    # make a list to store the emails
    emails = []
    # loop through the rows and add the emails to the list
    for index, row in value.iterrows():
        emails.append(row["email"])
    # add the list to the dictionary
    shuffledEmails[key] = emails

# take the first name + " -> " + the next name in the dictionary and add it to a dictionary named AssignedNames
# the last name should be assigned to the first name of that class
AssignedNames = {}
# loop through the dictionary and add the names to the dictionary
for key, value in shuffledNames.items():
    # make a list to store the names
    names = []
    # loop through the names and add the names to the list
    for index, name in enumerate(value):
        # check if the index is the last index
        if index == len(value) - 1:
            # add the name to the list
            names.append(name + " -> " + value[0])
        else:
            # add the name to the list
            names.append(name + " -> " + value[index + 1])
    # add the list to the dictionary
    AssignedNames[key] = names

# take the first email + " -> " + the next email in the dictionary and add it to a dictionary named AssignedEmails
# the last email should be assigned to the first email of that class
AssignedEmails = {}
# loop through the dictionary and add the emails to the dictionary
for key, value in shuffledEmails.items():
    # make a list to store the emails
    emails = []
    # loop through the emails and add the emails to the list
    for index, email in enumerate(value):
        # check if the index is the last index
        if index == len(value) - 1:
            # add the email to the list
            emails.append(email + " -> " + value[0])
        else:
            # add the email to the list
            emails.append(email + " -> " + value[index + 1])
    # add the list to the dictionary
    AssignedEmails[key] = emails

# wait for the user to press enter
input("\nPress enter to save the files...")

# save the assigned names for each class to a txt file named after the class and "AssignedNames.txt"
# in the output folder
for key, value in AssignedNames.items():
    # open the file
    file = open("output/AssignedNames/" + key + "_AssignedNames.txt", "w")
    # loop through the names and write them to the file
    for name in value:
        file.write(name + "\n")
    # close the file
    file.close()

# save the assigned emails for each class to a txt file named after the class and "AssignedEmails.txt"
# in the output folder
for key, value in AssignedEmails.items():
    # open the file
    file = open("output/AssignedEmails/" + key + "_AssignedEmails.txt", "w")
    # loop through the emails and write them to the file
    for email in value:
        file.write(email + "\n")
    # close the file
    file.close()

# tell the user the files have been saved
print("The files have been saved!")

# wait for the user to press enter to exit
input("\nPress enter to exit...")
# exit the program
exit()
