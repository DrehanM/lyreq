import requests
from lxml import html
import numpy as np
from PIL import Image
import scipy.misc as smp

# Intro
print(">> Genius Lyric Fetcher\n")
running = True

while(running):

    # User Prompt
    artist = input("What artist would you like to search?> ")
    song = input("What song would you like to search by this artist?> ")

    print("Searching for ", song, " by ", artist, "...")

    # Format URL
    #url = []
    #url.extend(artist.split(' '))
    #url.extend(song.split(' '))
    #url.extend(['lyrics'])
    #url = '-'.join(url)
    url = 'https://genius.com/' + '-'.join(artist.split(' ') + song.split(' ') + ['lyrics'])

    # Fetching Request
    print('Checking Genius at ', url, '\n\n')


    page = requests.get(url)
    tree = html.fromstring(page.content)
    lyric_list = tree.xpath('//div[@class="lyrics"]/p/a/text()')

    if not lyric_list:
        print("Could not find the artist or song you requested.")
        
    else:
        lyrics = []
        for line in lyric_list:
            if '[' not in line and ']' not in line:
                line = line.replace('\n', '')
                line = line.replace('.', '')
                line = line.replace(',', '')
                line = line.replace('?', '')
                line = line.replace('!', '')
                lyrics.extend([x.lower() for x in line.split(' ')])

        length = len(lyrics)

        data = np.zeros((length,length,3), dtype=np.uint8 )
        score = 0
        for i in range(length):
            for j in range(length):
                if lyrics[i] == lyrics[j]: #and not data[j,i].any():
                    data[i,j] = (255,0,0)
                    score += 1

        img = Image.fromarray(data)
        #img.name = "{0}{1}".format('-'.join(artist.split(' ')),'-'.join(song.split(' ')))
        img.show()
        score /= length**2
        print("Similarity index: ", score)

    resp = input("Again?> ")
    if resp[0] != 'y':
        running = False



