from bs4 import BeautifulSoup
import requests



def calc_marks(url, answer_key):
    headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'''}
    
    legend = {'A':0,'B':1,'C':2,'D':3}
    response = requests.get(url, headers = headers).content

    soup = BeautifulSoup(response, 'html.parser')

    menu_tbl = soup.find_all('table', class_ = 'menu-tbl')
    ques_blocks = soup.find_all('table', class_ = 'questionRowTbl')

    resp = []
    marks = 0

    # answer_key = {}

    # for k in menu_tbl:
    #     dat = k.find_all('td')
    #     answer_key[dat[3].text] = 0

    # print(answer_key)
    # print(len(answer_key))

    for t in menu_tbl:
        j = 0
        dict = {}
        dat = t.find_all('td')

        if dat[1].text == 'SA':
            for j in range(0,6,2):
                dict[dat[j].text] = dat[j+1].text
            i = menu_tbl.index(t)
            if dat[5].text == 'Answered':
                ans = float(ques_blocks[i].find_all('tr')[2].find_all('td')[2].text)
            else:
                ans = ques_blocks[i].find_all('tr')[2].find_all('td')[2].text
            dict['Answer :'] = ans

        elif dat[1].text == 'MSQ':
            for j in range(0,6,2):
                dict[dat[j].text] = dat[j+1].text
            dict[dat[6].text] = dat[7].text.split(',')

        else:
            for j in range(0,8,2):
                dict[dat[j].text] = dat[j+1].text
        resp.append(dict)
        
    
    for x in resp:
        if x['Question ID :'] == '695658629':
            marks = marks + 3
            
        elif x['Status :'] == 'Not Answered' or x['Status :'] == 'Not Attempted and Marked For Review':
            pass

        else:
            if x['Question Type :'] == 'SA':
                if x['Answer :'] in answer_key[x['Question ID :']]:
                    marks = marks + 4
                else:
                    pass
            
            elif x['Question Type :'] == 'MCQ' and resp.index(x) in [0,1,2,3,16,17,18,19,32,33,34,35]:
                opt_order = []
                for t in ques_blocks[resp.index(x)].find_all('img')[-1:-5:-1][::-1]:
                    opt_order.append(t['name'][::-1][4].upper())

                if opt_order[legend[x['Chosen Option :']]] == answer_key[x['Question ID :']]:
                    marks = marks + 3
                else:
                    marks = marks - 1

            elif x['Question Type :'] == 'MCQ':
                opt_order = []
                for t in ques_blocks[resp.index(x)].find_all('img')[-1:-5:-1][::-1]:
                    opt_order.append(t['name'][::-1][4].upper())

                if opt_order[legend[x['Chosen Option :']]] == answer_key[x['Question ID :']]:
                    marks = marks + 4
                else:
                    marks = marks - 1
            
            elif x['Question Type :'] == 'MSQ':
                opt_order = []
                for t in ques_blocks[resp.index(x)].find_all('img')[-1:-5:-1][::-1]:
                    opt_order.append(t['name'][::-1][4].upper())
                
                ans = []
                for t in x['Chosen Option :']:
                    ans.append(opt_order[legend[t]])
                ans.sort()    

                if ans == answer_key[x['Question ID :']]:
                    marks = marks + 4
                else:
                    stat = True
                    for y in ans:
                        if y not in answer_key[x['Question ID :']]:
                            marks = marks - 2
                            stat = False
                            break
                    
                    if stat == True:
                        marks = marks + len(ans)

    return marks


# def marks_data():
#     p1 = calc_marks(url1, answer_key_1)
#     p2 = calc_marks(url2, answer_key_2)
#     marks = p1 + p2
#     return [marks, p1, p2]
