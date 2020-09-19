import pyaudio, struct, numpy as np, pyttsx3
from scipy import signal
from scipy.fftpack import fft,ifft
from python_speech_features import mfcc

class voice():
    
    def __init__(self, chunk = 4410 * 5, rate = 44100):
        
        # PyAudio
        self.chunk = chunk		    
        self.format = pyaudio.paInt16      
        self.channels = 1		            
        self.rate = rate	            
        self.p = pyaudio.PyAudio()
        self.chosen_device_index = -1
        for x in range(0,self.p.get_device_count()):
            info = self.p.get_device_info_by_index(x)
            if info["name"] == "pulse":
                self.chosen_device_index = info["index"]
        self.stream = self.p.open(format = self.format,
	                        channels = self.channels,
	                        rate = self.rate,
	                        input_device_index = self.chosen_device_index,
	                        input = True,
	                        output = True,
	                        frames_per_buffer = self.chunk)

        # Pyttsx
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)

    def v_real(self, norm = False):

        data = self.stream.read(self.chunk)
        data_in = np.array(struct.unpack(str(2 * self.chunk)+'B', data), dtype='b')[::2]
        if norm == False:
            return data_in
        else:
            data_in = data_in/255.0
            return data_in

    def v_filter(self, data, low, high):

        low = low/(self.rate/2)
        high = high/(self.rate/2)
        bl,al = signal.butter(9,high,'low')
        bh,ah = signal.butter(9,low,'high')
        data_in = signal.filtfilt(bh, ah, data)
        data_in = signal.filtfilt(bl, al, data)
        return data_in

    def trace_sp(self, norm = False):
        try:
            p1 = 0
            count = 0
            d = []
            while (p1 >= 2500) | (count < 3):
                q = self.v_real()
                q1 = np.where(np.diff(np.sign(q)))[0]
                p1 = len(q1)
                d = np.concatenate([d, q])
                if p1 >= 2500:
                    count = 3
                else:
                    count += 1
            if norm == False:
                return d
            else:
                d = d / 255.0
                return d
        except KeyboardInterrupt:
            print('Interruption...')
        except Exception as e:
	        print(str(e))

    def terminate_voice(self):

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def v_fft(self, data):
        
        a = len(data)
        data_fft = fft(np.abs(data))
        data_fft = data_fft[0 : a//2] * 2 / a
        return data_fft


if __name__ == '__main__':
    v = voice(chunk = 4410 * 5)
    d = v.trace_sp()
    v. terminate_voice()
            
            
                            
