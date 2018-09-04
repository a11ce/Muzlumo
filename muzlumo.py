import pyaudio
import audioop
import pygame
import colorsys

def map( x,  in_min,  in_max,  out_min,  out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

def main():
    inpFormat = pyaudio.paInt16
    inpChannels = 1
    inpRate = 44100
    inpBlockSize = 1024

    pygame.init()
    screen = pygame.display.set_mode((200,200))
    audio = pyaudio.PyAudio()
    clock = pygame.time.Clock()
    pygame.display.update()


    inpStream = audio.open( format=inpFormat,
                            channels=inpChannels,
                            rate=inpRate,
                            input=True)

    while True:
        pygame.event.pump()

        data = inpStream.read(inpBlockSize)
        volume = audioop.rms(data, 2)

        volMapDec = map(volume,0,9000,0,100)/100.0
        color = colorsys.hsv_to_rgb(0.9, 1, volMapDec)
        color = tuple(int(round(map(i,0.0,1.0,0.0,255.0 )))for i in color)
        print(color)
        screen.fill(color)
        pygame.display.update()
        clock.tick(60)
if __name__ == '__main__':
    main()
