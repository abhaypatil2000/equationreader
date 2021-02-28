from html.parser import HTMLParser

input_file = "./Files/temp.xhtml"
output_file = "./Files/out1.txt"

f = open(output_file, "w")

stack = []
mrow_count = 0
mfrac_count = 0
msup_count = 0
avoid_count = 0


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global stack
        global mrow_count
        global mfrac_count
        global msup_count
        global avoid_count

        if (tag == "head" or tag == "style" or tag == "script" or tag == "title"):
            avoid_count += 1

        elif (tag == "msqrt"):
            f.write("√ (")
            stack.append(str(tag))

        elif (tag == "msup"):
            f.write("(")
            stack.append(str(tag))

        elif (tag == "mfrac"):
            f.write("(")
            mfrac_count += 1
            stack.append(str(tag))

        elif (tag == "mrow"):
            if (stack[-1] == "msup"):
                f.write(") ^ (")
                stack.append(str(tag))
                return
            elif (stack[-1] == "msqrt"):
                f.write("")
                stack.append(str(tag))
                return
            mrow_count += 1
            f.write("(")
            stack.append(str(tag))

    def handle_endtag(self, tag):
        global stack
        global mrow_count
        global mfrac_count
        global msup_count
        global avoid_count

        if (tag == "head" or tag == "style" or tag == "script" or tag == "title"):
            avoid_count -= 1

        elif (tag == "msqrt"):
            f.write(")")
            stack.pop()

        elif (tag == "msup"):
            f.write(")")
            stack.pop()

        elif (tag == "mfrac"):
            mfrac_count -= 1
            stack.pop()
            f.write(")")

        elif (tag == "mrow"):
            stack.pop()
            if (stack[-1] == "msup" or stack[-1] == "msqrt"):
                return

            f.write(") ")
            if ((mrow_count + mfrac_count + 2) % 2 == 0):
                f.write("/")
                mrow_count -= 2

        elif (tag == "p"):
            f.write("\n")

    def handle_data(self, data):
        global stack
        global avoid_count

        if (avoid_count > 0):
            return

        if (data == "("):
            f.write("(")

        elif (data == ")"):
            f.write(")")

        else:
            data = data.strip()
            f.write(" " + data)
            pass


parser = MyHTMLParser()

xhtml_file = open(input_file, "r")
my_text = xhtml_file.read().replace("\n", " ")
parser.feed(my_text)
f.close()
xhtml_file.close()

# msqrt must contain one mrow