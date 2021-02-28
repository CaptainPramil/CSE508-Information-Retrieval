import os
import re, string, unicodedata
import nltk
import shutil
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer

file='C:\\Users\\vishy\\Desktop\\4th SEM\\IR\\Assignment\\A1\\RT'



def createDictionary():
    ad={}
    d17=os.getcwd()
    os.chdir(file)
    fi= os.listdir(os.getcwd())
    fi2=fi

    for jd in fi2:
          with open(jd, 'r') as f:
              words=f.read()
              g2=words.lower()
              f3=g2.split()
              k1=[',']
              k2=['!']
              k3=['?']
              k4=['.']
              k5=k1+k2+k3+k4
              g5=f.name
              gp=ad.keys()
              for i in f3:
                d1=i[-1]
                if d1 in k5:
                  k=i[:-1]
                  i=k
                if i not in gp:
                    t=g5
                    ad[i] = [t]
                else:
                  if jd in ad[i]:
                      continue
                  else:
                      ad[i] = ad[i]+[g5]

    return ad, fi

postlist,doclist =createDictionary()
#print(postlist)

def AND(S1,S2):
    ans=[]
    i=0
    j=0
    c=0
    while (i<len(S1) and j<len(S2)):
        c+=1
        if (S1[i]==S2[j]):
            ans.append(S1[i])
            i=i+1
            j=j+1
        elif (i<j):
            i=i+1
        else:
            j=j+1
    return ans,c


def OR(S1,S2):
    ans=[]
    i=0
    j=0
    c=0
    while (i<len(S1) and j<len(S2)):
        c=c+1
        if (S1[i]==S2[j]):
            ans.append(S1[i])
            i=i+1
            j=j+1
        elif (i<j):
            ans.append(S1[i])
            i=i+1
        else:
            ans.append(S2[j])
            j=j+1
            
    while i < len(S1): 
        print(S1[i])
        c=c+1
        ans.append(S1[i])
  
    while j < len(S2): 
        ans.append(S2[j])
        j += 1
        c=c+1
    return ans,c   


def notAND(S1,S2):
    ans,c=AND(S1,list(set(S2)^set(doclist)))
    return ans,c

def notOR(S1,S2):
    ans,c=OR(S1,list(set(S2)^set(doclist)))
    return ans,c


stop_words = set(stopwords.words('english'))  
query=input('Enter Query:')

def to_lowercase(words):
    lower_word = [] # Initialization to save the lower case character
    for word in words: #Iterate through each word in filr
        new_word = word.lower() #convert to lower case
        lower_word.append(new_word + " ") #append the normalized word to the text
        
    return lower_word


def stem_words(words):
    stemmer = LancasterStemmer()
    stems_words = []
    for word in words:
        rstem = stemmer.stem(word)
        stems_words.append(rstem +" ")
    return stems_words


#words = nltk.word_tokenize(query)
s=query.lower()
tokenizer=RegexpTokenizer(r'\w+')
tokens=tokenizer.tokenize(s)
filtered_content = [w for w in tokens if not w in stop_words]
processed_content = to_lowercase(filtered_content)
processed_content = [''.join(c for c in s if c not in string.punctuation) for s in processed_content]

#processed_content = [x.strip(' ') for x in processed_content]
#print(processed_content)

res = [] 
#for ele in processed_content: 
    #if ele.strip(): 
        #res.append(ele) 
res=processed_content        
#res = stem_words(res)

sequence=input('Enter Sequence: ')
li = list(sequence.split(","))


def process(S1,S2,exp):
    if (exp=='OR'):
        S,c= OR(S1,S2)
    elif(exp=='AND'):
        S,c= AND(S1,S2)
    elif(exp=='OR NOT'):
        S,c= notOR(S1,S2)
    else :
        S,c= notAND(S1,S2)
    return S,c
    
S=postlist[res[0].rstrip()]
c=0
for i in range(1,len(res)):
    S1=postlist[res[i].rstrip()]
    S,c1=process(S,S1,li[i-1])
    c=c+c1
    
print('Number of documents Matched',len(S))
print('Number of comparisons',c)
print('Documents Matched')
for i in S:
    print(i)
