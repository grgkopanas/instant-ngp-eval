from PIL import Image
import PIL.ImageOps    
import os
from joblib import delayed, Parallel
import argparse
import glob

def split_mask(folder_in, folder_out, img_path):
    rgba_image = Image.open(os.path.join(folder_in, img_path))

    # Separate the RGB and A channels
    rgb_image = rgba_image.convert("RGB")
    alpha_channel = PIL.ImageOps.invert(rgba_image.getchannel("A"))

    os.makedirs(os.path.dirname(os.path.join(folder_out, img_path)), exist_ok=True)

    # Save RGB image
    rgb_image_path = os.path.join(folder_out, os.path.join(folder_out, img_path.split(".")[0] + ".png"))
    rgb_image.save(rgb_image_path)

    # Save A channel as a grayscale image
    alpha_channel_path = os.path.join(folder_out, os.path.join(folder_out, 
                                      os.path.dirname(img_path), 
                                      "dynamic_mask_" + os.path.basename(img_path).split(".")[0] + ".png"))
    alpha_channel.save(alpha_channel_path)

parser = argparse.ArgumentParser()

parser.add_argument('--images_path', required=True)

args = parser.parse_args()

FOLDER_IN = args.images_path
FOLDER_OUT = FOLDER_IN + "_ingp"

paths = glob.glob(os.path.join(FOLDER_IN, '*\*'))
paths = [p.split("images\\")[-1] for p in paths]

#for img_name in paths:
#    split_mask(FOLDER_IN, FOLDER_OUT, img_name)
Parallel(n_jobs=-1, backend="threading")(delayed(split_mask)(FOLDER_IN, FOLDER_OUT, img_path) for img_path in paths) 