from waveapi import events
from waveapi import robot
from waveapi import appengine_robot_runner
import logging

def OnWaveletSelfAdded(event, wavelet):
  """Invoked when the robot has been added."""
  logging.info("OnWaveletSelfAdded called")
  wavelet.reply("\nHi everybody! I'm a Python robot! " + "waveid: " + wavelet.wave_id + " waveletid: " + wavelet.wavelet_id)
  
def OnWaveletParticipantsChanged(event, wavelet):
  logging.info("OnParticipantsChanged called")
  newParticipants = event.participants_added
  for newParticipant in newParticipants:
    wavelet.reply("\nHi : " + newParticipant)
    wavelet.reply("\nI'm a Python robot! " + "waveid: " + wavelet.wave_id + " waveletid: " + wavelet.wavelet_id)




def ProfileHandler(name):
  if name == 'drew':
    return {'name': 'Drew LeSueur',
            'imageUrl': 'http://a3.twimg.com/profile_images/250985893/twitter_pic_bigger.jpg',
            'profileUrl': 'http://www.twitter.com/drewlesueur'}
            

if __name__ == '__main__':
  myRobot = robot.Robot('gae-run', 
      image_url='http://a3.twimg.com/profile_images/250985893/twitter_pic_bigger.jpg',
      profile_url='http://clstff.appspot.com/')
  myRobot.register_handler(events.WaveletParticipantsChanged, OnWaveletParticipantsChanged)
  myRobot.register_handler(events.WaveletSelfAdded, OnWaveletSelfAdded)
  myRobot.register_profile_handler(ProfileHandler)
  
  appengine_robot_runner.run(myRobot)