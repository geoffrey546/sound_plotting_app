from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.graph import MeshLinePlot
from kivy.clock import Clock
from threading import Thread
import audioop
import pyaudio
from kivy.core.window import Window
from kivy.lang import Builder

Window.borderless = True

def capture_mic_data():
    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    p = pyaudio.PyAudio()
    s = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = chunk)
    global levels
    while True:
        data = s.read(chunk)
        mx = audioop.rms(data,2)
        if len(levels) >= 100:
           levels = []
        levels.append(mx)



class Logic(BoxLayout):

    def __init__(self,**kwargs):
        super(Logic,self).__init__(**kwargs)
        self.plot = MeshLinePlot(color=[1,0,0,1])

    def start(self):
        self.ids.graph.add_plot(self.plot)
        Clock.schedule_interval(self.get_value,0.0001)


    def stop(self):
        Clock.unschedule(self.get_value)

    def get_value(self,dt):
        self.plot.points = [(i,j/5) for i,j in enumerate(levels)]

class MainApp(App):
    def build(self):
        return Builder.load_file("main.kv")


levels = []
capture_mic_data_thread = Thread(target = capture_mic_data)
capture_mic_data_thread.daemon = True
capture_mic_data_thread.start()

MainApp().run()
