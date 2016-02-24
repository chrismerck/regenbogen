import wave
import struct
import numpy as np
import sys
import math
import time
import pyaudio
import random 

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
    '/':'-..-.',
    ' ':'',
    }

lessons = {
    'q-codes':['qth','qso','qsl','qsy','qrp','qrpp','qrs','qrq','qro','qrn','qrm','qrz','qrt','qru'],
    'names':['jim','joe','steve','chris','walter','bruce','ron','rob','frank','henry','jane','fred','tom'],
    'elements':['age','name','qth','rig','ant','key','keyer','tuner','rst'],
    'reports':['599','5nn','559','55n','579','57n','339'],
    'brands':['icom','kenwood','knwd','yaesu','tentec','ten tec','mfj','heathkit','heath','astron','alpha','vibroplex'],
    'countries':['usa','america','belize','russia','france','japan','korea','germany','england'],
    'cities':['new york','boston','portland','ashville','nashville','tampa','atlanta','chicago','paris','berlin','london','sweetwater','austin','huntsville'],
    'codes':['btu','ok','_kn','_ar','bk','/m','/r','/p','/qrp','fb','rr','rrr','r','hw','hw?','73','_sk'],
    'english':['a','the','my','on','this','again','pleasure','contact','station','radio','arrl','contest','sota'],
    'callsigns':['w2ttt','kd2imv','kc2wdj',
      'wi2w','k2zo','k2zb','wa2aly','kb2ocj',
      'w0ore', 'w1gbe',
      'k1jt','k1oki','k2hep','wa2mki','k2ors',
      'ne2q','k2riw','k2zcz','w4cgp','k4lib','kc4oca',
      'n4rh','wa4sir','w4zg','k6due','w6ezv',
      'n6kgb','kb6olj','k7ta','n6yos','9k2cs',
      'ea0jc','fo5gj','gb1mir','g2dqu','g3thz',
      'hs1a','hs1yc','j3bb','ji1kit','jy1','su1vn','ua1lo',
      'vk4ha','vu2rg','xe1n'],
    'abrvs':['sri','pse','tnx','fer','sed','rx','tx','agn','cul','abt','swl','xyl','yl','cfm','sked','dx','gm','ge','ur','hi','hihi',
      'hr','sig','sigs','hw','hv','wkd','wkg','wx','ncs','xcvr','73','nw','om','op','nr'],
    'ages':['18','20','26','29','31','42','47','38','39','50','55','66','72','81','84','86','92'],
    'states':['AL','AK','AS','AZ','AR','CA','CO','CT','DE','DC','FL','GA','GU','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MH','MA','MI','FM','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','MP','OH','OK','OR','PW','PA','PR','RI','SC','SD','TN','TX','UT','VT','VA','VI','WA','WV','WI','WY'],
    }


FORMAT = pyaudio.paInt16 

class CWTrainer(object):
  def __init__(self):
    self._font = {}
    #pygame.init()
    self._samprate = 16000
    self._chunk = 1024
    self._wpm = 40
    self._freq = 600
    p = pyaudio.PyAudio() 
    self._stream = p.open(format = FORMAT, 
                    channels = 1, 
                    rate = self._samprate, 
                    input = True, 
                    output = True, 
                    frames_per_buffer = self._chunk) 

  def char2audio(self,c,end_space=3):
    c=c.lower()
    block_size = 1024*64

    t = 0

    ditdur = 1.2 / self._wpm
    ramp = ditdur/5.

    dahdits = morse[c]
    for i in range(len(dahdits)):
      dahdit = dahdits[i]

      if i == len(dahdits) - 1:
        space_dur = end_space * ditdur
      else:
        space_dur = 1 * ditdur

      if dahdit == '.':
        dur = ditdur*1
      elif dahdit == '-':
        dur = ditdur*3

      T = np.arange(0,dur+space_dur,1.0/self._samprate)
      A = np.concatenate([
        np.linspace(0,1,ramp*self._samprate),
        np.linspace(1,1,(dur-2*ramp)*self._samprate),
        np.linspace(1,0,ramp*self._samprate),
        np.linspace(0,0,space_dur*self._samprate)
        ])
      X = A * np.sin(2*math.pi*self._freq*T)
      X *= 2**14 # scale

      s = 0
      while s < len(X):
        data = X[s:s+self._chunk]
        signal = wave.struct.pack("%dh"%(len(data)), *list(data))
        self._stream.write(signal)
        #f_dst.writeframes(signal)
        s += self._chunk

  def play_word(self,w):
    for i in range(len(w)):
      c = w[i]
      if i == len(w)-1:
        self.char2audio(c,end_space=7)
      else:
        self.char2audio(c)

  def play_prosign(self,w):
    for i in range(len(w)):
      c = w[i]
      if i == len(w)-1:
        self.char2audio(c,end_space=7)
      else:
        self.char2audio(c,end_space=0)

  def play_word_or_prosign(self,w):
    if w[0] == '_':
      self.play_prosign(w[1:])
    else:
      self.play_word(w)

def random_callsign_test(hints):
  k = 5
  letters = map(chr,range(ord('a'),ord('z')+1))
  digits = map(chr,range(ord('0'),ord('9')+1))
  first = random.choice(letters)
  last = random.choice(letters)
  # three callsigns with common first and last letters
  calls = [random_callsign_fixed(first,last) for i in range(3)]
  # two callsigns totally random
  calls += [random_callsign() for i in range(2)]
  return test(calls,hints)

def random_callsign_fixed(first,last):
  t = random.randint(1,4)
  call = ''
  letters = map(chr,range(ord('a'),ord('z')+1))
  digits = map(chr,range(ord('0'),ord('9')+1))
  if t == 1:
    call += first
    call += random.choice(letters) 
    call += random.choice(digits) 
    call += random.choice(letters) 
    call += random.choice(letters) 
    call += last
  elif t == 2:
    call += first
    call += random.choice(digits) 
    call += random.choice(letters) 
    call += random.choice(letters) 
    call += last
  elif t == 3:
    call += first
    call += random.choice(letters) 
    call += random.choice(digits) 
    call += random.choice(letters) 
    call += last
  elif t == 4:
    call += first
    call += random.choice(digits) 
    call += random.choice(letters) 
    call += last
  return call

def random_callsign():
  t = random.randint(1,6)
  call = ''
  letters = map(chr,range(ord('a'),ord('z')+1))
  digits = map(chr,range(ord('0'),ord('9')+1))
  if t == 1:
    call += random.choice(letters) 
    call += random.choice(letters) 
    call += random.choice(digits) 
    call += random.choice(letters) 
    call += random.choice(letters) 
    call += random.choice(letters) 
  elif t == 2:
    call += random.choice(letters) 
    call += random.choice(digits) 
    call += random.choice(letters) 
    call += random.choice(letters) 
    call += random.choice(letters) 
  elif t == 3:
    call += random.choice(letters) 
    call += random.choice(letters) 
    call += random.choice(digits) 
    call += random.choice(letters) 
    call += random.choice(letters) 
  elif t == 4:
    call += random.choice(letters) 
    call += random.choice(digits) 
    call += random.choice(letters) 
    call += random.choice(letters) 
  elif t == 5:
    call += random.choice(digits) 
    call += random.choice(letters) 
    call += random.choice(digits) 
    call += random.choice(letters) 
    call += random.choice(letters) 
    call += random.choice(letters) 
  elif t == 6:
    call += random.choice(digits) 
    call += random.choice(letters) 
    call += random.choice(digits) 
    call += random.choice(letters) 
    call += random.choice(letters) 
  return call

def test_lesson(lesson,hints=True):
  k = 5
  ws = random.sample(lesson,k)
  return test(ws,hints)

def test(ws,hints=True):
  w0 = ws[0]
  random.shuffle(ws)
  if hints:
    print '  '.join(ws) 
  cwt = CWTrainer()
  cwt.play_word_or_prosign(w0)
  resp = raw_input('> ')
  if resp.lower() == w0.lower():
    print "                       Correct!"
    return 1
  else:
    print "                       WRONG. Was %s"%(w0)
    return 0

def round(lesson,n=12,hints=True):
  score = 0
  for i in range(n):
    print "  word %d of %d"%(i,n)
    score += test_lesson(lesson,hints)
  print "Your Score: %d/%d"%(score,n)
  return score

def round_random_callsigns(n=12,hints=True):
  score = 0
  for i in range(n):
    print "  call %d of %d"%(i,n)
    score += random_callsign_test(hints)
  print "Your Score: %d/%d"%(score,n)
  return score

def game():
  level = 1
  def announce_lesson(level,name,hints=True):
    print
    print "****"
    print "* Level #%d"%level
    print "* Topic '%s'"%(lesson_name)
    if not hints:
      print "*   (without hints)"
    print "****"
    print
  #main_topics = ['states','codes','reports','english','names',
  main_topics = ['cities',
      'abrvs','q-codes','cities','countries','brands','elements','ages',
      'callsigns']
  while True:
    if level in range(1,1+2*len(main_topics)):
      if level % 2 == 1:
        lesson_name = main_topics[level / 2]
        announce_lesson(level,lesson_name)
        score=round(lessons[lesson_name])
      elif level % 2 == 0:
        lesson_name = main_topics[(level-1) / 2]
        announce_lesson(level,lesson_name,hints=False)
        score=round(lessons[lesson_name],hints=False)
    elif level == len(main_topics)*2:
      # final level (fully random callsigns, no hints)
      announce_lesson(level,"Totally Random Callsigns",False)
      score=round_random_callsigns(lessons[lesson_name],False)

    if score >= 11:
      level += 1
      print "You leveled up!"
    elif score < 8:
      print "You are leveled down..."
      level -= 1
    if level == 0:
      level = 1

game()


###
# Each level must be gotten 12/12 to continue.
# If you get less than 8/12, game over.
#
# Levels:
#
# (1) state abbreviations
#       and with no hints
# (2) procedural calls
#       and with no hints
# (3) abbreviations
#       and with no hints
# (4) english words
#       and with no hints
# (5) brands
#       and with no hints
# (6) cities
#       and with no hints
# (7) random callsigns
# (8) random callsigns (same first/last)
# (9) random callsigns (single char different)
# (10) random callsigns (with no hints)
###

