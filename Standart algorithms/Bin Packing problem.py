def best_fit(packages, max_package, obj):
    for i in range(len(packages)):
        if max_package - packages[i] >= obj:
            packages[i] += obj
            return
    packages.append(obj)

n = int(input())
objects = list(map(int,input().split()))
max_package = int(input())
objects.sort(reverse = True)
packages = []
for obj in objects:
    best_fit(packages, max_package, obj)
print(len(packages))

# input:
# n - number of objects to load
# weights of objects
# max weight of a container
