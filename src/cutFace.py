import cv2#需提前在你的python环境下安装opencv包
import sys
import os.path
import shutil
from glob import glob

def detect(savepath,filename, cascade_file="../tools/lbpcascade_animeface.xml"):
    if not os.path.isfile(cascade_file):#lbpcascade_animeface.xml文件可在github上面找到，就是一个巨长的xml格式代码，表示看不懂。
        raise RuntimeError("%s: not found" % cascade_file)

    cascade = cv2.CascadeClassifier(cascade_file)
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    faces = cascade.detectMultiScale(gray,
                                     # detector options
                                     scaleFactor=1.1,
                                     minNeighbors=5,
                                     minSize=(48, 48))
    for i, (x, y, w, h) in enumerate(faces):
        face = image[y: y + h, x:x + w, :]
        face = cv2.resize(face, (96, 96))
        save_filename = '%s-%d.jpg' % (os.path.basename(filename).split('.')[0], i)
        #print("processing "+save_filename)
        cv2.imwrite(savepath + save_filename, face)#写入文件
        print("finished!")

def cut():
    savedir='../imgs/faces/'
    rowdir='../imgs/animes/'
    if os.path.exists(savedir):
        shutil.rmtree(savedir)
    os.makedirs(savedir)
    file_list = glob(rowdir+'*.jpg')
    for filename in file_list:
        print(filename)
        detect(savedir,filename)
    print('All finished.')


cut()