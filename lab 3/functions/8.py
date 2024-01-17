def spy_game(nums):
    a = ""
    for i in range(len(nums)):
        if nums[i] == 0 or nums[i] == 7:
            a+=str(nums[i])
    print("True" if "007" in a else "False")
            

spy_game([1,2,4,0,0,7,5])
spy_game([1,0,2,4,0,5,7])
spy_game([1,7,2,0,4,5,0])