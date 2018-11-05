#import packages
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

##use urllib2 module to open the url you want to crawl
Page = 1
while Page <= 2:
    url = r'https://www.booking.com/reviews/us/hotel/mandarin-oriental.html?aid=304142;label=gen173nr-1FCAEoggJCAlhYSDNYBHIFdXNfbnmIAQGYATHCAQp3aW5kb3dzIDEwyAEU2AEB6AEB-AECkgIBeagCAw;sid=5751f764491ccb1c7524169547d530e5;customer_type=total;hp_nav=0;old_page=0;order=featuredreviews;page='+str(Page)+';r_lang=en;rows=75&'
    hotelUrl=urlopen(url)
    soup=BeautifulSoup(hotelUrl,'html.parser')

    #To scrape reviewers' demographic information
    authorList = []
    for i in soup.find_all('div',{'class':'review_item_reviewer'}): 
        perauthor = i.find('span', itemprop='name').get_text()
        authorList.append(perauthor)
    demographicInfo = []
    for d in soup.find_all('div',{'class':'review_item_reviewer'}): 
        c = d.find('span', itemprop='nationality').get_text()
        country = c.replace('\n','')
        age = d.find('div', {'class':'user_age_group'}).get_text()
        age_group = age.replace('\n','')
        perInfoTuple = (country,age_group)
        demographicInfo.append(perInfoTuple)
    #To scrape reviewers' scores on reviews
    scoreInfo = []
    for s in soup.find_all('div',{'class':'review_item_review'}):
        score = s.find('span',{'class':'review-score-badge'}).get_text()
        perscore = score.replace('\n','')
        scoreInfo.append(perscore)
    #print(scoreInfo[3])
    #To scrape reviewers' both positive and negative reviews
    reviewInfo = []
    for r in soup.find_all('div',{'class':'review_item_review_content'}):
        neg_review = r.find('p',{'class':'review_neg'})
        pos_review = r.find('p',{'class':'review_pos'})
        perReviewTuple = (neg_review,pos_review)
        reviewInfo.append(perReviewTuple)
    #To clean up reviews with tags and classes
    newReviewInfo = []
    for t in reviewInfo:
        a = str(t[0]).replace('<p class="review_neg"><i class="review_item_icon" data-et-click="customGoal:HDDHQDSJPXaFWDaXe:1">눉</i><span itemprop="reviewBody">','').replace('</span></p>','').replace('\t','').replace('^p','').replace('^|','').replace('\n','')
        b = str(t[1]).replace('<p class="review_pos"><i class="review_item_icon" data-et-click="customGoal:HDDHQDSJPXaFWDaXe:2">눇</i><span itemprop="reviewBody">','').replace('</span></p>','').replace('\t','').replace('^p','').replace('^|','').replace('\n','')
        newReviewTuple = (a,b)
        newReviewInfo.append(newReviewTuple)
    #print(newReviewInfo[3])

    ValueList = []
    for a,b,c in zip(demographicInfo,scoreInfo,newReviewInfo):
        ValueTuple = (a,b,c)
        ValueList.append(ValueTuple)
    CommentDic = dict(zip(authorList,ValueList))
    newFile = open('Reviews from Mandarin Oriental NYC.txt','a',encoding = 'utf8')
    newFile.write('Author'+'\t'+'Country'+'\t'+'Age group'+'\t'+'Score'+'\t'+'Negative Review'+'\t'+'Positive Review'+'\n')
    for k in CommentDic:
        newFile.write(k+'\t'+CommentDic[k][0][0]+'\t'+CommentDic[k][0][1]+'\t'+CommentDic[k][1][0]+'\t'+CommentDic[k][2][0]+'\t'+CommentDic[k][2][1]+'\n')
    newFile.close()
    Page += 1
    




