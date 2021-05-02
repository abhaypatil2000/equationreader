import json

parsed_content = ""
content = open('output.txt', 'r').read()


def text_checking(inp):
    """
    given a string input, check its properties

    returns a tuple of two bools

    first bool tells whether that equation is valid or not
    second bool tells whether start equation and end equation are to be read or not

    """

    first = True
    second = False

    special_counter = 0  # number of special characters in the input
    inp = str(inp)
    special_counter += inp.count("frac")
    special_counter += inp.count("div")
    special_counter += inp.count("sqrt")

    second = (special_counter >= 2)

    left_counter_1 = 0  # for (
    right_counter_1 = 0
    left_counter_2 = 0  # for [
    right_counter_2 = 0
    left_counter_3 = 0  # for {
    right_counter_3 = 0

    for x in inp:
        if x == '(':
            left_counter_1
        elif x == ')':
            right_counter_1
        elif x == '{':
            left_counter_2
        elif x == '}':
            right_counter_2
        elif x == '[':
            left_counter_3
        elif x == ']':
            right_counter_3

        if left_counter_1 < right_counter_1:
            first = False
        elif left_counter_2 < right_counter_2:
            first = False
        elif left_counter_3 < right_counter_3:
            first = False

    if left_counter_1 != right_counter_1 or left_counter_2 != right_counter_2 or left_counter_3 != right_counter_3:
        first = False

    return (first, second)


def latex_parser(input_content):
    global parsed_content
    print("==============================###################################")
    print(input_content)
    print("==============================###################################")

    content = input_content.replace("\\\\", "\\")
    util(content)

    file1 = open('temp.txt', 'w')
    file1.write(parsed_content)
    file1.close()
    return parsed_content


def util(content):
    global parsed_content
    flag = 0
    is_firstrow = 0
    table = 0
    n = int(len(content))
    is_array = 0
    len_parsed = 0
    ignore_eqn_end = 0
    #print("n is ", n)
    if (n == 0): return 0

    i = 0
    while i < n:
        #i=i+1
        #print(i)
        #flag=0 implies no special functions like frac and sqrt
        if (flag == 0):
            if (content[i] != '\\' and content[i] != '^'
                    and content[i] != '&'):  #write all chars except \ and ^

                parsed_content = parsed_content + content[i]

                i = i + 1
                #print(out)

            elif (content[i] == '\\'):  #flag when you see \

                flag = 1
                i = i + 1
                if (i == n):
                    return 0

            elif (content[i:i + 16] == "& \multicolumn{1"):
                #print("ok tested")
                parsed_content += " next column "
                i += 24
                li = ['{']
                j = i
                #getting contents inside {} to call the function recursively
                while (len(li) > 0):
                    if (j >= n):
                        return 0
                    if (content[j] == '{'): li.append('{')
                    if (content[j] == '}'): li.pop()
                    j = j + 1
                util(content[i + 1:j - 1])
                i = j

            elif (content[i] == '&' and is_array == 0):
                i = i + 1

                parsed_content += " next column "
            elif (content[i] == '&' and is_array == 1):
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
                    if (j >= n):
                        return 0
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
                    if (j >= n):
                        return 0
                    if (content[j] == '{'): li.append('{')
                    if (content[j] == '}'): li.pop()
                    j = j + 1
            # print("i is ",j)
                util(content[i + 5:j - 1])
                #file.write(" divided by ")
                #global out
                parsed_content = parsed_content + " by "
                #print("i is ",i)
                i = j
                j = i + 1
                li = ['{']
                while (li):
                    if (j >= n):
                        return 0
                    if (content[j] == '{'): li.append('{')
                    if (content[j] == '}'): li.pop()
                    j = j + 1
                util(content[i + 1:j - 1])
                i = j
                flag = 0

            elif (content[i:i + 5] == "times"):
                i = i + 5
                flag = 0
                parsed_content += " times "

            elif (content[i:i + 4] == "sqrt"):

                #file.write(" square root of ")
                # global out
                parsed_content = parsed_content + " square root of "

                j = i + 5
                li = ['{']
                while (li):
                    if (j >= n):
                        return 0
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
                len_parsed = len(parsed_content)

                li = ['(']
                j = i
                while (len(li) > 0):
                    if (j >= n):
                        return 0
                    if (content[j] == '('):
                        li.append('(')
                    if (content[j] == ')'):
                        li.pop()
                    j = j + 1
                ret = text_checking(content[i:j - 1])
                if (ret[0] is False):
                    i = j
                else:
                    if (ret[1]):
                        ignore_eqn_end = 0
                        parsed_content = parsed_content + " equation start"
                    else:
                        ignore_eqn_end = 1
                    util(content[i:j - 2])
                    i = j - 2
                flag = 0
            elif (content[i] == ')' and ignore_eqn_end == 0):
                i = i + 1

                parsed_content = parsed_content + " equation end "

                flag = 0
            elif (content[i] == ')' and ignore_eqn_end == 1):
                i = i + 1
                ignore_eqn_end = 0
                flag = 0
            elif (content[i] == '['):
                i = i + 1
                parsed_content = parsed_content + "new row"
                flag = 0
            elif (content[i] == ']'):
                i = i + 1
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
                    parsed_content = parsed_content + " first row "
                    #print(1)
                    i = i + 14
                    li = ['{']
                    columns = 0
                    j = i + 1
                    while (li):
                        if(j>=n):
                            return 0
                        #if (content[j] == '{'): li.append('{')
                        if (content[j] == '}'): li.pop()
                        if (content[j] == 'l'): columns += 1
                        j = j + 1
                    i = j
                    is_firstrow = 1

                if (content[i:i + 5] == "hline"
                        and content[i + 7:i + 10] != "end"):

                    if (is_firstrow == 1):
                        is_firstrow = 0
                    else:
                        parsed_content += " next row "
                    i += 5
                    j = i
                    while (content[j:j + 5] != "hline"):
                        j += 1

                    util(content[i:j - 3])
                    i = j
                elif (content[i:i + 11] == "end{tabular"):
                    parsed_content += " table ended "
                    table = 0
                    flag = 0
                    i += 12
                else:
                    i += 1

            elif (content[i:i + 11] == 'begin{array'):

                #str_remove = " equation start"
                #parsed_content = parsed_content[:-(len(str_remove))]
                is_array = 1
                #   print("array begin")
                i = i + 13
                while (content[i] != '}'):
                    i = i + 1
                i = i + 1
                flag = 0
            elif (content[i:i + 9] == 'end{array'):
                #str_remove = "equation end"
                #parsed_content = parsed_content[:-(len(str_remove))]
                is_array = 0
                ignore_eqn_end = 1
                # print("array end")
                i = i + 10
                flag = 0
            elif (content[i:i + 4] == 'text'):
                # print("text")
                i = i + 6
                j = i
                li = ['{']
                columns = 0
                while (li):
                    if (j >= n):
                        return 0
                    #if (content[j] == '{'): li.append('{')
                    if (content[j] == '}'): li.pop()
                    if (content[j] == 'l'): columns += 1
                    j = j + 1
                util(content[i:j - 1])
                i = j
                flag = 0
            elif (content[i:i + 6] == 'mathbf'):
                i = i + 7
                j = i
                li = ['{']
                columns = 0
                while (li):
                    if (j >= n):
                        return 0
                    #if (content[j] == '{'): li.append('{')
                    if (content[j] == '}'): li.pop()
                    if (content[j] == 'l'): columns += 1
                    j = j + 1
                util(content[i:j - 1])
                i = j
                flag = 0
            elif (content[i:i + 2] == "pi"):
                flag = 0
                i = i + 2
                parsed_content += " pi "
            elif (content[i:i + 14] == "leftrightarrow"
                  or content[i:i + 14] == "Leftrightarrow"):
                flag = 0
                i = i + 14
                parsed_content += " if and only if "
            elif (content[i:i + 9] == "leftarrow"
                  or content[i:i + 9] == "Leftarrow"):
                flag = 0
                i = i + 9
                parsed_content += " left arrow "
            elif (content[i:i + 10] == "rightarrow"
                  or content[i:i + 9] == "Rightarrow"):
                flag = 0
                i = i + 10
                parsed_content += " right arrow "
            elif (content[i:i + 5] == "angle"):
                flag = 0
                i = i + 5
                parsed_content += " angle "
            elif (content[i:i + 8] == "overline"):
                flag = 0
                i = i + 8
                parsed_content += " line segment "
            elif (content[i:i + 6] == "mathrm"):
                i = i + 7
                flag = 0
                li = ['{']
                j = i
                while (li):
                    if(j>=n):
                        return 0
                    if (content[j] == '{'): li.append('{')
                    if (content[j] == '}'): li.pop()

                    j = j + 1
                util(content[i:j - 1])
                i = j
            elif (content[i:i + 5] == "Delta"):
                i = i + 5
                flag = 0
                parsed_content += " triangle "
            elif (content[i:i + 4] == "cong"):
                i = i + 4
                flag = 0
                parsed_content += " congruent to "

            else:
                i = i + 1
    return 0


#if __name__ == "__main__":

print(latex_parser(content))