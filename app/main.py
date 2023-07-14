from playsound import playsound
from time import sleep
from math import floor
from tkinter import Tk, Canvas
import threading

default_breath_out_duration = 4
default_breath_in_duration = 4
default_pause_duration = 4
default_session_duration = 60
window_size = 500
ball_max_radius = 200
ball_id = None

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
  window = init_graphical_interface()
  canvas = init_canvas(window)
  create_ball(canvas, 10)

  def animate_ball():
    inflate_ball(canvas, breath_in_duration)
    window.after(pause_duration * 1000, lambda: deflate_ball(canvas, breath_out_duration))
    window.after((2 * pause_duration + breath_out_duration) * 1000, animate_ball)

  animate_ball()
  window.after(session_duration * 1000, window.quit)
  window.mainloop()

def breath_step(message, duration):
  print('\r\033[K', end='')
  make_sound()
  print(message, end='', flush=True)
  sleep(duration)

def init_graphical_interface():
  root = Tk()
  root.title('Python square breathing')
  root.geometry(f'{window_size}x{window_size}')
  return root

def init_canvas(window):
  canvas = Canvas(window, width=window_size, height=window_size)
  canvas.pack()
  return canvas

def create_ball(canvas, radius):
  global ball_id

  center_x = window_size // 2
  center_y = window_size // 2
  circle_x1 = center_x - radius
  circle_y1 = center_y - radius
  circle_x2 = center_x + radius
  circle_y2 = center_y + radius
  ball_id = canvas.create_oval(circle_x1, circle_y1, circle_x2, circle_y2, fill='red')

def inflate_ball(canvas, duration):
  radius = 10
  growth_per_deciSecond = (ball_max_radius - radius) / duration / 10

  make_sound()
  for i in range(duration * 10):
    sleep(0.1)
    update_ball(canvas, radius)
    radius += growth_per_deciSecond
  make_sound()

def deflate_ball(canvas, duration):
  radius = ball_max_radius
  shrink_per_deciSecond = radius / duration / 10

  make_sound()
  for i in range(duration * 10):
    sleep(0.1)
    update_ball(canvas, radius)
    radius -= shrink_per_deciSecond
  make_sound()

def update_ball(canvas, radius):
  global ball_id

  canvas.delete(ball_id)
  center_x, center_y = window_size // 2, window_size // 2
  circle_x1, circle_y1 = center_x - radius, center_y - radius
  circle_x2, circle_y2 = center_x + radius, center_y + radius

  fraction_red = (ball_max_radius - radius) / ball_max_radius
  fraction_blue = radius / ball_max_radius

  red = int(fraction_red * 255)
  blue = int(fraction_blue * 255)
  green = 0
  ball_id = canvas.create_oval(circle_x1, circle_y1, circle_x2, circle_y2, fill=getHexadecimalColor(red, green, blue))
  canvas.update()

def get_number_of_iterations(breath_in_duration, breath_out_duration, pause_duration, session_duration):
  iteration_duration = breath_in_duration + pause_duration + breath_out_duration
  number_of_iterations = floor(session_duration / iteration_duration)
  return number_of_iterations

def make_sound():
  audio_thread = threading.Thread(target=playsound, args=('pok.mp3',))
  audio_thread.start()

def getHexadecimalColor(red, green, blue):
  red = int(red)
  green = int(green)
  blue = int(blue)

  hex_code = '#%02x%02x%02x' % (red, green, blue)
  return hex_code


main()
