from bs4 import BeautifulSoup
import re
import os

def LyricCounting(dirIn):
    
    workDir = dirIn

    spell = open('spellcheck.txt', 'r').read()
    
    os.chdir(workDir)

    wordList = {}
    rejected = {}
    wordCount = 0
    songNumber = 0

    for file in os.listdir(os.getcwd()):

        try:

            page = open(file, encoding='utf-8')

            rapperName = workDir + '-'

            songName = page.name.replace(rapperName, '').replace('-',' ').replace('.htm','').title()

            soup = BeautifulSoup(page, "html.parser")

            soup = soup.find('div', class_='song_body-lyrics')

            lyrics = soup.get_text()

            lyrics = lyrics.lower()

            print(songName)

            googleDelete = re.compile(r'googletag.*?;.*?;', re.DOTALL)

            lyrics = re.sub(googleDelete, '', lyrics)

        
            deleteHook = re.compile(r'\[break\]|\[intro\]|\[hook.*?\]|\[sample.*?\]|\[verse.*?\]|\[bridge.*?\]|\[outro\]|\[produced.*?\]')

            lyrics = re.sub(deleteHook, ' ', lyrics)
        
            lyrics = re.sub("[^a-zA-Z'-]"," ",lyrics).split()

            #print(lyrics)

            wordCount += len(lyrics)
        
            for word in lyrics:

                if word in spell:
            
                    if word in wordList:
                        wordList[word] += 1

                    else:
                        wordList[word] = 1

                else:
                    if word in rejected:
                        rejected[word] += 1

                    else:
                        rejected[word] = 1
            
            songNumber += 1

        except KeyboardInterrupt:
            break


    print()
    print()

    for w in sorted(wordList, key=wordList.get, reverse=True):

        if wordList[w] >= 100:
            print(w, wordList[w])

    print()

    print(str(len(wordList)) + ' verschiedene Wörter in ' + str(songNumber) + ' Songs.')

    print()

    print('Total words: ' + str(wordCount))

    print('Added dict value: ' + str(sum(wordList.values())))

    print('Words not in dict: ')

    print(rejected.keys())

    os.chdir('..')
    
    f = open('RapperVocab.txt', 'a')

    rapName = dirIn.replace('-', ' ').title()
    
    f.write('Rapper: ' + rapName + '\n')

    f.write('Unique words: ' + str(len(wordList)) + '\n')

    f.write('Words with at least 100 uses: \n')
    
    for w in sorted(wordList, key=wordList.get, reverse=True):

        if wordList[w] >= 100:
            f.write(str(w) + ' ' + str(wordList[w]) + '\n')

    f.write('\n\n----------------------------------------------------------------\n\n')

    f.close()

    print()
    
    another = input('Analyze another rapper? If yes - dir name: ')

    if another != '':
        LyricCounting(another)

inp = input('dir name: ')

LyricCounting(inp)
