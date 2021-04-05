import json
'''
\n is end line
frac{a}{b} is a/b
ignore left and right just after \\
text after \\ is key word(frac or sqrt etc)
x^{a} is x to the power a 
sqrt{a} is square root of a 
cdot is '.'

'''

str = open('./request1/tex/page0.tex', 'r').read()

file = open('output.txt', 'w')
data = json.loads(str)
content = data["text"]
#print(str)

print(content)


def latex_parser(content):
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
                file.write(content[i])

                i = i + 1
                #print(out)

            elif (content[i] == '\\'):  #flag when you see \
                flag = 1
                i = i + 1

            elif (content[i] == '^'):  #write to the power of instead of ^{}

                file.write(" to the power ")
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
                latex_parser(content[i + 1:j - 1])
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
                latex_parser(content[i + 5:j - 1])
                file.write(" divided by ")

                #print("i is ",i)
                i = j
                j = i + 1
                li = ['{']
                while (li):
                    if (content[j] == '{'): li.append('{')
                    if (content[j] == '}'): li.pop()
                    j = j + 1
                latex_parser(content[i + 1:j - 1])
                i = j
                flag = 0

            elif (content[i:i + 4] == "sqrt"):

                file.write(" square root of ")

                j = i + 5
                li = ['{']
                while (li):
                    if (content[j] == '{'): li.append('{')
                    if (content[j] == '}'): li.pop()
                    j = j + 1
                latex_parser(content[i + 5:j - 1])
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
                file.write(" equation start ")

                flag = 0
            elif (content[i] == ')'):
                i = i + 1
                file.write(" equation end ")

                flag = 0
            elif (content[i:i + 4] == "cdot"):
                file.write(".")
                i = i + 4
                flag = 0


latex_parser(content)
file.close()
