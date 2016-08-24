
# coding: utf-8

# 

# In[38]:

from sklearn.externals import joblib


# In[39]:


clf = joblib.load('classify.model')
cate_dict = joblib.load('cate_dict.dat')
vectorizer = joblib.load('vectorizer.dat')


# In[40]:

joblib.dump(clf,'n_classify.model')


# In[ ]:

joblib.dump(cate_dict,'n_cate_dict.dat')
joblib.dump(vectorizer,'n_vectorizer.dat')


# In[ ]:

cate_id_name_dict = dict(map(lambda (k,v):(v,k),cate_dict.items()))


# In[ ]:

pred = clf.predict(vectorizer.transform(['베네통키즈 멀티프린트경량신발주머니']))[0]
print pred
print cate_id_name_dict[pred]


# In[ ]:


from bottle import route, run, template,request,get, post
from konlpy.tag import Mecab
from nltk import collocations

def ParseDash(tmp):
    index = tmp.find('-')
    tmpIndex = index
    
    while tmp[tmpIndex]!=' ':
        if tmpIndex>0:
            tmpIndex-=1
        else :
            break
    while tmp[index]!=' ':
        if len(tmp)-1 != index:
            index+=1
        else :
            break
    return " " + tmp[tmpIndex:tmp.find('-')] +" "+ tmp[tmp.find('-')+1:index]

mecab = Mecab()
bigram_measures = collocations.BigramAssocMeasures()

import  time
import sys
from threading import  Condition
_CONDITION = Condition()
@route('/classify')
def classify():
    
    reload(sys)
    sys.setdefaultencoding('utf-8')

    specialLetter = "( ) [ ] { } % ＃ ＆ ＊ ＠ § ※ ☆ ★ ○ ● ◎ ◇ ◆ □ ■ △ ▲ ▽ ▼ → ← ↑ ↓ ↔ 〓 ◁ ◀ ▷ ▶ ♤ ♠ ♡ ♥ ♧ ♣ ⊙ ◈ ▣ ◐ ◑ ▒ ▤ ▥ ▨ ▧ ▦ ▩ ♨ ☏ ☎ ☜ ☞ ¶ † ‡ ↕ ↗ ↙ ↖ ↘ ♭ ♩ ♪ ♬ ㉿ ㈜ № ㏇ ㏂ ㏘ ℡ ? ª º ☞ ☜ ▒ "
    specialLetter += "─ │ ┌ ┐ ┘ └ ├ ┬ ┤ ┴ │ ━ ┃ ┏ ┓ ┛ ┗ ┣ ┳ ┫ ┻ ╋ ┠ ┯ ┨ ┷ ┿ ┝ ┰ ┥ ┸ ╂ ┒ ┑ ┚ ┙ ┖ ┕ ┎ ┍ ┞ ┟ ┡ ┢ ┦ ┧ ┩ ┪ ┭ ┮ ┱ ┲ ┵ ┶ ┹ ┺ ┽ ┾ ╀ ╁ ╃ ╄ ╅ ╆ ╇ ╈ ╉ ╊ "
    print "classify called"
    img = request.GET.get('img','')
    name = request.GET.get('name', '')
    name = unicode(name)
    print name
    listTmp = mecab.pos(name)
    print 'test1'
    for node in listTmp:    
        if node[1]=="SY":
            if node[0]=='-':
                name += ParseDash(name)
            if specialLetter.find(node[0].encode('utf-8'))!= -1:
                name = name.replace(node[0]," ")
            elif len(node[0])>=2:
                name = name.replace(node[0]," ")
    print type(name)
    pred = clf.predict(vectorizer.transform([name]))[0]
    print cate_id_name_dict[pred]
    return {'cate':cate_id_name_dict[pred]}


run(host='0.0.0.0', port=8887)


#  * 추후 여기 docker 에서 뭔가 python package 설치할게 있으면 
#  * /opt/conda/bin/pip2 install bottle 이런식으로 설치 가능

# In[ ]:



