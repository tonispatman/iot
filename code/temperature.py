import clr  # Install pythonnet: pip install pythonnet

clr.AddReference("System")
clr.AddReference("System.Management")

from System.Management import ManagementObjectSearcher

def get_cpu_temperature_windows():
    try:
        searcher = ManagementObjectSearcher("root\\WMI", "SELECT * FROM MSAcpi_ThermalZoneTemperature")
        for obj in searcher.Get():
            temp_kelvin = obj["CurrentTemperature"]
            temp_celsius = (temp_kelvin - 2732) / 10.0  # Convert tenths of Kelvin to Celsius
            return temp_celsius
    except Exception as e:
        print(f"Error reading CPU temperature: {e}")
        return None

if __name__ == "__main__":
    temp = get_cpu_temperature_windows()
    if temp is not None:
        print(f"CPU Temperature: {temp:.2f}°C")
    else:
        print("Unable to read CPU temperature.")
