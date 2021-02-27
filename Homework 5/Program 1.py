def my_range(num, end, dif):
    while num < end:
        yield num
        num += dif  
        
for i in my_range(0,5,2):
    print(i)
