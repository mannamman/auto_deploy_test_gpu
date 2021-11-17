#!/usr/bin/env python
# coding: utf-8

import torch
from flask import Flask

app = Flask(__name__)

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
    app.run(host="0.0.0.0", port=8090)