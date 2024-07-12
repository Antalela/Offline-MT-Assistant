from ASR import ASR
import time


asr = ASR()

while True:

    input('start')
    asr.start()
    input('stop')
    ans = asr.stop()

    #To clear punctuations
    ans = [''.join([char  for char in word if char.isalpha()]) for word in ans.split()]

    if 'close' in ans:
        print('closing...')
        break
    else:
        print(' '.join(ans))
