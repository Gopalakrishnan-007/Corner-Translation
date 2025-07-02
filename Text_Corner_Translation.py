#Program for Corner Translation. Input : Any String of square length(1,4,9,16..)
def spiral_layers(matrix):

    rows, cols = len(matrix), len(matrix[0])
    layers = []
    left, right, top, bottom = 0, cols - 1, 0, rows - 1

    while left <= right and top <= bottom:
        current_layer = []

        # Traverse down along the left column
        for i in range(top, bottom + 1):
            current_layer.append(matrix[i][left])
        left += 1

        # Traverse right along the bottom row
        for i in range(left, right + 1):
            current_layer.append(matrix[bottom][i])
        bottom -= 1

        # Traverse up along the right column (if within bounds)
        if left <= right:
            for i in range(bottom, top - 1, -1):
                current_layer.append(matrix[i][right])
            right -= 1

        # Traverse left along the top row (if within bounds)
        if top <= bottom:
            for i in range(right, left - 1, -1):
                current_layer.append(matrix[top][i])
            top += 1

        # Add the current layer to the layers list
        layers.append(current_layer)

    return layers



def reconstruct_matrix(layers, rows, cols):
    
    # Initialize an empty matrix
    matrix = [[0] * cols for _ in range(rows)]

    left, right, top, bottom = 0, cols - 1, 0, rows - 1

    layer_index = 0
    while left <= right and top <= bottom:
        current_layer = layers[layer_index]
        index = 0

        # Fill down the left column
        for i in range(top, bottom + 1):
            matrix[i][left] = current_layer[index]
            index += 1
        left += 1

        # Fill right along the bottom row
        for i in range(left, right + 1):
            matrix[bottom][i] = current_layer[index]
            index += 1
        bottom -= 1

        # Fill up the right column (if within bounds)
        if left <= right:
            for i in range(bottom, top - 1, -1):
                matrix[i][right] = current_layer[index]
                index += 1
            right -= 1

        # Fill left along the top row (if within bounds)
        if top <= bottom:
            for i in range(right, left - 1, -1):
                matrix[top][i] = current_layer[index]
                index += 1
            top += 1

        layer_index += 1

    return matrix


def convert_to_2d(array):
    n = int(len(array) ** 0.5)  # Calculate the size of the 2D array (n x n)
    if n * n != len(array):
        raise ValueError("The input array does not have n^2 elements.")
    return [array[i * n:(i + 1) * n] for i in range(n)]

def convert_to_1d(matrix):
    return [element for row in matrix for element in row]


def decrypt_to_corner(array,n,i):
  #array is 1D array input
  temp = []
  for k in range(4*n-4):
    temp.append(array[k])
  dec.append(temp)




def find(arr,k,ss):
  anss=[]
  size=len(arr[k])
  for i in range(ss):
    j=0
    for _ in range(4):
      anss.append(arr[k][j])
      j = (j+ss)%size
    arr[k] = arr[k][size-1:]+arr[k][:size-1]
  if anss:
      ans.append(anss)

input_text = input("Enter any string of length n^2: ")
L = list(input_text)
matrix = convert_to_2d(L)
#print(matrix)

'''matrix = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13 ,14, 15],
    [16, 17, 18, 19, 20],
    [21, 22 , 23,24,25]
]'''
arr = spiral_layers(matrix)
#print(arr)
n = len(matrix)-1
ans = []
for i in range(len(arr)):
  find(arr,i,n)
  n-=2
if len(arr[-1]) == 1:
  ans.append(arr[-1])

enc_mat = convert_to_1d(ans)
enc_text = "".join(enc_mat)
print("Final encrypted text = ",enc_text)

array = list(enc_text)
#print(array)
n = int(len(array)**0.5)
dec = []
i=0
while n > 1:
  decrypt_to_corner(array,n,i)
  i+=1
  array = array[4*n-4:]
  n-=2
if len(array) == 1:
  dec.append(array)

ans = dec

Final_decrypted_matrix = []
def decrypt_corner(ans,n,i):
  a=[]
  b=[]
  c=[]
  d=[]
  arr_num = 0
  temp = ans[i]
  for i in temp:
    if arr_num == 0:
      a = [i]+a
      arr_num = (arr_num+1)%4
    elif arr_num == 1:
      b = [i]+b
      arr_num = (arr_num+1)%4
    elif arr_num == 2:
      c = [i]+c
      arr_num = (arr_num+1)%4
    elif arr_num == 3:
      d = [i]+d
      arr_num = (arr_num+1)%4
  res = a+b+c+d
  res = res[n-2:]+res[:n-2]
  Final_decrypted_matrix.append(res)
  
n = len(matrix)
for i in range(len(ans)):
  decrypt_corner(ans,n,i)
  n-=2

#print(Final_decrypted_matrix)


d1=reconstruct_matrix(Final_decrypted_matrix,len(matrix),len(matrix))
Final_decrypted_text = "".join(convert_to_1d(d1))
print("Decrypted = ",Final_decrypted_text)
if Final_decrypted_text == input_text:
  print("Decryption Successful")
else:
  print("Decryption failed!!")

