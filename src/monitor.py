import pynvml
import time 
import numpy as np
import threading

class Monitor():
    def __init__(self, sample_interval = 1, time_window = 300):

        # GPU temperature setup
        pynvml.nvmlInit()
        self.device_count = pynvml.nvmlDeviceGetCount()
        self.gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        self.gpu_name = pynvml.nvmlDeviceGetName(self.gpu_handle)

        self.gpu_t = np.zeros(time_window)
        self.timer = 0

        self.time_window = time_window

    def __del__(self):
        pynvml.nvmlShutdown()


    def run(self):
        while True:
            time.sleep(1)
            self.gpu_t[self.timer] = self.get_gpu_temp()
            self.timer += 1
            if self.timer == self.time_window:
                print (f"Average temperature within last 5 minutes was: {self.gpu_t.sum() / self.timer}")
                print (f"Temperature peak within last 5 minutes was: {np.max(self.gpu_t)}")
                self.timer = self.timer % self.time_window


    def get_gpu_temp(self):
        return pynvml.nvmlDeviceGetTemperature(
            self.gpu_handle, pynvml.NVML_TEMPERATURE_GPU
        )

            
        