
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

# coding: utf-8


import argparse
from pathlib import Path

import asyncio
from functools import wraps
import omni.client
import time
import numpy as np


# import sys
# import subprocess

# try:
#     import websockets as ws
# except ModuleNotFoundError:
#     subprocess.check_call([sys.executable, "-m", "pip", "install", "websockets"])


g_1 = None 
g_2 = None

g_control_data = {
    'nucleus'           : 'ov-elysium.redshiftltd.com',
    'nucleus_path'      : 'Projects/nat',
    'nucleus_user'      : 'omniverse',
    'nucleus_password'  : 'xxxxxx',
}


# declare constants
DATA_SOURCE_PATH = 'usd-files'

def gdt():
    return(time.time() - g_control_data['start_time'])

def asyncio_wrap(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        asyncio.get_event_loop().run_until_complete(func(*args, **kwargs))
    return wrapper

#
# 
#      
@asyncio_wrap
async def create_folder(fullFolderPath):
    result = await omni.client.create_folder_async(fullFolderPath)
    print(f'[access-test]: create_folder : result: {result.name:<20} {fullFolderPath} ')
    
@asyncio_wrap
async def list_folder(fullFolderPath):
    result = await omni.client.list_async(fullFolderPath)
    for entry in result[1]:
        print(f'[access-test]: list dir : {entry.flags:<5} {entry.relative_path[0:24]:<26} {entry.size:<10} {entry.created_by[0:24]:<25} {entry.modified_by[0:24]:<25} {entry.created_time}')

@asyncio_wrap
async def copy_file(sourcePath, destinationPath):
    result = await omni.client.copy_async(sourcePath,destinationPath,omni.client.CopyBehavior.OVERWRITE, "copy file")
    print(f'[access-test]: copy_file     : result: {result.name:<20} {destinationPath} ')
    
@asyncio_wrap
async def write_file(destinationPath,buffer):
    result = await omni.client.write_file_async(destinationPath,buffer)
    print(f'[access-test]: write file    : result: {result.name:<20} {destinationPath} ')

#
# 
#     
def authentication_callback(url):
    print("[access-test]: Authenticating to {}".format(url)) # is printed once
    return g_control_data["nucleus_user"], g_control_data["nucleus_password"]
   
def connectionStatusCallback(url, connectionStatus):
    print("[access-test]: Connection status to {} is {}".format(url, connectionStatus))
  
def connect_to_nucleus():
    global g_1, g_2

    try:
        if not omni.client.initialize():
            return "Failed to initialize Omni Client"

        print("[access-test]: Omni Client initialized" + omni.client.get_version()) # version 2.17

        g_1 = omni.client.register_authorize_callback(authentication_callback)
        g_2 = omni.client.register_connection_status_callback(connectionStatusCallback)

    except Exception as e:
        print("[access-test]: The error is: ",e)

def startupOmniverse():
    g_control_data['start_time'] = time.time()
    connect_to_nucleus()

def shutdownOmniverse():
    omni.client.sign_out(get_nucleus_url())
    omni.client.shutdown()
  
#
#
def write_nucleus_file():
    omni_base_path = f"omniverse://{g_control_data['nucleus']}/{g_control_data['nucleus_path']}"

    arr1 = np.random.rand(g_control_data["file_size"])

    start_time = time.time()

    write_file(omni_base_path,arr1)
  
    end_time = time.time()
    execution_time = end_time - start_time
    rate = ((g_control_data["file_size"]/execution_time)*8)/1000000

    print(f'Execution time: {execution_time:.1f} seconds for {g_control_data["file_size"]} bytes {rate:.2f} Mb/sec')

    
#
#
def process_directories(root_dir):
    omni_base_path = f"omniverse://{g_control_data['nucleus']}/{g_control_data['nucleus_path']}"

    for path in Path(root_dir).iterdir():
       
        source_path = str(path).replace("\\","/")
        omniverse_full_dir_path = source_path.replace(DATA_SOURCE_PATH, omni_base_path)

        if path.is_dir():  
            create_folder(omniverse_full_dir_path)
            process_directories(path)
        elif path.is_file:
            copy_file(source_path,omniverse_full_dir_path)
    
def write_nucleus_dirs():
    process_directories(DATA_SOURCE_PATH)

def list_nucleus_directory():
    omni_base_path = f"omniverse://{g_control_data['nucleus']}/{g_control_data['nucleus_path']}"
    list_folder(omni_base_path)


def initClient(parser):
    def log_callback(thread, component, level, message):
        print(f"{gdt():.4f}  {thread} {component} {level} {message}")    
        
    args = parser.parse_args()

    g_control_data["nucleus"] = args.nucleus
    g_control_data["nucleus_user"] = args.user_id
    g_control_data["nucleus_path"] = args.nucleus_path
    g_control_data["nucleus_password"] = args.password
    g_control_data["pre_delete_path"] = args.pre_delete_path
    g_control_data["mode"] = args.mode
    g_control_data["file_size"] = 2 ** args.file_size


    if g_control_data["nucleus_user"] == '$omni-api-token':
        with open('api-token.txt') as f:
            g_control_data["nucleus_password"] = f.readline().replace('\n','')
        

    verbose_enabled = args.verbose

    if verbose_enabled:
        omni.client.set_log_level(omni.client.LogLevel.DEBUG)
        omni.client.set_log_callback(log_callback)

def read_nucleus_file():
    omni_base_path = f"omniverse://{g_control_data['nucleus']}/{g_control_data['nucleus_path']}"
    length = -1 

    (ret,_,content) = omni.client.read_file(omni_base_path)
    if ret.name == 'OK':
        length  = len(memoryview(content).tobytes())
       
    print(f'------------')
    print(f'[access-test]: read file : {omni_base_path} {ret.name} {length}')
    print(f'------------')
    print("")

def get_nucleus_url():
    return f"omniverse://{g_control_data['nucleus']}"
    
def pre_delete_path():
    omni_base_path = f"omniverse://{g_control_data['nucleus']}/{g_control_data['nucleus_path']}"

    result, data = omni.client.list(omni_base_path)
    for i in data:
        destinationPath = omni_base_path + '/' + i.relative_path
        result = omni.client.delete(destinationPath)
        print(f'[access-test]: delete_obj    : result: {result.name:<20} {destinationPath} ')




# #for later  asyncio.run(xxx())
# import json
# async def xxx():
#     async with ws.connect("wss://ov-elysium.redshiftltd.net/omni/discovery") as websocket:
#         message = {"type": "get", "resource": ""}
#         await websocket.send(json.dumps(message))
#         response = await websocket.recv()
#         print(response)


        




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python Client to copy data from a local file system to Nucleus Server",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('nucleus',      type=str,help="example: ov-elysium.redshiftltd.com")
    parser.add_argument('nucleus_path', type=str,help="Projects/SomeFolder (no leading '/')")

    parser.add_argument("-u", "--user_id",  action='store', default="omniverse")
    parser.add_argument("-p", "--password", action='store', default="xxxxxx")
    parser.add_argument("-v", "--verbose",  action="store_true", default=False, help='debug log data' )
    parser.add_argument("-d", "--pre_delete_path",  action="store_true", default=False )

    parser.add_argument("-M", "--mode",  type=int, default=0, help='Tool method' )
    parser.add_argument("-s", "--file_size",  type=int, default=4, help='File size = 2^N' )

    initClient(parser)
    
    startupOmniverse()

    if g_control_data['mode'] == 1:
        if g_control_data["pre_delete_path"]:
            pre_delete_path()
        write_nucleus_dirs()

    if g_control_data['mode'] == 2:
        read_nucleus_file() 

    if g_control_data['mode'] == 3:
        list_nucleus_directory() 

    if g_control_data['mode'] == 4:
        write_nucleus_file() 

    shutdownOmniverse()
    

