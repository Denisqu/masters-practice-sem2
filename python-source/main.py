from k_rle import k_rle_code, k_rle_decode

# Import Meteostat library and dependencies
from datetime import datetime
from meteostat import Hourly, Point
import numpy as np
import matplotlib.pyplot as plt

def create_temperature_stream(multiplier: int):
    start = datetime(2018, 6, 1)
    #end = datetime(2018, 1, 1, 23, 59)
    end = datetime(2018, 6, 28, 23, 59)
    saint_petersburg = Point(59.9387, 30.3256, 10) 
    data = Hourly(saint_petersburg, start, end)
    data = data.fetch()
    stream = []
    for temp in data['temp']:
        stream.append(int(temp * 1e7))
    return stream
    
def calc_absolute_loss_k_rle():
    multiplier = 1e7
    source_stream = create_temperature_stream(multiplier)
    i_values = []
    compress_rates = []
    data_losses = []
    for i in range(1, 500 + 1, 10):
        coded_stream = k_rle_code(source_stream, multiplier * i / 100)
        decoded_stream = k_rle_decode(coded_stream, 2048)
        compress_rate = int((1 - (len(coded_stream) / len(source_stream))) * 100)
        data_loss = np.mean( np.array(source_stream) != np.array(decoded_stream) ) * 100
        
        i_values.append(i / 100)
        compress_rates.append(compress_rate)
        data_losses.append(data_loss)
        
        print('-------------------------------')
        print(f'i = {i / 100}, compress_rate = {compress_rate}%, loss = {data_loss}%')
        print('-------------------------------')
        
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(i_values, compress_rates)
    plt.title('Compression Rate vs i')
    plt.xlabel('i')
    plt.ylabel('Compression Rate (%)')

    plt.subplot(1, 2, 2)
    plt.plot(i_values, data_losses)
    plt.title('Data Loss vs i')
    plt.xlabel('i')
    plt.ylabel('Data Loss (%)')

    plt.tight_layout()
    plt.show()    

if __name__ == '__main__':
    calc_absolute_loss_k_rle()
    
    
# 123,456 // % 1
