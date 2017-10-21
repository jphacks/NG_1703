#!/usr/bin/env python
# vim:fileencoding=utf-8

import time
import numpy as np
import pyaudio as pa
import requests
import sys
import json
import string, random
import cv2

# set Device ID to variable "id".
# Device ID: You can get the id from portal
# https://www6.arche.blue/portal/
#id = "device id string"
id = "c59ea1212a11cf"

# global 
# edge_id get by register_client_sdk
apiurl = "https://www6.arche.blue/api/v1/"
edge_id = ""
edge_port = 80
edge_ip_addr = ""
session_id = ""

# cv2.cv.CV_FOURCC
def cv_fourcc(c1, c2, c3, c4):
    return (ord(c1) & 255) + ((ord(c2) & 255) << 8) + \
        ((ord(c3) & 255) << 16) + ((ord(c4) & 255) << 24)

        #字幕生成
def make_subtitle(c_frame,text,place_x,place_y,size):
        font = cv2.FONT_HERSHEY_PLAIN
        g_frame = cv2.putText(c_frame,text,(place_x,place_y),font, size,(255,255,0),3)

        return (g_frame)

# Generate random string. It is used in session create to cloud edge.
def random_string(length, seq=string.digits + string.ascii_lowercase):
    sr = random.SystemRandom()
    return ''.join([sr.choice(seq) for i in range(length)])
rnd = "?"+random_string(4)


# This program does not run without setting id variable.
# If not set, program stop.
if(id is None):
    print("Error. Set Device ID to variable \"id\" in this source code by text editors.")
    sys.exit()


# This callback is called from pyaudio periodically.
# chunk is a piece of sound.
def callback(in_data, frame_count, time_info, status):
    global chunk
    global w_flag

    in_data = np.frombuffer(in_data, dtype=np.int16)    
    chunk = in_data.tobytes()
    w_flag = True

    return (in_data, pa.paContinue)



# Call Management Server API "Create Edge"
# POST https://www6.arche.blue/api/v1/<device_id>/edge
# It returns an existing cloud edge id or (if not exist) create a new cloud edge.
# This API returns device ID(it is same device_id) and edge ID with json form.
def create_edge():
    global edge_id
    
    request_url = apiurl + id + "/edge"
    try:
        r = requests.post(request_url) 
#        r = requests.post(request_url, proxies=proxies) 
    except:
        print ("Error! Fail to connect edge server.")
        sys.exit()
    if (r.status_code > 299):
        print ("Error! Fail to request management server. Check client id. status="+str(r.status_code))
        sys.exit()
    
#    print("Booting Edge Server.")
    
    edge_id = r.json()["edge_id"]
#    print("edge id:" +edge_id)
    return r.json() 



# Call Management Server API "Get Edge Info"
# GET https://www6.arche.blue/api/v1/<device_id>/edge/<edge_id>
#
# This API return Edge Status and Information with json form,
# {
#  "ready":true/false,   // true -> connectable
#  "error":true/false,   // true -> error. Reboot client and generate another VM.
#  "description":"...",   // readable status
#  "ip_address":"xx.xx.xx.xx"  // it is returned when ready = true
# }
# The API should be called periodically until 'ready' becomes true
def get_edge_info():
    global edge_ip_addr
    
    if(edge_id == ""):
        print ("Error! Edge ID Lost.")
        sys.exit()
    
    request_url = apiurl + id + "/edge/" + edge_id
    try:
        r = requests.get(request_url)
#        r = requests.get(request_url, proxies=proxies)
    except:
        print ("Error! Fail to connect edge server.")
        sys.exit()
    if (r.status_code > 299):
        print ("Error! Fail to connect management server."+str(r.status_code))
        sys.exit()

    data = r.json()
    if(data["error"]):
        print ("Error! Fail to start edge server.")
        sys.exit()
    
    if(data["ready"]):
        edge_ip_addr = data["ip_address"]
 #       print ("Edge Server Ready.")
    
    return(data)


# Call Edge API "Connect to edge server"
# Get http://edge_ipaddress/sounddetect/v1/<device_id>/edge/<edge_id>
# It returns "session id" with json form.
def connect_edge_server():
    global session_id
    if( edge_ip_addr == ""):
        print("Error, IP address of Edge Server unknown.")
        sys.exit()
    
    if(edge_id  == ""):
        print("Error, Edge Server ID unknown.")
        sys.exit()

    bufsize = 4096

#    print("Connect to Edge Server.")

    request_url = "http://" + edge_ip_addr +"/sounddetect/v1/" + id + "/edge/" + edge_id + rnd
    try:
        r = requests.get(request_url)
#        r = requests.get(request_url, proxies=proxies)
    except:
        print ("Error! Fail to connect edge server.")
        sys.exit()
    if(r.status_code > 299):
        print ("Error! Edge server replied error code:"+str(r.status_code))
        sys.exit()

    data = r.json()
    session_id = data["session"]
#    print("Connected Successfully. Session ID:"+session_id)

    return session_id


# Call Edge API "Send Sound chunk data to edge server"
# POST http://edge_ipaddress/sounddetect/v1/<device_id>/edge/<edge_id>/session/<session_id>
def send_chunk_edge_server(chunk):
    retry = 3

    request_url = "http://" + edge_ip_addr +"/sounddetect/v1/" + id + "/edge/" + edge_id + "/session/" + session_id

    session = requests.Session()
    session.mount("http://", requests.adapters.HTTPAdapter(max_retries=retry))
    session.mount("https://", requests.adapters.HTTPAdapter(max_retries=retry))

    try:
        r = requests.post(request_url, data=chunk, timeout=(10.0, 30.0))
#        r = requests.post(request_url, data=chunk, timeout=(10.0, 30.0), proxies=proxies)
    except:
        print ("Error! Fail to connect edge server.")
        sys.exit()
    if(r.status_code > 299):
        print ("Error! Edge server replied error code:"+str(r.status_code))
        sys.exit()
#    print("Send data successfully")
    return True


# Call Edge API "Last Event"
# GET http://edge_ipaddress/v1/<device_id>/event
# @return array("event":{eventtype},"unixtime":{eventtime})
def get_last_event():

    request_url = apiurl + id + "/event"

    session = requests.Session()

    try:
        r = requests.get(request_url)
#        r = requests.get(request_url, proxies=proxies)
    except:
        print ("Error! Fail to connect management server.")
        #sys.exit()
        return None;
    if(r.status_code > 299):
        print ("Error! Management server replied error code:"+str(r.status_code))
        #sys.exit()
        return None;

    if(len(r.content) == 0):
        return None
    data = r.json()
    if(len(data) >0):
        return r.json()[0]
    else:
        return None


# start setting up sound recording and sending sounds to the edge server.
def start_sound_detect():
    connect_edge_server()

    # pyaudio
    p_in = pa.PyAudio()
    bytes = 2
    py_format = p_in.get_format_from_width(bytes)
    fs = 0
    channels = 1
    use_device_index = -1
    
    # find input device
    for i in range(p_in.get_device_count()):
        maxInputChannels = p_in.get_device_info_by_index(i)['maxInputChannels']
        if maxInputChannels > 0:
            if use_device_index == -1:
                use_device_index = i
                fs = int(p_in.get_device_info_by_index(i)['defaultSampleRate'])
    chank_size = fs * 1

#    print('use_device_index = ', use_device_index)
#    print('SampleRate = ', fs)

    # generate an input stream
    in_stream = p_in.open(format=py_format,
                          channels=channels,
                          rate=fs,
                          input=True,
                          frames_per_buffer=chank_size,
                          input_device_index=use_device_index,
                          stream_callback=callback)

    in_stream.start_stream()
    return in_stream

if __name__ == "__main__":
    global w_flag
    global chunk

    ESC_KEY = 27     # Escキー
    INTERVAL= 33     # 待ち時間
    FRAME_RATE = 5  # fps

    ORG_WINDOW_NAME = "org"
    GAUSSIAN_WINDOW_NAME = "gaussian"

#    GAUSSIAN_FILE_NAME = "gaussian.avi"

    DEVICE_ID = 0

    # カメラ映像取得
    cap = cv2.VideoCapture(DEVICE_ID)

    # 保存ビデオファイルの準備
    end_flag, c_frame = cap.read()
#    height, width, channels = c_frame.shape
#    rec = cv2.VideoWriter(GAUSSIAN_FILE_NAME, \
#                          cv_fourcc('X', 'V', 'I', 'D'), \
#                          FRAME_RATE, \
#                          (width, height), \
#                          True)
    # ウィンドウの準備
 #   cv2.namedWindow(ORG_WINDOW_NAME)
    cv2.namedWindow(GAUSSIAN_WINDOW_NAME)


    komagen_flag = True   

    create_edge()

#    print("Now creating your Cloud Edge. Please wait for approx 60 sec ..")
    
    edgeinfo = get_edge_info()
#    sys.stderr.write("Progress %3s%%" % (edgeinfo["progress"]))
    pre_progress = int(edgeinfo["progress"])
    progress = int(edgeinfo["progress"])
    while ((edgeinfo["ready"] == False) and (edgeinfo["error"] == False)):
        time.sleep(3)
        edgeinfo = get_edge_info()
        new_progress = int(edgeinfo["progress"])
        if(pre_progress == new_progress):
            progress += 1
        else:
            progress = int(new_progress)
            pre_progress = progress
        
#        sys.stderr.write("\rProgress %3s%%" % (progress))
    sys.stderr.write("\n")

    if(edgeinfo["error"]):
        print("Fail to create your Cloud Edge.")
        sys.exit()

#    print("Edge Server IP address:", edge_ip_addr)

    w_flag = False

    old_event = get_last_event()

    in_stream = start_sound_detect()

    while (in_stream.is_active() or (end_flag == True)):
        text = "test"
#as client
        if w_flag:
            w_flag = Fals
            if komagen_flag == True:
                print("check start")
                komagen_flag = False
            send_chunk_edge_server(chunk)
            
            e_flag = False
            new_event = get_last_event()
            if(new_event != None):
                if(old_event == None):
                    old_event= new_event 
                    e_flag = True
                elif(old_event['unixtime'] != new_event['unixtime']):
                    old_event= new_event 
                    e_flag = True
             if(e_flag):
#                    print(""+new_event['event'])
                 text = new_event['event']
        #字幕生成
        g_frame = make_subtitle(c_frame,text,200,200,3)
        # フレーム書き込み
#        rec.write(g_frame)
        # フレーム表示
        cv2.imshow(GAUSSIAN_WINDOW_NAME, g_frame)

        # Escキーで終了
#        key = cv2.waitKey(INTERVAL)
#        if key == ESC_KEY:
#            break

        # 次のフレーム読み込み
         end_flag, c_frame = cap.read()
    else:
        in_stream.stop_stream()
        in_stream.close()
    # 終了処理
    cv2.destroyAllWindows()
