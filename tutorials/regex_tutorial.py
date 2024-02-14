# regex = regular expressions = sequence of characters that form a search pattern
# regular expressions are useful to solve NLP-related tasks
# regex101.com is useful
import re

def example1():
    # Search the string to see if it starts with "The" and ends with "Spain":
    txt = "The rain in Spain"
    x = re.search("^The.*Spain$", txt)

def functions_notes():
    # findall() = returns a list containing all matches
    # search() = returns a Match object if there is a match anywhere in the string
    # split() = returns a list where the string has been split at each match
    # sub() = replaces one or many matches with a string
    return

def findall_example():
    # returns a list containing all matches
    txt = "The rain in Spain"
    x = re.findall("ai", txt) # ['ai', 'ai']
    y = re.findall("Portugal", txt) # []
    print(x)
    print(y)

def search_example():
    # searches string for a match, and returns a Match object if there is a match
    # returns first occurence of the match if there is more than one match

    # search for first whitespace character in the string
    txt = "The rain in Spain"
    x = re.search("\s", txt)
    print("The first white-space character is located in position:", x.start())

    # return None if no matches are found
    txt = "The rain in Spain"
    x = re.search("Portugal", txt)
    print(x)

def split_example():
    # returns a list where the string has been split at each match
    txt = "The rain in Spain"
    x = re.split("\s", txt)
    print(x)

    # control the number of occurences by specifying the maxsplit parameter
    # split string at only first occurrence in this example
    y = re.split("\s", txt, 1)
    print(y)

def sub_example():
    # replaces matches with text of your choice
    
    # replace every white-space character with the number 9:
    txt = "The rain in Spain"
    x = re.sub("\s", "9", txt)
    print(x)

    # control the number of replacements by specifying the count parameter
    # replace the first 2 occurrences in this example
    y = re.sub("\s", "9", txt, 2)
    print(y)

def match_object_notes():
    # A Match Object is an object containing information about the search and the result.
    # If there is no match, the value None will be returned, instead of the Match Object.

    txt = "The rain in Spain"
    x = re.search("ai", txt)
    print(x) #this will print an object

    # The Match object has properties and methods used to retrieve information about the search, and the result:
    # .span() returns a tuple containing the start-, and end positions of the match.
    # .string returns the string passed into the function
    # .group() returns the part of the string where there was a match

    # search for S followed by 1+ occurences of a character at beginning or end of word, and print start/end positions
    x = re.search(r"\bS\w+", txt)
    print(x.span())

    # print the string passed into the search function
    print(x.string)

    # print the part of the string where there was a match
    print(x.group())

def main():
    match_object_notes()
    return

if __name__=="__main__":
    main()
