import numpy as np
import time


t0 = time.perf_counter()

INPUT = np.loadtxt('./input/day1-1.txt', dtype=np.int64)
coefs = np.zeros(np.shape(INPUT)[0], dtype=np.int64)
for i, entry0 in enumerate(INPUT[:,0]):
    count = 0
    for entry1 in INPUT[:,1]:
        count += entry0 == entry1
    coefs[i] = count
    
print(np.sum(coefs * INPUT[:,0]))
print(f'Completed in {time.perf_counter()-t0}s.')


# t0 = time.perf_counter()

# INPUT = np.loadtxt('./input/day1-1.txt', dtype=np.int64)

# base_list = INPUT[:,0].tolist()
# comp_list = INPUT[:,1].tolist()
# # compare = np.linspace(0, np.shape(INPUT)-1, 1, dtype=np.int64).tolist()
# # counts = np.zeros(np.shape(INPUT)[0], dtype=np.int64)

# def count(A):
#     '''
#     return a map of the frequency of each element in A
#     '''
#     assert type(A) == list or np.NDArray
#     out = {}
#     for element in A:
#         try:
#             out[element] += 1
#         except KeyError:
#             out[element] = 1

# counts = count(comp_list)

# similarity = 0
# for element in base_list:
#     try:
#         similarity += element*counts[element]
#     except KeyError:
#         break

# print(similarity)
# print(f'Completed in {time.perf_counter()-t0}s.')