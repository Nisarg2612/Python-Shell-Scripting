def fahr_to_cal(temp_cal):
    temp_cal = (temp_fahr - 32) * (5/9)
    print("{} F temp ={: .2f} C".format(temp_fahr, temp_cal))

temp_fahr = int(input("Enter number to convert temperature from Fahrenheit to Celsius: "))
fahr_to_cal(temp_fahr)