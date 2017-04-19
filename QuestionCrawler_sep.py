from bs4 import BeautifulSoup
import re
import time
import requests
import csv

def getDate():
    b = 243583
    fw = open('date_'+str(b)+'.txt','w')
    for p in range(b,b+10000000):
        print(p)
        pageLink = 'http://stackoverflow.com/questions?page='+str(p)+'&sort=newest'
        for i in range(5): # try 5 times
            try:
                response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                html=response.content
                break
            except Exception as e:
                print ('failed attempt',i)
                #time.sleep(0.1)
        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml')
        questions = soup.findAll('div', {'class':'question-summary'})
        for question in questions:
            qid = question['id']
            votes = question.find('span', {'class':'vote-count-post'}).text
            try: 
                date = question.find('div', {'class':'user-action-time'}).span['title'].split()[0]
            except Exception as e:
                '???'
            fw.write(str(p)+'\t'+qid+'\t'+votes+'\t'+date+'\n')
        time.sleep(0.1)
    fw.close()

def getInfo(url):
    time.sleep(1)
    for i in range(5): # try 5 times
        try:
            response=requests.get(url,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
            html=response.content
            break
        except Exception as e:
            print ('failed attempt',i)
            #time.sleep(0.1)
    soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml')
    try:
        question = soup.find('div', {'id':'question'}).tr
    except:
        return '-1','!','!'
    favorites = question.find('div', {'class':'favoritecount'}).text
    text = question.find('div', {'class':'post-text'}).text
    tags = question.find('div', {'class':'post-taglist'}).text
    #answers = soup.find('span', {'itemprop':'answerCount'}).text
    #stats = soup.find('div', {'class':'module question-stats'}).findAll('p', {'label-key'})
    #views = stats[3].text.split()[0]
    return text, tags, favorites#, views

def getQuestion():
    b = 171954
    fw = open('question_'+str(b)+'.csv','w',encoding='utf-8')
    w = csv.writer(fw)
    w.writerow(['page','qid','name','votes','answerstatus','answers','views','favorites','date','author','reputation','gold','silver','bronze','text','tags'])
    for p in range(b,b+3000):
        print(p)
        pageLink = 'http://stackoverflow.com/questions?page='+str(p)+'&sort=newest'
        for i in range(5): # try 5 times
            try:
                response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                html=response.content
                break
            except Exception as e:
                print ('failed attempt',i)
                #time.sleep(0.1)
        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml')
        questions = soup.findAll('div', {'class':'question-summary'})
        for question in questions:
            qid = question['id']
            name = question.a.text
            votes = question.find('span', {'class':'vote-count-post'}).text
            try: 
                date = question.find('div', {'class':'user-action-time'}).span['title'].split()[0]
            except Exception as e:
                '???'
            try: 
                author = question.find('div', {'class':'user-details'}).a.text
            except: 
                author = 'community wiki'
            try: 
                reputation = question.find('span', {'class':'reputation-score'}).text
            except:
                reputation = 0
            try:
                gold = question.find('span', {'title':re.compile('gold')}).text
            except:
                gold = 0
            try:
                silver = question.find('span', {'title':re.compile('silver')}).text
            except:
                silver = 0
            try:
                bronze = question.find('span', {'title':re.compile('bronze')}).text
            except:
                bronze = 0
            answer = question.find('div', {'class':re.compile('answer')})
            answerstatus = answer['class'][1]
            answers = answer.strong.text
            views = question.find('div', {'class':re.compile('views')})['title'].split()[0]
            url = 'http://stackoverflow.com'+question.a['href']
            text, tags, favorites = getInfo(url)
            w.writerow([p,qid,name,votes,answerstatus,answers,views,favorites,date,author,reputation,gold,silver,bronze,text,tags])
        #time.sleep(5)
    fw.close()

if __name__=='__main__':
    getQuestion()


