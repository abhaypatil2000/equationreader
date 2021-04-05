import json
from tex2py import tex2py
from pylatexenc.latexwalker import LatexWalker
'''
\n is end line
frac{a}{b} is a/b
ignore left and right just after \\
text after \\ is key word(frac or sqrt etc)
x^{a} is x to the power a 
sqrt{a} is square root of a 
cdot is '.'

'''
      
str=open('result.tex','r').read()

file=open('output.txt','w')
data=json.loads(str)
content=data["text"]
#print(str)

print(content)

def util_function(content):
    flag=0
    n=int(len(content))
    i=0
    while i<n :
        #i=i+1
        #print(i)
        if(flag==0):
            #i=i+1
            if(i>=n):return
            '''
            if(content[i:i+2]==" \\n"):
                file.write(" \n")
                i=i+1 # check for i++
            '''
            if(content[i]!='\\' and content[i]!='^'):
                if(content[i]=='('):file.write(" open bracket ")
                elif(content[i]==')'):file.write(" close bracket ")
                else:file.write(content[i])
                
                i=i+1
                #print(out)
        
            elif(content[i]=='\\'):
                flag=1
                i=i+1
        
            elif(content[i]=='^'):
                
                file.write(" to the power ")
                i=i+1
               
                j=i+1
                li=['{']
                while(len(li)>0):
                    if(content[j]=='{'):li.append('{')
                    if(content[j]=='}'):li.pop()
                    j=j+1
                util_function(content[i+1:j-1])
                i=j

        if(flag==1):
            if(content[i:i+4] == "frac"):
                #print("i here is ",i)
                j=i+5
                li=['{']
                while(li):
                    if(content[j]=='{'):li.append('{')
                    if(content[j]=='}'):li.pop()
                    j=j+1
               # print("i is ",j)
                util_function(content[i+5:j-1])
                file.write(" divided by ")
                
                #print("i is ",i)
                i=j
                j=i+1
                li=['{']
                while(li):
                    if(content[j]=='{'):li.append('{')
                    if(content[j]=='}'):li.pop()
                    j=j+1
                util_function(content[i+1:j-1])
                i=j
                flag=0


            elif(content[i:i+4] == "sqrt"):
                
                file.write(" square root of ")
                
                j=i+5
                li=['{']
                while(li):
                    if(content[j]=='{'):li.append('{')
                    if(content[j]=='}'):li.pop()
                    j=j+1
                util_function(content[i+5:j-1])
                i=j
                flag=0

            elif(content[i:i+4] == "left"):
                flag=0
                i=i+4
            elif(content[i:i+5] == "right"):
                flag=0
                i=i+5
            elif(content[i]=='('):
                i=i+1
                file.write(" open bracket ")
                
                flag=0
            elif(content[i]==')'):
                i=i+1 
                file.write(" close bracket ")
                
                flag=0
            elif(content[i:i+4]=="cdot"):
                file.write(".")
                i=i+4
                flag=0


util_function(content)
file.close()





        