"""
Class used for generating tone. Originally downloaded from:
    http://markjones112358.co.nz/projects/Python-Tone-Generator/
Only very slight modifications made!
"""

import numpy
import pyaudio
import math


class ToneGenerator(object):

    def __init__(self, samplerate=44100, frames_per_buffer=2205):
        self.p = pyaudio.PyAudio()
        self.samplerate = samplerate
        self.frames_per_buffer = frames_per_buffer
        self.streamOpen = False
        self.notes = [False]*7

    def sinewave(self,frequency):
        omega = float(frequency) * (math.pi * 2) / self.samplerate
        xs = numpy.arange(self.buffer_offset,
                          self.buffer_offset + self.frames_per_buffer)
        out = self.amplitude * numpy.sin(xs * omega)
        return out

    def callback(self, in_data, frame_count, time_info, status):
        self.buffer_offset = self.buffer_offset%(44100*60)
        data = numpy.zeros(self.frames_per_buffer).astype(numpy.float32)
        if self.notes[0]:
            data += self.sinewave(261.63).astype(numpy.float32)
        if self.notes[1]:
            data += self.sinewave(293.66).astype(numpy.float32)
        if self.notes[2]:
            data += self.sinewave(329.63).astype(numpy.float32)
        if self.notes[3]:
            data += self.sinewave(349.23).astype(numpy.float32)
        if self.notes[4]:
            data += self.sinewave(392.00).astype(numpy.float32)
        if self.notes[5]:
            data += self.sinewave(440.00).astype(numpy.float32)
        if self.notes[6]:
            data += self.sinewave(493.88).astype(numpy.float32)
        data = data
        self.buffer_offset += self.frames_per_buffer
        return (data.tostring(), pyaudio.paContinue)

    def update_frequency(self, frequency):
        self.omega = float(frequency) * (math.pi * 2) / self.samplerate

    def switch(self,note,switch):
        if switch=="on":
            self.notes[note] = True
        else:
            self.notes[note] = False

    def is_playing(self):
        if self.stream.is_active():
            return True
        else:
            if self.streamOpen:
                self.stream.stop_stream()
                self.stream.close()
                self.streamOpen = False
            return False

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.streamOpen = False

    def play(self, frequency, duration, amplitude):
        self.amplitude = amplitude
        self.buffer_offset = 0
        self.streamOpen = True
        self.on = True
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.samplerate,
                                  output=True,
                                  frames_per_buffer=self.frames_per_buffer,
                                  stream_callback=self.callback)