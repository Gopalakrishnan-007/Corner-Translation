
def logistic_key(x, r1, y, r2, size):
    """
    Generate a list of pseudo-random keys using the logistic equation.
    """
    key = []
    for i in range(size):   
        x = r1 * x * (1 - x)  # The logistic equation
        y = r2 * y * (1 - y)
        temp = [int((x * pow(10, 16)) % 256),int((y * pow(10, 16)) % 256)]  # Map to 0-255
        key.append(temp)
    return key

  
def encrypt_function_1(p1,x):
  return (p1+x)%256

def encrypt_function_2(p2):
  even_bits = p2 & 0xAA
  odd_bits = p2 & 0x55
  even_bits = even_bits>>1
  odd_bits = odd_bits<<1
  return odd_bits | even_bits


def decrypt_function_1(c1,x):
  return (c1-x)%256

def decrypt_function_2(p2):
  even_bits = p2 & 0xAA
  odd_bits = p2 & 0x55
  even_bits = even_bits>>1
  odd_bits = odd_bits<<1
  return odd_bits | even_bits

def circular_left_shift(value, shift, bit_width=8):
    # Ensure the shift is within the range of the bit width
    shift %= bit_width
    
    # Perform the circular left shift
    left_shifted = (value << shift) & ((1 << bit_width) - 1)  # Mask ensures we stay within bit width
    wrapped_around = value >> (bit_width - shift)
    result = left_shifted | wrapped_around
    return result

def circular_right_shift(value, shift, bit_width=8):
    # Ensure the shift is within the range of the bit width
    shift %= bit_width
    
    # Perform the circular right shift
    right_shifted = (value >> shift)  # Shift to the right
    wrapped_around = (value << (bit_width - shift)) & ((1 << bit_width) - 1)  # Wrap around to the left
    result = right_shifted | wrapped_around
    return result


def encrypt(value):
  
  byte4 = value & 0xFF          # Extract 1st byte (LSB)
  byte3 = (value >> 8) & 0xFF   # Extract 2nd byte
  byte2 = (value >> 16) & 0xFF  # Extract 3rd byte
  byte1 = (value >> 24) & 0xFF  # Extract 4th byte (MSB)
  
  
  
  e1 = encrypt_function_1(byte1,X)
  e2 = encrypt_function_2(byte2)
  e3 = encrypt_function_2(byte3)
  e4 = encrypt_function_1(byte4,Y)
  

  C1 = circular_left_shift(e1,2)
  C4 = circular_left_shift(e4,2)

  C3 = C1 ^ e2
  C2 = C4 ^ e3
  result = (C1 << 24) | (C2 << 16) | (C3 << 8) | C4
  return result


def decrypt(value):
  byte4 = value & 0xFF          # Extract 1st byte (LSB)
  byte3 = (value >> 8) & 0xFF   # Extract 2nd byte
  byte2 = (value >> 16) & 0xFF  # Extract 3rd byte
  byte1 = (value >> 24) & 0xFF  # Extract 4th byte (MSB)

  d1 = circular_right_shift(byte1,2)
  p1 = decrypt_function_1(d1,X)

  d3 = byte2^byte4
  p3 = decrypt_function_2(d3)

  d2 = byte3 ^ byte1
  p2 = decrypt_function_2(d2)

  d4 = circular_right_shift(byte4,2)
  p4 = decrypt_function_1(d4,Y)
  
  result = (p1 << 24) | (p2 << 16) | (p3 << 8) | p4
  return result

def string_to_32bit_list(s):
    s = s.ljust((len(s) + 3) // 4 * 4, '\x00')  # Pad with null characters if needed
    result = []
    
    for i in range(0, len(s), 4):
        group = s[i:i+4]
        value = sum(ord(group[j]) << (8 * (3 - j)) for j in range(4))  # Convert to 32-bit number
        result.append(value)
    
    return result
def list_to_string(lst):
    result = []
    
    for num in lst:
        chars = [(num >> (8 * (3 - i))) & 0xFF for i in range(4)]  # Extract 8-bit segments
        result.extend(chr(c) for c in chars if c != 0)  # Ignore null padding
    
    return ''.join(result)



x = 0.7
r1 = 3.9
size=32 #Number of keys
y = 0.01
r2 = 3.95
Key = logistic_key(x,r1,y,r2,size)


input_string="This is a test string for encryption."
print("Input String = ",input_string)
value = string_to_32bit_list(input_string)
Enc =value
for no_of_rounds in range(5):
    for i in range(len(Enc)):
        X,Y = Key[size-i-1][0],Key[size-i-1][1]
        Enc[i] = encrypt(Enc[i])
    print("Encrypted Text after round ",no_of_rounds+1," : ",list_to_string(Enc))
Encrypted_string = list_to_string(Enc)
print("Encrypted String = ",Encrypted_string)
Dec=Enc
for no_of_rounds in range(5):
    for i in range(len(Dec)):
        X,Y = Key[size-i-1][0],Key[size-i-1][1]
        Dec[i]=decrypt(Dec[i])
    print("Decrypted Text after round ",no_of_rounds+1," : ",list_to_string(Dec))
Decrypted_string=list_to_string(Dec)
print("Decrypted String = ",Decrypted_string)
if(Decrypted_string == input_string):
    print("Decryption Successful..")
else:
    print("Decryption Failed..")
    
  
  
  
  

