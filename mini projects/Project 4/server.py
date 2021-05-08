import psutil
import time
from time import localtime, strftime
import json
import asyncio
import websockets
import subprocess


def get_cpu_reading():
	cpu = {}  # we will store the cpu readings here
	cpu_readings = psutil.cpu_percent(interval=1, percpu=True)

	#{"cpu0": 4.6, "cpu1": 6.2, "cpu2": 13.8, "cpu3": 6.2, "cpu4": 13.8, "cpu5": 4.6, "cpu6": 12.3, "cpu7": 6.2}
	for i in range(0, len(cpu_readings)):
		cpu['cpu'+str(i)] = cpu_readings[i]
	return cpu

    #{"one_min": 0.0, "five_min": 0.0, "fifteen_min": 0.0}
def get_load_averages():
	load_avg = [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]
	mapped_avg = {
		"one_min": load_avg[0], "five_min": load_avg[1], "fifteen_min": load_avg[2]}
	return mapped_avg

    # virtual_memory_utilized": 42.7
def get_memory():
	mem = psutil.virtual_memory()
	return mem[2]

    #"disk_utilized": 17.6
def get_disk():
	disk = psutil.disk_usage('/')
	return disk[3]

def get_network_traffic(pernic=True):
    #net_red = {} # will store the network data reading here
    net_tarf = psutil.net_io_counters()
    net_data = {
        "Packets_Sent": net_tarf.packets_sent, "Packets_Rec": net_tarf.packets_recv, "Bytes_sent": net_tarf.bytes_sent, "Bytes_Rec": net_tarf.bytes_recv
    }
    #for i in range(len(net_tarf)) : net_red[str(i)] = net_tarf[i]
    return net_data

def get_signal_strength():
    stats = psutil.net_if_stats()

    for nic in stats:
        st = stats[nic]
        net_info = {
            "Signal Strength": st.speed
        }
    return net_info

async def client(websocket, path):
    name = await websocket.recv()
    await asyncio.sleep(1)  # sleep for 1 second
    reading_time = strftime("%H:%M:%S", localtime())
    send_obj = json.dumps({"time": reading_time,\
                       "cpu": get_cpu_reading(),\
                       "load_avg": get_load_averages(),\
                       "virtual_memory_utilized": get_memory(),\
                       "disk_utilized": get_disk(),\
                       "network_traffic":get_network_traffic(), \
                        "Internet_Signal": get_signal_strength(),
                        })
    await websocket.send(send_obj)
    print(send_obj)

start_server = websockets.serve(client, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
