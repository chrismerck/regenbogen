import wave
import struct
import numpy as np
import sys
import pygame
import math
import pyaudio

FORMAT = pyaudio.paInt16 

class Regenbogen(object):
  def __init__(self):
    self._font = {}
    pygame.init()
    self._bw = 2000
    self._f_min = 500
    self._samprate = 16000
    self._pps = 50
    self._chunk = 1024
    p = pyaudio.PyAudio() 
    self._stream = p.open(format = FORMAT, 
                    channels = 1, 
                    rate = self._samprate, 
                    input = True, 
                    output = True, 
                    frames_per_buffer = self._chunk) 

  def text2img(self,string):
    string = ' %s '%string
    size = 40
    color = (255,255,255)
    pos = (0,0)
    if size not in self._font:
      self._font[size] = pygame.font.Font("FreeMonoBold.ttf",size)
    text = self._font[size].render(string,1,color,(0,0,0))
    textrect = text.get_rect()
    textrect.left = pos[0]
    textrect.top = pos[1]
    w = text.get_width()
    h = text.get_height()
    img = np.zeros((w,h))
    def color_to_grey(c):
      return (c[0]+c[1]+c[2])/(3.0*255)
    for i in range(w):
      for j in range(h):
        img[i,j] = color_to_grey(text.get_at((i,j)))
    return img

  def img2audio(self,img):
    block_size = 1024*64

    #dst = 'hello.wav'
    #f_dst = wave.open(dst,"w")
    #f_dst.setnchannels(1)
    #f_dst.setsampwidth(2)
    #f_dst.setframerate(self._samprate)

    comp = 50.0

    pix_len = len(img)
    pix_wide = len(img[0])
    theta = np.random.rand(pix_wide)
    t = 0
    def get_freq(j):
      # get frequency of oscillator for frequency j
      return (pix_wide - j) / float(pix_wide) * self._bw + self._f_min

    # generate sample at once
    s = 0
    data = np.zeros(self._chunk)
    T = np.arange(0,(pix_len-1)/float(self._pps),1.0/self._samprate)
    I = np.floor(T*float(self._pps))
    P = (T*float(self._pps) - I)
    A1 = 0.5*(1+np.cos((P+1)*math.pi))
    A2 = 1 - A1
    X = np.zeros(len(T))
    for j in range(pix_wide):
      X += img[map(int,I),j] * A2 * np.sin(2*math.pi*get_freq(j)*T + theta[j])
      X += img[map(lambda x: int(x+1),I),j] * A1 * np.sin(2*math.pi*get_freq(j)*T + theta[j])

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


rb = Regenbogen()
#rb.regenbogen('Hello, World!','hello.wav')
while True:
  text = raw_input("Regenbogen >> ")
  rb.regenbogen(text,'')

