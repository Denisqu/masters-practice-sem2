from typing import List

def k_rle_code(stream:List[int], K:int) -> List[int]:
    result_stream = []
    count = 0
    repeat_count = 0
    ST = 0
    
    def insert_func():
        if repeat_count < 4:
            result_stream.extend([ST] * (repeat_count + 1))
        else:
            result_stream.extend([repeat_count, ST])    
    
    for i, newT in enumerate(stream):
        count += 1
        if count == 1:
            ST = newT
            continue
        if (newT + K > ST and newT - K < ST) or newT == ST:
            repeat_count += 1
            continue
        insert_func()
        repeat_count = 0
        ST = newT
    insert_func()  
        
    return result_stream

def k_rle_decode(stream:List[int], threshold:int) -> List[int]:
    result_stream = []
    i = 0
    while i < len(stream):
        if stream[i] < threshold and stream[i] > 0:
            result_stream.extend([stream[i+1]] * (stream[i] + 1))
            i += 2
        else:
            current = stream[i]
            result_stream.append(current)
            i += 1 
    return result_stream