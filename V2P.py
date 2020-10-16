# coding: utf-8

"""
Created on:
@brief:图集与视频的相互转化
@author: YangLei
@version: Python3
"""
import os
import cv2
from PIL import Image

def P2V(sp,fps,img_path):
    """
    图集转换成视频
    :param sp:生成视频的储存路径
    :param fps: 帧率，1秒钟有n张图片写进去[控制一张图片停留5秒钟，那就是帧率为1，重复播放这张图片5次]；如果文件夹下有50张 534*300的图片，这里设置1秒钟播放5张，那么这个视频的时长就是10秒
    :param img_path: 图集地址
    :return:
    """
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    images = os.listdir(img_path)
    im = Image.open(img_path + '/' + images[0]) #这里以第一张图片的尺寸为视频的尺寸
    VideoWriter = cv2.VideoWriter(sp, fourcc, fps, im.size)

    #进入到图集路径下
    os.chdir(img_path)
    for item in os.listdir():
        img = cv2.imread(str(item))  # 使用opencv读取图像，直接返回numpy.ndarray 对象，通道顺序为BGR ，注意是BGR，通道值默认范围0-255。
        img = cv2.resize(img, im.size)  # 重新设置尺寸，这里视频的尺寸要和图片的尺寸一致
        VideoWriter.write(img)
    VideoWriter.release()
    print(sp, 'Synthetic success!')


def V2P(sp,img_path):
    """
    视频转换成图集
    :param sp: 视频路径
    :param img_path: 生成图片存储文件夹路径
    :return:
    """
    cap = cv2.VideoCapture(sp) #参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
    suc = cap.isOpened()  # 是否成功打开
    frame_count = 0
    while suc:
        frame_count += 1
        suc, frame = cap.read()  # 按帧读取视频,suc是布尔值，如果读取帧是正确的则返回True，如果文件读取到结尾，它的返回值就为False;frame就是每一帧的图像，是个三维矩阵。
        if frame is not None:
            cv2.imwrite(f'{img_path}/{frame_count}.png',frame, [3]) #第一个参数是要保存的文件名，第二个参数是要保存的图像。可选的第三个参数，它针对特定的格式：对于JPEG，其表示的是图像的质量，用0 - 100的整数表示，默认95;对于png ,第三个参数表示的是压缩级别，默认为3。
    cap.release()
    print('unlock image: ', frame_count-1)


if __name__ == '__main__':
    sp = 'a.avi'
    img_path='mv'
    V2P(sp,img_path)
