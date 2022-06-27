import numpy as np
import random
import matplotlib.pyplot as plt

# the number of components
num = 120
# to record the result of placement
size_list = []
pos_list = []

def by_size(t):
    return(-t[0]*t[1])

for iter in range(100):
    # c_list to record the position of component by left-up (x,y) and right-down (x,y)
    c0 = []
    c1 = []
    c2 = []
    c3 = []
    # initialize the position of IC component with (-100,100) and (100,-100)
    min_x = -100
    min_y = -100
    max_x = 100
    max_y = 100
    # to record width and height
    cur_width = max_x - min_x
    cur_height = max_y - min_y
    # arr_list to record the position where components can be placed
    arr0 = [(min_x, max_y)]
    arr1 = [(min_x, min_y)]
    arr2 = [(max_x, min_y)]
    arr3 = [(max_x, max_y)]
    
    com_list = []
    # use random component_size currently,
    # can be replaced by data in component_data.jsonl
    res = np.random.randint(100,size=num * 2)
    for i in range(num):
        if res[2*i] == 0:
            res[2*i] = 1
        if res[2*i + 1] == 0:
            res[2*i + 1] = 1
        com_list.append((res[2*i], res[2*i+1]))

    # optional, to place the component after sorted
    com_list = sorted(com_list,key=by_size)

    for i in range(len(com_list)):
        com = com_list[i]
        cur_width = max_x - min_x
        cur_height = max_y - min_y
        min_space = 1e8
        min_index1 = 5
        min_index = 50
        cur_space = cur_width * cur_height
        width = cur_width
        height = cur_height

        # method1
        if i % 4 == 0:
            for j in range(len(arr0)):
                # get space
                each = arr0[j]
                x = each[0] - com[0]
                y = each[1] - com[1]
                # check if position is available
                available = True
                for item in c0:
                    if (each[0] > item[0] and each[0] < item[2] and y < item[1] and y > item[3]) \
                    or (x > item[0] and x < item[2] and each[1] < item[1] and each[1] > item[3]) \
                    or (x > item[0] and x < item[2] and y < item[1] and y > item[3]):
                        # print(x,y,each[0],each[1],item)
                        available = False
                        break
                if not available:
                    continue
                if x < min_x:
                    width = max_x - x
                if y < min_y:
                    height = max_y - y
                cur_space = width * height
                if cur_space <= min_space:
                    min_space = cur_space
                    min_index = j

            # used to compare with random placement method
            # min_index = random.randint(0,len(arr0)-1)

            each = arr0[min_index]
            x = each[0] - com[0]
            y = each[1] - com[1]
            if x < min_x:
                min_x = x
                cur_width = max_x - x
            if y < min_y:
                min_y = y
                cur_height = max_y - y
            pos = (each[0] - com[0], each[1], each[0], each[1] - com[1])
            arr0.pop(min_index)
            arr0.append((each[0] - com[0], each[1]))
            arr0.append((each[0], each[1] - com[1]))
            c0.append(pos)
            # print(com)
            # print(pos)
        if i % 4 == 1:
            for j in range(len(arr1)):
                each = arr1[j]
                x = each[0] + com[0]
                y = each[1] - com[1]
                available = True
                for item in c1:
                    if (each[0] > item[0] and each[0] < item[2] and y < item[1] and y > item[3]) \
                    or (x > item[0] and x < item[2] and each[1] < item[1] and each[1] > item[3]) \
                    or (x > item[0] and x < item[2] and y < item[1] and y > item[3]):
                        available = False
                        break
                if not available:
                    continue
                if x > max_x:
                    width = x - min_x
                if y < min_y:
                    height = max_y - y
                cur_space = width * height
                if cur_space <= min_space:
                    min_space = cur_space
                    min_index = j
            
            # min_index = random.randint(0,len(arr1)-1)
            each = arr1[min_index]
            x = each[0] + com[0]
            y = each[1] - com[1]
            if x > max_x:
                max_x = x
                cur_width = x - min_x
            if y < min_y:
                min_y = y
                cur_height = max_y - y
            pos = (each[0], each[1], each[0] + com[0], each[1] - com[1])
            arr1.pop(min_index)
            arr1.append((each[0] + com[0], each[1]))
            arr1.append((each[0], each[1] - com[1]))
            c1.append(pos)
            # print(pos)
        if i % 4 == 2:
            for j in range(len(arr2)):
                # get space
                each = arr2[j]
                x = each[0] + com[0]
                y = each[1] + com[1]
                available = True
                for item in c2:
                    if (each[0] > item[0] and each[0] < item[2] and y < item[1] and y > item[3]) \
                    or (x > item[0] and x < item[2] and each[1] < item[1] and each[1] > item[3]) \
                    or (x > item[0] and x < item[2] and y < item[1] and y > item[3]):
                        available = False
                        break
                if not available:
                    continue
                if x > max_x:
                    width = x - min_x
                if y > max_y:
                    height = y - min_y
                cur_space = width * height
                if cur_space <= min_space:
                    min_space = cur_space
                    min_index = j
            
            # min_index = random.randint(0,len(arr2)-1)

            each = arr2[min_index]
            x = each[0] + com[0]
            y = each[1] + com[1]
            if x > max_x:
                max_x = x
                cur_width = x - min_x
            if y > max_y:
                max_y = y
                cur_height = y - min_y
            pos = (each[0], each[1] + com[1], each[0] + com[0], each[1])
            arr2.pop(min_index)
            arr2.append((each[0] + com[0], each[1]))
            arr2.append((each[0], each[1] + com[1]))
            c2.append(pos)
            # print(pos)
        if i % 4 == 3:
            for j in range(len(arr3)):
                # get space
                each = arr3[j]
                x = each[0] - com[0]
                y = each[1] + com[1]
                available = True
                for item in c3:
                    if (each[0] > item[0] and each[0] < item[2] and y < item[1] and y > item[3]) \
                    or (x > item[0] and x < item[2] and each[1] < item[1] and each[1] > item[3]) \
                    or (x > item[0] and x < item[2] and y < item[1] and y > item[3]):
                        available = False
                        break
                if not available:
                    continue
                if x < min_x:
                    width = max_x - x
                if y > max_y:
                    height = y - min_y
                cur_space = width * height
                if cur_space <= min_space:
                    min_space = cur_space
                    min_index = j
            
            # min_index = random.randint(0,len(arr3)-1)
            
            each = arr3[min_index]
            x = each[0] - com[0]
            y = each[1] + com[1]
            if x < min_x:
                min_x = x
                cur_width = max_x - x
            if y > max_y:
                max_y = y
                cur_height = y - min_y
            pos = (each[0] - com[0], each[1] + com[1], each[0], each[1])
            arr3.pop(min_index)
            arr3.append((each[0] - com[0], each[1]))
            arr3.append((each[0], each[1] + com[1]))
            c3.append(pos)
            # print(pos)
        
        # ==================================================================================
        # method2, get position index globally 
        # get position index
        # ==================================================================================
        # for j in range(len(arr0)):
        #     each = arr0[j]
        #     if com[0] >= com[1]:
        #         x = each[0] - com[1]
        #         y = each[1] - com[0]
        #     if com[0] < com[1]:
        #         x = each[0] - com[0]
        #         y = each[1] - com[1]
        #     if x < min_x:
        #         width = max_x - x
        #     if y < min_y:
        #         height = max_y - y
        #     cur_space = width * height
        #     if cur_space <= min_space:
        #         min_space = cur_space
        #         min_index1 = 0
        #         min_index = j
        
        # for j in range(len(arr1)):
        #     each = arr1[j]
        #     if com[0] >= com[1]:
        #         x = each[0] + com[0]
        #         y = each[1] - com[1]
        #     if com[0] < com[1]:
        #         x = each[0] + com[1]
        #         y = each[1] - com[0]
        #     if x > max_x:
        #         width = x - min_x
        #     if y < min_y:
        #         height = max_y - y
        #     cur_space = width * height
        #     if cur_space <= min_space:
        #         min_space = cur_space
        #         min_index1 = 1
        #         min_index = j

        # for j in range(len(arr2)):
        #     each = arr2[j]
        #     if com[0] >= com[1]:
        #         x = each[0] + com[1]
        #         y = each[1] + com[0]
        #     if com[0] < com[1]:
        #         x = each[0] + com[0]
        #         y = each[1] + com[1]
        #     if x > max_x:
        #         width = x - min_x
        #     if y > max_y:
        #         height = y - min_y
        #     cur_space = width * height
        #     if cur_space <= min_space:
        #         min_space = cur_space
        #         min_index1 = 2
        #         min_index = j

        # for j in range(len(arr3)):
        #     each = arr3[j]
        #     if com[0] >= com[1]:
        #         x = each[0] - com[0]
        #         y = each[1] + com[1]
        #     if com[0] < com[1]:
        #         x = each[0] - com[1]
        #         y = each[1] + com[0]
        #     if x < min_x:
        #         width = max_x - x
        #     if y > max_y:
        #         height = y - min_y
        #     cur_space = width * height
        #     if cur_space <= min_space:
        #         min_space = cur_space
        #         min_index1 = 3
        #         min_index = j
        # ==================================================================
        # place the component
        # ==================================================================
        # if min_index1 == 0:
        #     each = arr0[min_index]
        #     x = each[0] - com[0]
        #     y = each[1] - com[1]
        #     if x < min_x:
        #         min_x = x
        #         cur_width = max_x - x
        #     if y < min_y:
        #         min_y = y
        #         cur_height = max_y - y
        #     pos = (each[0] - com[0], each[1], each[0], each[1] - com[1])
        #     arr0.pop(min_index)
        #     arr0.append((each[0] - com[0], each[1]))
        #     arr0.append((each[0], each[1] - com[1]))
        #     c0.append(pos)        
        # if min_index1 == 1:
        #     each = arr1[min_index]
        #     x = each[0] + com[0]
        #     y = each[1] - com[1]
        #     if x > max_x:
        #         max_x = x
        #         cur_width = x - min_x
        #     if y < min_y:
        #         min_y = y
        #         cur_height = max_y - y
        #     pos = (each[0], each[1], each[0] + com[0], each[1] - com[1])
        #     arr1.pop(min_index)
        #     arr1.append((each[0] + com[0], each[1]))
        #     arr1.append((each[0], each[1] - com[1]))
        #     c1.append(pos)
        # if min_index1 == 2:
        #     each = arr2[min_index]
        #     x = each[0] + com[0]
        #     y = each[1] + com[1]
        #     if x > max_x:
        #         max_x = x
        #         cur_width = x - min_x
        #     if y > max_y:
        #         max_y = y
        #         cur_height = y - min_y
        #     pos = (each[0], each[1] + com[1], each[0] + com[0], each[1])
        #     arr2.pop(min_index)
        #     arr2.append((each[0] + com[0], each[1]))
        #     arr2.append((each[0], each[1] + com[1]))
        #     c2.append(pos)
        # if min_index1 == 3:
        #     each = arr3[min_index]
        #     x = each[0] - com[0]
        #     y = each[1] + com[1]
        #     if x < min_x:
        #         min_x = x
        #         cur_width = max_x - x
        #     if y > max_y:
        #         max_y = y
        #         cur_height = y - min_y
        #     pos = (each[0] - com[0], each[1] + com[1], each[0], each[1])
        #     arr3.pop(min_index)
        #     arr3.append((each[0] - com[0], each[1]))
        #     arr3.append((each[0], each[1] + com[1]))
        #     c3.append(pos)

        # =======================================================
        # plot the result
        # =======================================================
        # if i == len(com_list) - 1:
        #     fig = plt.figure()
        #     ax1 = fig.add_subplot(111)
        #     rect = plt.Rectangle((-100,-100),200,200,linewidth=1,edgecolor='grey',facecolor='green')
        #     ax1.add_patch(rect)
        #     for i in c0:
        #         pos = (i[0],i[1])
        #         width = i[2] - i[0]
        #         height = i[3] - i[1]
        #         rect = plt.Rectangle(pos,width,height,linewidth=1,edgecolor='grey',facecolor='red')
        #         ax1.add_patch(rect)
        #     for i in c1:
        #         pos = (i[0],i[1])
        #         width = i[2] - i[0]
        #         height = i[3] - i[1]
        #         rect = plt.Rectangle(pos,width,height,linewidth=1,edgecolor='grey',facecolor='blue')
        #         ax1.add_patch(rect)
        #     for i in c2:
        #         pos = (i[0],i[1])
        #         width = i[2] - i[0]
        #         height = i[3] - i[1]
        #         rect = plt.Rectangle(pos,width,height,linewidth=1,edgecolor='grey',facecolor='orange')
        #         ax1.add_patch(rect)
        #     for i in c3:
        #         pos = (i[0],i[1])
        #         width = i[2] - i[0]
        #         height = i[3] - i[1]
        #         rect = plt.Rectangle(pos,width,height,linewidth=1,edgecolor='grey',facecolor='purple')
        #         ax1.add_patch(rect)
        #     plt.xlim(min_x, max_x)
        #     plt.ylim(min_y, max_y)
        #     plt.show()

    # to record the result
    com_size = 0
    for i in com_list:
        com_size += i[0]*i[1]
    cur_size = (max_x - min_x)*(max_y - min_y)
    size_list.append((com_size + 40000) / cur_size)
    cur_pos = (-min_x / (max_x - min_x), -min_y / (max_y - min_y))
    pos_list.append(cur_pos)
    
# print(size_list)

# to calculate the average result
size_sum = 0
for i in size_list:
    size_sum += i
print(size_sum / len(size_list))

pos_1 = 0
pos_2 = 0

for i in pos_list:
    pos_1 += i[0]
    pos_2 += i[1]
print(pos_1 / len(pos_list))
print(pos_2 / len(pos_list))
