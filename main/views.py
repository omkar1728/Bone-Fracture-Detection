import numpy as np
import pydicom as dicom
import matplotlib.pyplot as plt
from django.templatetags.static import static
from keras.models import load_model
import os
from .models import CT
from django.contrib import messages
from django.shortcuts import render

# Create your views here.


def mainHome(request):
    if request.method == "POST":
        image_list = request.FILES.getlist("images")
        for i in image_list:
            print(i)
        print(image_list)
        # radiogram = request.FILES['radiogram']
        # entry = patient_radiogram(radiogram = radiogram)
        # entry.save()
        messages.success(request, "radiogram uploaded successfully")
    return render(request, "upload.html")


def main_upload(request):
    if request.method == "POST":
        image_list = request.FILES.getlist("images")
        print(image_list)
        for i in image_list:
            print(i)
            entry = CT(image=i)
            entry.save()

        messages.success(request, "The dicom scans were successfully uploaded.")
    return render(request, "upload-b.html")


def services(request):
    return render(request, "Services.html")


def Home(request):
    return render(request, "home.html")


def aboutus(request):
    return render(request, "About.html")


def predict(request):
    # images = CT.objects.all()
    # saggital_view = []
    # for i in range(len(images)):
    #     image = images[i]
    #     image = image.image
    #     print(image)
    #     image = dicom.dcmread(image)
    #     image = image.pixel_array
    #     # image = image/255 #optional normalization step
    #     saggital_view.append(image)
    # saggital_view = np.array(saggital_view)
    # saggital_view = saggital_view[:, :, 256]
    # number_of_images = len(images)
    # trim_np = np.zeros([512, 512])  # creating blank array of only zeros
    # if number_of_images >= 512:
    #     trim_np = saggital_view[:512]
    # else:
    #     for i in range(number_of_images):
    #         trim_np[i + (512 - number_of_images) // 2] = saggital_view[i]

    # # plt.imshow(trim_np, cmap='bone')
    # # plt.savefig(os.path.join('static', 'imshow.png'))
    # plt.imsave(os.path.join("static", "imsave.png"), trim_np, cmap="bone")
    # # img = Image.fromarray(trim_np)
    # # img.save(os.path.join('static', 'PIL.png'))
    # model_path = os.path.join("static", "epoch85.h5")
    # # model = static(model_path)
    # model = load_model(model_path)

    # print(trim_np.shape)
    # trim_np = [trim_np]
    # trim_np = np.array(trim_np)
    # print(trim_np.shape)

    # predictions = model.predict(trim_np)
    # print(predictions)

    # context = {}
    # if predictions[0][0] == 1:
    #     context["predicted"] = False
    # else:
    #     context["predicted"] = True

    # print("deleting uploaded images....")
    # for i in images:
    #     # print('deleted ', i)
    #     i.delete()
    # print("uploaded images deleted.")

    context = {}
    model_path = os.path.join("static", "epoch200.h5")
    # model = static(model_path)
    model = load_model(model_path)

    images = CT.objects.all()
    image = images[0]
    image = image.image
    print(image)
    image = dicom.dcmread(image)
    image = image.pixel_array

    def reshape(arr_512):
        arr_64 = np.zeros((64, 64))
        for i in range(64):
            for j in range(64):
                arr_64[i, j] = np.mean(arr_512[i * 8 : i * 8 + 8, j * 8 : j * 8 + 8])
        return arr_64

    image = reshape(image)
    image = image / 255.0
    image = image.reshape((64, 64, 1))
    image = [image]
    image = np.array(image)
    p = model.predict(image)
    if (np.max(p)) > 0.99:
        context["predicted"] = True
        print("yes")
    else:
        context["predicted"] = False
        print("No")

    print("deleting uploaded images....")
    for i in images:
        # print('deleted ', i)
        i.delete()
    print("uploaded images deleted.")

    return render(request, "prediction-ui.html", context=context)
