def twoSum(nums, target):

    str3 = {}

    for i in range(len(nums)):

        if target - nums[i] in str3:
            return [str3[target - nums[i]], i]   
        else:
            str3[nums[i]] = i

string = list(map(int, input("Please enter list of numbers: ")))
str2 = int(input("Enter the target number: "))
print(twoSum(string, str2))
