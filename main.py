from src.monitor import Monitor
from src.temperatureOverlay import TemperatureOverlay

resolution = "QHD"

def main():
    m = Monitor()
    
    to = TemperatureOverlay(resolution) # pos argument is set for QHD monitor by default
    to.run()


if __name__ == "__main__":
    main()