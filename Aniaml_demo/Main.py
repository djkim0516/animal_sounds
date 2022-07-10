import os
from ISPL_DEMO import Animal_log
os.environ["CUDA_VISIBLE_DEVICES"]='0'

audio_path='./Frogdemo.m4a'
check_point='./CKT_DEMO_mask'
outputs=Animal_log(audio_path,check_point,thread_unknown=0.9,thread_class=0.9)



