import cv2
from PIL import Image

Trans_Window = "transwindow"

trans = Image.new('RGBA', [300, 300], (0, 0, 0, 0))
dst = Image.new('RGB',[300,300],(0,0,0))

font = cv2.FONT_HERSHEY_PLAIN
src = cv2.putText(trans,"Hello",(100,100),font,5,(255,255,0),3)

width, height = src.shape[:2]

mask = src[:,:,3]  # アルファチャンネルだけ抜き出す。
mask = cv2.cvtColor(mask, cv2.cv.CV_GRAY2BGR)  # 3色分に増やす。
mask = mask / 255.0  # 0-255だと使い勝手が悪いので、0.0-1.0に変更。

src = src[:,:,:3]  # アルファチャンネルは取り出しちゃったのでもういらない。

dst[0:height:, 0:width] *= 1 - mask  # 透過率に応じて元の画像を暗くする。
dst[0:height:, 0:width] += src * mask  # 貼り付ける方の画像に透過率をかけて加算。

cv2.namedWindow(Trans_Window)
cv2.imshow(Trans_Window , dst,)

width, height = src.shape[:2]

mask = src[:,:,3]  # アルフxaチャンネルだけ抜き出す。
mask = cv2.cvtColor(mask, cv2.cv.CV_GRAY2BGR)  # 3色分に増やす。
mask = mask / 255.0  # 0-255だと使い勝手が悪いので、0.0-1.0に変更。

src = src[:,:,:3]  # アルファチャンネルは取り出しちゃったのでもういらない。

dst[0:height:, 0:width] *= 1 - mask  # 透過率に応じて元の画像を暗くする。
dst[0:height:, 0:width] += src * mask  # 貼り付ける方の画像に透過率をかけて加算。

cv2.namedWindow(Trans_Window)
cv2.imshow(Trans_Window , dst,)
