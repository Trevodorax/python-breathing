from playsound import playsound
from time import sleep
from math import floor
import threading

sound_duration = 1
default_breath_out_duration = 4
default_breath_in_duration = 4
default_pause_duration = 4
default_session_duration = 60

def main():
  if(input('Do you want to enter custom durations ? (y / n)') == 'y'):
    breath_in_duration, breath_out_duration, pause_duration, session_duration = getCustomDurations()
  else:
    breath_in_duration = default_breath_in_duration
    breath_out_duration = default_breath_out_duration
    pause_duration = default_pause_duration
    session_duration = default_session_duration

  launch_session(
    breath_in_duration, 
    pause_duration, 
    breath_out_duration, 
    session_duration
  )

def getCustomDurations():
  breath_in_duration = int(input('Breath in duration: '))
  breath_out_duration = int(input('Breath out duration: '))
  pause_duration = int(input('Pause between breaths: '))
  session_duration = int(input('Total session duration: '))
  return breath_in_duration, breath_out_duration, pause_duration, session_duration

def launch_session(breath_in_duration, pause_duration, breath_out_duration, session_duration):
  number_of_iterations = get_number_of_iterations(breath_in_duration, breath_out_duration, pause_duration, session_duration)
  for i in range(number_of_iterations):
    breath_step('Breathe in', breath_in_duration)
    breath_step('Hold', pause_duration)
    breath_step('Breathe out', breath_out_duration)
    breath_step('Hold', pause_duration)

def breath_step(message, duration):
  print('\r\033[K', end='')
  make_sound()
  print(message)
  sleep(duration)

def get_number_of_iterations(breath_in_duration, breath_out_duration, pause_duration, session_duration):
  iteration_duration = breath_in_duration + pause_duration + breath_out_duration + (4 * sound_duration) 
  number_of_iterations = floor(session_duration / iteration_duration)
  return number_of_iterations

def make_sound():
  audio_thread = threading.Thread(target=playsound, args=('ding.mp3',))
  audio_thread.start()

main()
