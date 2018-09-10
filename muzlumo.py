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

    pDetection = aubio.pitch("default", 2048,2048//2, 44100)
    pDetection.set_unit("midi")
    pDetection.set_silence(-40)

    inpStream = audio.open( format=inpFormat,
                            channels=inpChannels,
                            rate=inpRate,
                            input=True)
    maxVol = 0
    minPitch = 48
    maxPitch = 48
    while True:
        for e in pygame.event.get():
            if ((e.type == pygame.KEYDOWN) and (e.key == pygame.K_q)):
                sys.exit()

        try:
            data = inpStream.read(inpBlockSize)
        except Exception as e:
            pass

        aubioData = np.fromstring(data, dtype=aubio.float_type)

        volume = np.sum(aubioData**2)/len(aubioData)
        if (volume == 0): maxVol = 0.00000000000000001
        if (volume>maxVol): maxVol = volume
        volMapDec = map(volume,0,maxVol,0,100)/100.0

        pitch = pDetection(aubioData)[0]
        if (pitch>maxPitch and pitch<5000): maxPitch = pitch
        if (pitch<minPitch and pitch > 0): minPitch = pitch
        if (pitch==0):
            minPitch = 48
            maxPitch = 48
            pitch = (minPitch+maxPitch)/2


        try:
            pitchMapDec = map(pitch, minPitch, maxPitch, 0, 87.5)/100.0
            int(pitchMapDec)
        except Exception as e:
            pitchMapDec = 0.5
        color = colorsys.hsv_to_rgb(pitchMapDec, 1, volMapDec)

        color = tuple(int(round(map(i,0.0,1.0,0.0,255.0 )))for i in color)

        print(color)
        screen.fill(color)
        pygame.display.update()
        clock.tick(60)
if __name__ == '__main__':
    main()
