import json


#str = open('./request1/tex/page0.tex', 'r').read()
#print(str)
#file = open('output.txt', 'w')
out=""
def latex_parser(str):
    data = json.loads(str)
    content = data["text"]
    
    util(content)
    #file.close()
    #file1=open('output.txt','r')
    #list=file1.readlines()
    global out
    #print(list)
    #for string in list:
        #out=out+string
    return out

    


# TODO : Sathwik return only one string output when one content string is passed
# TODO : just return one string called as parsed_string
def util(content):
    global out
    flag = 0
    n = int(len(content))
    i = 0
    while i < n:
        #i=i+1
        #print(i)
        #flag=0 implies no special functions like frac and sqrt
        if (flag == 0):
            #i=i+1
            '''
            if(content[i:i+2]==" \\n"):
                file.write(" \n")
                i=i+1 # check for i++
            '''
            if (content[i] != '\\'
                    and content[i] != '^'):  #write all chars except \ and ^
                
                out=out+content[i]

                i = i + 1
                #print(out)

            elif (content[i] == '\\'):  #flag when you see \
                flag = 1
                i = i + 1

            elif (content[i] == '^'):  #write to the power of instead of ^{}

                #global out
                out=out+" to the power "
                i = i + 1

                j = i + 1
                temp = 0
                li = ['{']
                while (
                        len(li) > 0
                ):  #getting contents inside {} to call the function recursively
                    if (content[j] == '{'): li.append('{')
                    if (content[j] == '}'): li.pop()
                    j = j + 1
                    temp = temp + 1
                if (temp > 5): file.write("(")  # TODO:decide
                util(content[i + 1:j - 1])
                if (temp > 5): file.write(')')  #TODO:decide
                i = j

        if (flag == 1):
            if (content[i:i + 4] == "frac"):
                #print("i here is ",i)
                j = i + 5
                li = ['{']
                while (li):
                    if (content[j] == '{'): li.append('{')
                    if (content[j] == '}'): li.pop()
                    j = j + 1
            # print("i is ",j)
                util(content[i + 5:j - 1])
                #file.write(" divided by ")
                #global out
                out=out+" divided by "
                #print("i is ",i)
                i = j
                j = i + 1
                li = ['{']
                while (li):
                    if (content[j] == '{'): li.append('{')
                    if (content[j] == '}'): li.pop()
                    j = j + 1
                util(content[i + 1:j - 1])
                i = j
                flag = 0

            elif (content[i:i + 4] == "sqrt"):

                #file.write(" square root of ")
               # global out
                out=out+" square root of "

                j = i + 5
                li = ['{']
                while (li):
                    if (content[j] == '{'): li.append('{')
                    if (content[j] == '}'): li.pop()
                    j = j + 1
                util(content[i + 5:j - 1])
                i = j
                flag = 0

            elif (content[i:i + 4] == "left"):
                flag = 0
                i = i + 4
            elif (content[i:i + 5] == "right"):
                flag = 0
                i = i + 5
            elif (content[i] == '('):
                i = i + 1
                #file.write(" equation start ")
               # global out
                out=out+" equation start"

                flag = 0
            elif (content[i] == ')'):
                i = i + 1
               # global out
                out=out+" equation end "
                #file.write(" equation end ")

                flag = 0
            elif (content[i:i + 4] == "cdot"):
                #file.write(".")
                i = i + 4
                flag = 0

str=open('result.tex','r').read()
out=latex_parser(str)
print(out)

