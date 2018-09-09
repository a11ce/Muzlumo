import pyaudio
import aubio
import numpy as np
import pygame, sys
import colorsys

def map( x,  in_min,  in_max,  out_min,  out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

def main():

    audio = pyaudio.PyAudio()

    inpFormat = pyaudio.paFloat32
    inpChannels = 1
    inpRate = int(audio.get_device_info_by_index(0)['defaultSampleRate'])
    inpBlockSize = 1024

    pygame.init()
    if ("-f" in sys.argv):
        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((200,200))

    clock = pygame.time.Clock()
    pygame.display.update()


    inpStream = audio.open( format=inpFormat,
                            channels=inpChannels,
                            rate=inpRate,
                            input=True)
    maxVol = 0
    while True:
        for e in pygame.event.get():
            if ((e.type == pygame.KEYDOWN) and (e.key == pygame.K_q)):
                sys.exit()

        data = inpStream.read(inpBlockSize)
        aubioData = np.fromstring(data, dtype=aubio.float_type)

        volume = np.sum(aubioData**2)/len(aubioData)
        print(volume)
        if (volume == 0): maxVol = 0
        if (volume>maxVol): maxVol = volume
        volMapDec = map(volume,0,maxVol,0,100)/100.0
        color = colorsys.hsv_to_rgb(0.9, 1, volMapDec)
        color = tuple(int(round(map(i,0.0,1.0,0.0,255.0 )))for i in color)
        print(color)
        screen.fill(color)
        pygame.display.update()
        clock.tick(60)
if __name__ == '__main__':
    main()
