import vlc
from time import sleep
p = vlc.MediaPlayer('Norbi.mp3')
p.play()
sleep(100)