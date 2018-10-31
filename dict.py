import ctypes
import logging
import os
import time
import traceback
from pprint import pprint as print

logging.basicConfig(filename='LogFile.txt', filemode='a', datefmt='%D %I:%M %p',
                    format='%(asctime)s - %(message)s\n')


def mainApp():
    obj = {}
    mystring = r'A green hunting cap squeezed the top of the fleshy balloon of a head. The green earflaps, ' \
               r'full of large ears and uncut hair and the fine bristles that grew in the ears themselves, ' \
               r'stuck out on either side like turn signals indicating two directions at once. Full, pursed lips ' \
               r'protruded beneath the bushy black moustache and, at their corners, sank into little folds filled ' \
               r'with disapproval and potato chip crumbs. In the shadow under the green visor of the cap Ignatius J. ' \
               r'Reilly’s supercilious blue and yellow eyes looked down upon the other people waiting under the clock ' \
               r'at the D.H. Holmes department store, studying the crowd of people for signs of bad taste in dress. ' \
               r'Several of the outfits, Ignatius noticed, were new enough and expensive enough to be properly ' \
               r'considered offenses against taste and decency. Possession of anything new or expensive only ' \
               r'reflected a person’s lack of theology and geometry; it could even cast doubts upon one’s soul. '
    for character in mystring.upper():
        if character == " ":
            #test = character/0
            pass
        elif not character.isalpha():
            pass
        else:
            obj.setdefault(character, 0)
            obj[character] = obj[character] + 1
    print(obj)
    print(mystring)


if __name__ == '__main__':
    try:
        mainApp()
    except Exception as e:
        logging.exception(e)
        ctypes.windll.user32.MessageBoxW(0, "Exception:{}".format(
            traceback.format_exc()), "Exception", 1)
