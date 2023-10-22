from PIL import Image
import numpy as np
# Load the image
image = Image.open('Fracture.png').convert('L')
# Convert the image to a NumPy array
image_array = np.array(image)
print(image_array)
a=image_array.shape
print(a)
c=10e-100
b = np.exp(image_array)
b =np.where(b > 255, 255, b)
print(b)
image1 = Image.fromarray(b.astype(int))
image1.show()
