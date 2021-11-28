from bs4 import BeautifulSoup
import requests
import random
import re
import sys
import time
import json
import pprint

# Tests

# url = 'https://www.reddit.com/r/random'
# search_texts = ['a', 'e', 'the']
#
# url ='https://en.wikipedia.org/wiki/Synthesizer'
# search_texts = ['moog']

url = 'https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/mixer.htm#Mixer_Sidechain'
search_texts = ['mixer']


class iter_obj:
    '''This is a docstring. I have created a new class'''
    children_text = ""
    parents_text = ""
    siblings_text = ""
    next_element = ""
    prev_element = ""
    index = ""
    text = ""
    pass

ignore_tags = ['body', 'title', 'script', 'style', 'html', 'img', 'a', 'meta', 'iframe']

elements = []

# To start building the JSON String we will need to create an array so... use a [
json_results_strings = "["

# Start loop here 
with requests.Session() as session:

    if random.randint(0,1):
        session.headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    else :
        session.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'}
    response = session.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    # print(soup.prettify())

    element_index = -1
    print(soup.title.get_text())

    for thing in soup.find_all():
        print(thing.name)

        print(thing.name)
        if thing.name in ignore_tags:
            continue
        print(thing)

        # You can add a substring search here, and 'continue' if you don't find a match against your list...
        found = 0
        for term in search_texts:
            if str(term) in str(thing.text):
                found = found +1
        if found is 0:
            continue

        element_index=element_index + 1
        this_iter = iter_obj()
        this_iter.text = thing.text
        this_iter.index = element_index
        this_iter.children_text = ""
        this_iter.parents_text = ""
        this_iter.siblings_text = ""
        this_iter.next_element = ""
        this_iter.prev_element = ""

        # get text of the object
        print(thing)

        try:
            this_iter.text = str(thing.text)
        except:
            print("No text for this element")
        try:
            this_iter.next_element = str(thing.next_element)
            print(thing.next_element)
        except:
            print('could not get next element')
        try:
            this_iter.prev_element = str(thing.prev_element)
        except:
            print('could not get prev element')

        try:
            for child in thing.descendants:
                this_iter.children_text = this_iter.children_text + ", " + str(child)
                print(child)
        except:
            print("could not get children")

        # get text of the parent
        try:
            this_iter.parents_text = this_iter.parents_text + str(thing.parent.text)
            print(thing.parent.text)
        except:
            print("could not get parent")
        # get text of the siblings
        try:
            for sibling in thing.siblings:
                this_iter.sibling_text = this_iter.sibling_text  + str(sibling)
                print(sibling)
        except:
            print("could not get siblings")
        # add the object created during this iteration to our results array
        elements.append(this_iter)


for element in elements:
    # try:   (Do, or Do not. There is no TRY)
    print("print result text")
    print (element.text)
    print("print result next")
    print (element.next_element)
    print("print result previous")
    print (element.prev_element)
    print("print children")
    print (element.children_text)
    print ('siblings')
    print (element.siblings_text)

    json_string = json.dumps(element.__dict__)
    json_results_strings = json_results_strings + json_string
    json_results_strings = json_results_strings + ", "

# Truncate off the final ", " and close the array with a "]"
file_len = len(json_results_strings)
truncate_to = (len(json_results_strings) - 2)
json_results_strings = json_results_strings[0:int(truncate_to)]
json_results_strings = json_results_strings + "]"

# yeah write the file out
f = open("output.json", "w")
# existing = f.read()
f.write(str(json_results_strings))
f.close()
exit()