import pyaudio
import audioop

def main():
    inpFormat = pyaudio.paInt16
    inpChannels = 1
    inpRate = 44100
    inpBlockSize = 1024

    audio = pyaudio.PyAudio()

    inpStream = audio.open( format=inpFormat,
                            channels=inpChannels,
                            rate=inpRate,
                            input=True)

    while True:
        data = inpStream.read(inpBlockSize)
        volume = audioop.rms(data, 2)
        print(volume)


if __name__ == '__main__':
    main()
