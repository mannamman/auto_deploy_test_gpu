import matplotlib.pyplot as plt
import cv2
from colorizers import *
import numpy as np
import traceback
import json
import io
import torch
import requests
from PIL import Image
from flask import Flask, request
import requests
import torch

app = Flask(__name__)

# 에러 보기좋게 변환
def pretty_trackback(msg :str)->str:
    """
    에러 발생시 문구를 보기 편하게 변환하는 함수
    파라미터
        msg : traceback 모듈을 이용해 전달받은 에러 메시지
    반환 값
        변환된 에러 메시지
    """
    msg = msg.split("\n")
    msg = msg[1:-1]
    msg = [i.strip() for i in msg]
    msg = " ".join(msg)
    return msg

def load_model(style):
    model = None
    if(style == "eccv"):
        model = eccv16(pretrained=True).eval()
    elif(style == "siggraph"):
        model = siggraph17(pretrained=True).eval()
    model.cuda()
    return model


def load_img(pil_img):
    out_np = np.asarray(pil_img)
    if(out_np.ndim==2):
        out_np = np.tile(out_np[:,:,None],3)
    return out_np


def convert_cv2(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.convertScaleAbs(img, alpha=(255.0))
    return img


def prediction(img, model):
    # default size to process images is 256x256
    # grab L channel in both original ("orig") and resized ("rs") resolutions
    (tens_l_orig, tens_l_rs) = preprocess_img(img, HW=(256,256))
    tens_l_rs = tens_l_rs.cuda()

    # colorizer outputs 256x256 ab map
    # resize and concatenate to original L channel
    result = postprocess_tens(tens_l_orig, model(tens_l_rs).cpu())
    return result


@app.route('/', methods=["POST"])
def index():
    try:
        ## 메시지 파싱 ##
        recevied_msg = json.loads(request.get_data().decode("utf-8"))
        img_url = recevied_msg["input_url"]
        # eccv, siggraph
        style = recevied_msg["style"]
        header = recevied_msg["header"]
        upload_url = recevied_msg["upload_url"]

        # 모델 로드
        model = load_model(style)
        # url로 이미지 요청
        res = requests.get(img_url)

        ## 이미지 읽기 ##
        data = io.BytesIO(res.content)
        pil_img = Image.open(data)
        img = load_img(pil_img)

        # 예측
        pred = prediction(img, model)
        # cv2로 출력가능하게 변환
        pred = convert_cv2(pred)
        ## 처리 후 전송 ##
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, encimg = cv2.imencode('.jpg', pred, encode_param)
        img_bytes = io.BytesIO(encimg)
        res = requests.put(upload_url, data=img_bytes, headers=header)
        return(res.content.decode("utf-8"), res.status_code)
    except Exception:
        error = traceback.format_exc()
        error = pretty_trackback(error)
        return({"error":error},400)
    

@app.route('/', methods=["GET"])
def index():
    avaliable = torch.cuda.is_available()
    if avaliable:
        d_name = ""
        d_count = torch.cuda.device_count()
        for d in range(d_count):
            d_name += f"{torch.cuda.get_device_name(d)}, "
        return_string = f"available : {avaliable}, d_name : {d_name}d_count : {d_count}"
    else:
        return_string = f"available : {avaliable}"
    return(return_string, 200)

if(__name__=='__main__'):
    app.run(host="0.0.0.0", port=80)