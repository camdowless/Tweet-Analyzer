def main():
    import time
    from selenium import webdriver
    from bs4 import BeautifulSoup as bs
    user = input("Enter a twitter user handle\n")
    chrome_options = webdriver.ChromeOptions()  
    chrome_options.headless = True
    browser = webdriver.Chrome()
    browser.get('https://twitter.com/' + user)

    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
             match=True

    source_data = browser.page_source

    site = bs(source_data,'html.parser')
    prepareTweets(site, user)
    
def prepareTweets(site, user):
    username = user
    tweets = site.find_all('div',attrs={'class':'js-tweet-text-container'})
    handles = site.find_all('div',attrs={'class':'stream-item-header'})
    #searchForKeyWord(tweets, handles, username)
    excelDoc(tweets, handles, user)

def searchForKeyWord(tweets, handles, user):
    response = ""
    while(response != "q"):
        keyword = input("Enter a keyword or q to quit\n")
        response = keyword
        searchAndPrint(tweets, handles, keyword, username)
    
def searchAndPrint(tweets, handles, keyword, user):
    #Prints out all tweets that contain the keyword
    count = 0
    for i in range(0,len(tweets)):
        current_handle = handles[i]
        current_tweet = tweets[i]
        if(current_handle.find('b').text == user and keyword in (current_tweet.find('p').text)):
             print(current_handle.find('b').text)
             print(current_tweet.find('p').text)
             count += 1
             print()
    print(count)


def excelDoc(tweets,handles, user):
    #Sorts words by most frequently used in an Excel doc, excluding the top 100 most common words
    import xlsxwriter
    workbook = xlsxwriter.Workbook("test.xlsx")
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', '@'+user)
    wordList = []
    wordCount = []
    excelIndex = 2
    boringList = ["the","of","and","a","to","in","is","you","that","it","he","was","for","on","are","as","with","his","they","I","at","be","this","have","from","or","one","had","by","word","but","not","what","all","were","we","when","your","can","said","there","use","an","each","which","she","do","how","their","if","will","up","other","about","out","many","then","them","these","so","some","her","would","make","like","him","into","time","has","look","two","more","write","go","see","number","no","way","could","people","my","than","first","water","been","call","who","oil","its","now","find","long","down","day","did","get","come","made","may","part"]
    for i in range(0, len(tweets)):
        current_handle = handles[i]
        current_tweet = tweets[i]
        if(current_handle.find('b').text == user):
            tweet = current_tweet.find('p').text
            for word in tweet.split():
                if(word in wordList):
                   index = wordList.index(word)
                   wordCount[index] +=1
                else:
                    if(word not in boringList):
                        wordList.append(word)
                        wordCount.append(1)
                    
    for x in range(0,len(wordList)):
        worksheet.write('A' + str(excelIndex), wordList[x])
        worksheet.write('B' + str(excelIndex), wordCount[x])
        excelIndex += 1
    workbook.close()
    
