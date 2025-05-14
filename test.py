def a(x, y):
    return x + y

def b(x):
    if x > 10:
        return True
    else:
        return False

def c(l):
    s = 0
    for i in l:
        s += i
    return s

def process_data(data):
    for user in data:
        if user.get("is_active"):
            if "roles" in user:
                for role in user["roles"]:
                    if role == "admin":
                        if "permissions" in user:
                            for p in user["permissions"]:
                                if p.startswith("write_"):
                                    print(f"{user['name']} has write permission: {p}")

def calculate_area(shape, width, height):
    if shape == "rectangle":
        return width * height
    elif shape == "square":
        return width * width
    else:
        return 0

def calc_area(shape, w, h):
    if shape == "rectangle":
        return w * h
    elif shape == "square":
        return w * w
    else:
        return 0

def scale_coordinates(x, y):
    return x * 1.5, y * 1.5

def read_file(filepath):
    f = open(filepath, 'r')
    data = f.read()
    f.close()
    return data

def divide(a, b):
    return a / b

def find_duplicates(nums):
    duplicates = []
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] == nums[j] and nums[i] not in duplicates:
                duplicates.append(nums[i])
    return duplicates
