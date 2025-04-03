from django.test import TestCase

# Create your tests here.

matrix = [[1, 0, 0, 1, 0],
          [1, 0, 1, 0, 0],
          [0, 0, 1, 0, 0],
          [1, 0, 1, 0, 1],
          [1, 0, 1, 1, 1],
          ]


# You have to conncet the revers of the matrix and calculate the size of them [1, 2, 2, 2, 5]

blocks_dict = {}
revers = {}

for dx_, line in enumerate(matrix, start=1):
    for dy_, col_values in enumerate(line, start=1):
        blocks_dict[f'B{dx_, dy_}'] = col_values

for dx_, line in enumerate(matrix, start=1):
    for dy_, col_values in enumerate(line, start=1):
        blocks_dict[f'B{dx_, dy_}'] = col_values


# for i in range(len(matrix)):
#     size = 0
#     for j in range(len(matrix)):
#         if blocks_dict[f'B{i}{j}'] or blocks_dict[f'B{j}{i}']:
#             size += 1
#             revers[f'r{i,j}'] = size 











































# class Block():
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.size = 1

#     #def __eq__(self, other) -> bool:
#     #  return self.x == other.x or self.y == other.y
    
# all_dimensions_blocks = []


# for dy_, line in enumerate(matrix, start=1):
#     for dx_, col in enumerate(line, start=1):
#         if col:
#            all_dimensions_blocks.append([dx_, dy_])
           

# print(all_dimensions_blocks)
# block_dict = {}
# #[[1, 1], [1, 4], [2, 1], [2, 3], [3, 3], [4, 1], [4, 3], [4, 5], [5, 1], [5, 3], [5, 4], [5, 5]]
# for block in all_dimensions_blocks:
  
#     block = Block(block[0], block[1])
#     #all_dimensions_blocks.pop(1)
#     for other_block in all_dimensions_blocks:
#         if block.x == other_block[0]:
#             x_eq_blocks = []
#             x_eq_blocks.append(other_block)
#             for bl in x_eq_blocks:
#                 if block.y + 1 == bl[1]:
#                     block.size += 1
#                     block_dict[f'B{block.x, block.y}'] = block.size

#             if block.y == other_block[1]:
#                 y_eq_blocks = []
#                 y_eq_blocks.append(other_block)
#                 for bl in y_eq_blocks:
#                     if block.x + 1 == bl[0]:
#                         block.size += 1
#                         block_dict[f'B{block.x, block.y}'] = block.size

#     for other_block in all_dimensions_blocks:
#         if block.y == other_block[1]:
#             y_eq_blocks = []
#             y_eq_blocks.append(other_block)
#             for bl in y_eq_blocks:
#                 if block.y + 1 == bl[0]:
#                     block.size += 1
#                     block_dict[f'B{block.x, block.y}'] = block.size

#             if block.x == other_block[0]:
#                 x_eq_blocks = []
#                 x_eq_blocks.append(other_block)
#                 for bl in x_eq_blocks:
#                     if block.x + 1 == bl[1]:
#                         block.size += 1
#                         block_dict[f'B{block.x, block.y}'] = block.size


# print(block_dict)

# [
#  [1, 1], [  ], [  ], [4, 1], [  ] 
#  [1, 2], [  ], [3, 2], [  ], [  ]
#  [  ],   [  ], [3, 3], [  ], [  ]
#  [1, 4], [  ], [3, 4], [  ],[5, 4]
#  [1, 5],[   ],[3, 5],[4, 5],[5, 5]]

# for obj in all_dimensions_blocks:
#     block = Block(obj[0], obj[1])
#     for other_obj in all_dimensions_blocks:
#         if block.x == other_obj.x or block.y == other_obj.y:
#             block.size += 1
    