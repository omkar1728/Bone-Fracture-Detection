import pydicom as dicom
import media.images 

import matplotlib.pyplot as plt

path = "/../media/images/540.dcm"

x = dicom.dcmread(path)

plt.imshow(x.pixel_array, cmap="bone")
plt.show()