import groupy
import string, re, random, psutil, time, math, string
import sys, goslate, requests

broken = True
while broken:
    try:
        TOKEN = 0##Add your token here
        client = groupy.client.Client.from_token(TOKEN)
        time.sleep(0.1)
        groups = list(client.groups.list_all())
        broken = False
    except:
        broken = True
groupDict={}
for i in groups:
    groupDict[i.id] = i
allofem={}
allgroupids={}
def dispAll():
    i = 0
    while i < len(groups):
        print(i, groups[i].name.encode('ascii', 'ignore').decode('ascii'))
        i+=1
dispAll()

def _get_soup_object(url, parser="html.parser"):
    return BeautifulSoup(requests.get(url).text, parser)
pun=string.punctuation
pun=pun.replace("'", '')

wordFreqs = {'START':[]}
syntaxes = {}

for key in list(wordFreqs.keys()):
    if key != 'START':
        if '' in list(wordFreqs[key][1].keys()) and wordFreqs[key][1][''] != 0:
            if random.randint(1, 10)==7:
                print('Cleaning ', key)
            wordFreqs[key][0][''] = 0
            wordFreqs[key][1][''] = 0

            
def sentenceMaker(toUse, userID='all'):
    toDisp = []
    if userID == 'all':
        fullList = {'START':{}}
        for i in list(toUse.keys()):
            for j in list(toUse[i].keys()):
                ##print(len(j))
                ##print(j)
                if j == 'START':
                    for k in list(toUse[i][j].keys()):
                        ##print(k)
                        if k in list(fullList[j].keys()):
                            fullList[j][k] += toUse[i][j][k]
                        else:
                            fullList[j][k] = toUse[i][j][k]
                elif j in list(fullList.keys()):
                    for k in list(toUse[i][j][1].keys()):
                        ##print(k)
                        if k in list(fullList[j][1].keys()):
                            fullList[j][1][k] += toUse[i][j][1][k]
                        else:
                            fullList[j][1][k] = toUse[i][j][1][k]
                else:
                    fullList[j] = toUse[i][j]
    else:
        fullList = toUse[userID]
    keys = list(fullList['START'].keys())
    values=[]
    for i in keys:
        values.append(fullList['START'][i]**2)
    choice=random.choices(keys, weights=values)[0]
    toDisp.append(choice)
    exclude = ["https", "http", "twitter", "com", "groupme"]
    while choice != '.':
        try:
            keys = list(fullList[choice][1].keys())
            values=[]
            for i in keys:
                #print(i)
                values.append(fullList[choice][1][i])
            oldChoice = choice
            choice=random.choices(keys, values)[0]
            print(choice)
            while choice == '' or (choice not in list(fullList.keys()) and choice != '.'):
                if choice != '.' and (choice not in list(fullList.keys()) or len(fullList[choice]) < 3 or len(wordFreqs[choice][2]) == 0 or choice in exclude):
                    print('NOT VALID:\t', choice)
                    choice2=choice
                    choice=random.choices(keys, values)[0]
                    if choice2 == choice:
                        choice = '.'
        except:
            choice=keys[-1]
            print(keys, values)
        toDisp.append(choice)
    print(' '.join(toDisp))
    return toDisp

bigCats={}
def sentenceMaker2():
    if bigCats == {}:
        bigCatMaker()
    synKeys = list(syntaxes.keys())
    synVals = []
    for i in synKeys:
        synVals.append(syntaxes[i])
    struct=random.choices(synKeys, synVals)[0]
    parts=struct.split(' ')
    while '' in parts:
        parts.remove('')
    toPrint = []
    for i in parts:
        toPrint.append(random.choice(bigCats[i]))
    print(' '.join(toPrint))
    print(struct)
    
def save():
    print('Saving data')
    p=open('wordFreqs'+str(int(time.time()))+'.txt', 'w', encoding='utf-8')
    p.write(str(wordFreqs))
    p.close()
    q=open('visited'+str(int(time.time()))+'.txt', 'w', encoding='utf-8')
    q.write(str(visited))
    q.close()
    r=open('syntaxes'+str(int(time.time()))+'.txt', 'w', encoding='utf-8')
    r.write(str(syntaxes))
    r.close()

categories = []
def clean():
    keys = list(wordFreqs.keys())
    keys.remove('START')
    remCount = 0
    rems = []
    for k in keys:
        if len(wordFreqs[k]) < 3 or wordFreqs[k][2] == []:
            q=wordFreqs.pop(k)
            remCount+=1
            rems.append(k)
    print('Removed ',remCount,' invalid entries')
    print('They were ',', '.join(rems))


def scraper(group):
    toReturn = {}
    if group.id not in list(allgroupids.keys()):
        print('Getting all messages from group', group.name)
        print('This may take a while')
        messages = list(group.messages.list().autopage())
        allofem[group.name] = messages
        allgroupids[group.id] = group
        print('Total number of messages:', len(messages))
    else:
        messages = allofem[group.name]
    
    for m in messages:
        if messages.index(m)%100 == 0:
            print(messages.index(m))
        if m.text:
            ##sorter2()
            sentences=re.split('\. |\? |! |\n |- ', m.text.lower())

            if m.user_id not in list(toReturn.keys()):
                toReturn[m.user_id] = {'START':{}}
                print('NEW USER FOUND:\t', m.user_id, '\t', m.name)
                
            for i in sentences:
                thisSentence=i
                for j in pun:
                    while j in thisSentence:
                        thisSentence=thisSentence.replace(j, ' ')
                while '\n' in thisSentence:
                    thisSentence=thisSentence.replace('\n', ' ')
                words=thisSentence.encode('ascii', 'ignore').decode('ascii').split(' ')
                while '' in words:
                    words.remove('')
                for count in range(0, len(words)):
                    w=words[count].encode('ascii', 'ignore').decode('ascii')
                    if w.isprintable and w != '':
                        if w not in list(toReturn[m.user_id].keys()):
                            toReturn[m.user_id][w] = [{'START':0},{'.':0}]
##                            realWord=meaning(w)
##                            if not realWord:
##                                print(w)
##                                break
##                            else:
##                                print(w.upper())
                        if count == 0:
                            toReturn[m.user_id][w][0]['START']+=1
                            if w not in list(toReturn[m.user_id]['START'].keys()):
                                toReturn[m.user_id]['START'][w] = 0
                            if len(words) >= 2 and words[count+1] not in list(toReturn[m.user_id][w][1].keys()):
                                    toReturn[m.user_id][w][1][words[count+1]] = 0
                            toReturn[m.user_id]['START'][w]+=1
                            if len(words) >= 2:
                                toReturn[m.user_id][w][1][words[count+1]]+=1
                        else:
                            if count+1 == len(words):
                                if '.' not in list(toReturn[m.user_id][w][1].keys()):
                                    toReturn[m.user_id][w][1]['.']=0
                                toReturn[m.user_id][w][1]['.']+=1
                            else:
                                if words[count-1] not in list(toReturn[m.user_id][w][0].keys()):
                                    toReturn[m.user_id][w][0][words[count-1]] = 0
                                if words[count+1] not in list(toReturn[m.user_id][w][1].keys()):
                                    toReturn[m.user_id][w][1][words[count+1]] = 0
                                toReturn[m.user_id][w][0][words[count-1]]+=1
                                toReturn[m.user_id][w][1][words[count+1]]+=1
                #sorter2()
                #syntaxScanner(thisSentence.encode('ascii', 'ignore').decode('ascii'))
            
    return toReturn

def syntaxScanner(sentence='it is false'):
    thisStruct=''
    for i in pun:
        sentence=sentence.replace(i, ' '+i)
    words=sentence.split(' ')
    while ' ' in words:
        words.remove(' ')
    for j in words:
        if j not in list(wordFreqs.keys()) and j not in pun:
            return False
        elif j in pun:
            thisStruct=thisStruct+j+' '
        else:
            thisStruct=thisStruct+wordFreqs[j][2][0].lower()+' '
    if ' verb ' in thisStruct:
        if thisStruct not in list(syntaxes.keys()):
            syntaxes[thisStruct] = 0
        syntaxes[thisStruct]+=1
    else:
        print(thisStruct)
        print(sentence)
        return False


def meaning(term, disable_errors=False):
        global i
        if len(term.split()) > 1:
            print("Error: A Term must be only a single word")
        else:
                html = _get_soup_object("https://www.dictionary.com/browse/"+term)
                types = html.findAll("h3")
                types2 = []
                for i in types:
                    #print(str(i))
                    if type(i) != 'NoneType' and 'luna-pos' in str(i):
                        if i.text.split(' ') not in types2:
                            types2.append(i.text.split(' ')[0])
                types=types2
                length = len(types)
                lists = html.findAll("ul")
                out = {}
                for a in types:
                    try:
                        reg = str(lists[types.index(a)])
                    except:
                        reg=''
                    meanings = []
                    for x in re.findall(r'\((.*?)\)', reg):
                        if 'often followed by' in x:
                            pass
                        elif len(x) > 5 or ' ' in str(x):
                            meanings.append(x)
                    name = a.lower()
                    for j in string.punctuation:
                        while j in name:
                            name=name.replace(j, '')
                    if name != '' and name != 'sentence':
                        out[name] = meanings
                return out

def getPartsOfSpeech(key):
    defs = meaning(key.replace("'s", '').replace("'", ''))
    if defs:
        locPTS = {'TOTAL':0}
        totDefs = 0
        for pts in defs:
            if len(wordFreqs[key]) < 3:
                wordFreqs[key].append([])
            wordFreqs[key][2].append(pts)
        return True
    else:
        return False
    
def sorter2():
    global partsOfSpeech, defs
    partsOfSpeech = {}
    keys = list(wordFreqs.keys())
    keys.remove('START')
    valids=0
    for key in keys:
        if len(wordFreqs[key]) < 3 or wordFreqs[key][2] == []:
            if keys.index(key) % 50 == 0:
                print(key, ':\t',keys.index(key), valids)
            l=getPartsOfSpeech(key)
            if l:
                valids+=1
            else:
                print(key)
        else:
            valids+=1
    clean()

def bigCatMaker():
    global bigCats
    bigCats = {}
    keys=list(wordFreqs.keys())
    for key in keys:
        if len(wordFreqs[key]) == 3:
            for i in range(0, int(len(wordFreqs[key][2])/2)):
                currcat = wordFreqs[key][2][i].lower()
                if currcat not in list(bigCats.keys()):
                    bigCats[currcat] = []
                bigCats[currcat].append(key)

broken = True
wordFreqs = {}
##client.bots.list()[1].post("Going down for a few minutes. Refreshing...")
while broken:
    try:
        ##i=client.bots.list()[0]
        for i in client.bots.list():
            wordFreqs[i.group_id] = scraper(groupDict[i.group_id])
        broken = False
    except:
        time.sleep(5)
        print("Error with getting bots")


##client.bots.list()[1].post("Alright I'm back.")
while True:
    try:
        time.sleep(random.random()*6)
        for i in client.bots.list():
            mrm = groupDict[i.group_id].messages.list()[0]
            if mrm.text and 'predictive text' in mrm.text.lower():
                time.sleep(0.1)
                if mrm.attachments:
                    a=mrm.attachments
                    if a[0].user_ids:
                        sent = ['predictive', 'text', 'com']
                        while 'predictive' in sent and 'text' in sent and 'com' in sent:
                            sent=sentenceMaker(wordFreqs[i.group_id], a[0].user_ids[0])
                elif not mrm.attachments and 'Predictive Text' in mrm.text:
                    sent = ['predictive', 'text']
                    while 'predictive' in sent and 'text' in sent:
                        sent=sentenceMaker(wordFreqs[i.group_id], 'all')

                elif not mrm.attachments:
                    sent = ['predictive', 'text', 'http']
                    while 'predictive' in sent and 'text' in sent or 'http ' in sent or ' com ' in sent:
                        sent=sentenceMaker(wordFreqs[i.group_id], mrm.user_id)
                i.post(' '.join(sent))
    except :
        print("Got an error. Waiting")
        time.sleep(5)
