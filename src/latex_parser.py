import json

#str = open('./request1/tex/page0.tex', 'r').read()
#print(str)
#file = open('output.txt', 'w')
parsed_content = ""
content = open('output.txt', 'r').read()


def latex_parser(input_content):
    global parsed_content
    print("==============================###################################")
    print(input_content)
    print("==============================###################################")
    # data = json.loads(str)
    # content = data["text"]
    content = input_content.replace("\\\\", "\\")
    util(content)
    #file.close()
    #file1=open('output.txt','r')
    #list=file1.readlines()
    #print(list)
    #for string in list:
    #out=out+string
    print(parsed_content)
    return parsed_content


def util(content):
    global parsed_content
    flag = 0
    table = 0
    n = int(len(content))
    print("n is ", n)
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

                parsed_content = parsed_content + content[i]

                i = i + 1
                #print(out)

            elif (content[i] == '\\'):  #flag when you see \
                flag = 1
                i = i + 1

            elif (content[i] == '^'):  #write to the power of instead of ^{}

                #global out
                parsed_content = parsed_content + " to the power "
                i = i + 1

                j = i + 1
                temp = 0
                li = ['{']
                #getting contents inside {} to call the function recursively
                while (len(li) > 0):
                    if (content[j] == '{'): li.append('{')
                    if (content[j] == '}'): li.pop()
                    j = j + 1
                    temp = temp + 1
                # if (temp > 5): file.write("(")  # TODO:decide
                util(content[i + 1:j - 1])
                # if (temp > 5): file.write(')')  #TODO:decide
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
                parsed_content = parsed_content + " divided by "
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
                parsed_content = parsed_content + " square root of "

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

                parsed_content = parsed_content + " equation start"

                flag = 0
            elif (content[i] == ')'):
                i = i + 1

                parsed_content = parsed_content + " equation end "

                flag = 0
            elif (content[i:i + 4] == "cdot"):

                i = i + 4
                flag = 0
            elif (content[i:i + 3] == "geq"):
                parsed_content = parsed_content + " greater than or equal to "
                i = i + 3
                flag = 0
            elif (content[i:i + 3] == "div"):
                parsed_content = parsed_content + "divided by"
                i = i + 3
                flag = 0
            elif (content[i:i + 13] == "begin{tabular" or table == 1):
                if table == 0:
                    table = 1
                    parsed_content = parsed_content + "table begins"
                    print(1)
                    i = i + 14
                    li = ['{']
                    columns = 0
                    j = i + 1
                    while (li):
                        #if (content[j] == '{'): li.append('{')
                        if (content[j] == '}'): li.pop()
                        if (content[j] == 'l'): columns += 1
                        j = j + 1
                    i = j
                    parsed_content = parsed_content + "first row"
                if (content[i:i + 5] == "hline" and content[i+7:i+10]!="end"):
                    i += 5
                    j = i
                    while (content[j:j + 5] != "hline"):
                        j += 1

                    util(content[i:j - 3])
                    i = j
                elif (content[i:i + 11] == "end{tabular"):
                    table = 0
                    flag = 0
                    i += 12
                else:
                    i += 1

            else:
                i = i + 1


latex_parser(content)
#print(latex_parser(content))
#str="Algebra Practice Problems for Precalculus and Calculus\nSolve the following equations for the unknown \\( x \\) :\n1. \\( 5=7 x-16 \\)\n2. \\( 2 x-3=5-x \\)\n3. \\( \\frac{1}{2}(x-3)+x=17+3(4-x) \\)\n4. \\( \\frac{5}{x}=\\frac{2}{x-3} \\)\nMultiply the indicated polynomials and simplif.......\n5. \\( (4 x-1)(-3 x+2) \\)\n6. \\( (x-1)\\left(x^{2}+x+1\\right) \\)\n7. \\( (x+1)\\left(x^{2}-x+1\\right) \\)\n8. \\( (x-2)(x+2) \\)\n9. \\( (x-2)(x-2) \\)\n10. \\( \\left(x^{3}+2 x-1\\right)\\left(x^{3}-5 x^{2}+4\\right) \\)\nFind the domain of each of the following functions in \\( 11-15 . \\)\n11. \\( f(x)=\\sqrt{1+x} \\)\n12. \\( f(x)=\\frac{1}{1+x} \\)\n13. \\( f(x)=\\frac{1}{\\sqrt{x}} \\)\n14. \\( f(x)=\\frac{1}{\\sqrt{1+x}} \\)\n15. \\( f(x)=\\frac{1}{1+x^{2}} \\)\n16. Given that \\( f(x)=x^{2}-3 x+4 \\), find and simplify \\( f(3), f(a), f(-t) \\), and \\( f\\left(x^{2}+1\\right) \\)\n17. \\( x^{2}-x-20 \\)\n18. \\( x^{2}-10 x+21 \\)\n19. \\( x^{2}+10 x+16 \\)\n20. \\( x^{2}+8 x-105 \\)\n21. \\( 4 x^{2}+11 x-3 \\)\n22. \\( -2 x^{2}+7 x+15 \\)\n23. \\( x^{2}-2 \\)\n1"
# str = open('result.tex', 'r').read()
#parsed_content = latex_parser(str)
#print(parsed_content)
