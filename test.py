import requests
import shutil
from PIL import ImageGrab, ImageFile
from io import BytesIO
from PIL import Image
import win32clipboard

ImageFile.LOAD_TRUNCATED_IMAGES = True
    

def imageToClipboard(img_path='img.png'):
    image = Image.open(img_path)
    output = BytesIO()
    image.convert('RGB').save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()


def imgUrlToFile(src):
    response = requests.get(src, stream=True)
    with open('img.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response



imgUrlToFile('https://avatars.mds.yandex.net/i?id=92bd132c3ef221c7c2222472d3e6a8d0-4473749-images-thumbs&n=13')
imageToClipboard()



