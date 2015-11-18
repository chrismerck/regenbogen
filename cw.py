import wave
import struct
import numpy as np
import sys
import math
import pyaudio
from getch import getch

morse = {
    'a':'.-',
    'b':'-...',
    'c':'-.-.',
    'd':'-..',
    'e':'.',
    'f':'..-.',
    'g':'--.',
    'h':'....',
    'i':'..',
    'j':'.---',
    'k':'-.-',
    'l':'.-..',
    'm':'--',
    'n':'-.',
    'o':'---',
    'p':'.--.',
    'q':'--.-',
    'r':'.-.',
    's':'...',
    't':'-',
    'u':'..-',
    'v':'...-',
    'w':'.--',
    'x':'-..-',
    'y':'-.--',
    'z':'--..',
    '1':'.----',
    '2':'..---',
    '3':'...--',
    '4':'....-',
    '5':'.....',
    '6':'-....',
    '7':'--...',
    '8':'---..',
    '9':'----.',
    '0':'-----',
    '.':'.-.-.-',
    ',':'--..--',
    ':':'---...',
    '?':'..--..',
    "'":'.----.',
    '-':'-..-.',
    }


class CWTrainer(object):
  def __init__(self):
    self._font = {}
    pygame.init()
    self._samprate = 16000
    self._chunk = 1024
    self._wpm = 10
    self._freq = 600
    p = pyaudio.PyAudio() 
    self._stream = p.open(format = FORMAT, 
                    channels = 1, 
                    rate = self._samprate, 
                    input = True, 
                    output = True, 
                    frames_per_buffer = self._chunk) 

  def char2audio(self,c):
    block_size = 1024*64

    theta = np.random.rand(pix_wide)
    t = 0

    ditdur = 1.2 / self._wpm
    ramp = ditdur/5.

    dahdits = morse[c]
    for dahdit in dahdits:

      if dahdit == '.':
        dur = ditdur*1
      elif dahdit == '-':
        dur = ditdur*3

      data = np.zeros(self._chunk)
      T = np.arange(0,dur+ditdur,1.0/self._samprate)
      X = np.zeros(len(T))
      A = 
      X += img[map(int,I),j] * A2 * np.sin(2*math.pi*self._freq*T + theta[j])

      # normalize
      X = X/(np.max(np.abs(X))+0.1)*65535*0.5

      s = 0
      while s < len(X):
        data = X[s:s+self._chunk]
        signal = wave.struct.pack("%dh"%(len(data)), *list(data))
        self._stream.write(signal)
        #f_dst.writeframes(signal)
        s += self._chunk

  def regenbogen(self,text,fn):
    # convert unicode to image,
    #  then image to audio
    
    img = self.text2img(text)
    self.img2audio(img)

    """
    # open destination file
    f_dst = wave.open(dst,"w")
    f_dst.setnchannels(1)
    f_dst.setsampwidth(2)
    f_dst.setframerate(sample_rate)
    print "Writing to '%s'."%(dst)

    # write block at once
    block_i = 0
    sig_i = 0
    while True:
      sys.stdout.write("Progress: [%i]  \r"%(block_i))
      sys.stdout.flush()
      block_i += 1
      out_block = ''
      if block_i > 1000:
        break
      for i in range(1000):

        try:
          sig_raw = d._signal[sig_i][0]
        except:
          break

        sig_norm = max(-32768,min(32767,int(sig_raw/20.0*32767)))

        # load output buffer
        out_block += struct.pack("h",sig_norm)

        sig_i += 1

      # write output block
      f_dst.writeframes(out_block)

    print "Progress: [%3.02f%%]  "%(100.0)

    # clean up
    print "Cleaning up..."
    f_dst.close()

    print "Done."
    """

c = getch()
print "Got: ", c 

#cwt  = CWTrainer()
#cwt.loop()

