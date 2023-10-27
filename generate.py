#!/usr/bin/env python3
import base64
import os
import numpy
import random
import string
import cv2
import argparse
import captcha.image
import tensorflow as tf
import scipy


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', help='Width of captcha image', type=int)
    parser.add_argument('--height', help='Height of captcha image', type=int)
    # parser.add_argument('--length', help='Length of captchas in characters', type=int)
    parser.add_argument('--count', help='How many captchas to generate', type=int)
    parser.add_argument('--output-dir', help='Where to store the generated captchas', type=str)
    parser.add_argument('--symbols', help='File with the symbols to use in captchas', type=str)
    args = parser.parse_args()

    if args.width is None:
        print("Please specify the captcha image width")
        exit(1)

    if args.height is None:
        print("Please specify the captcha image height")
        exit(1)

    # if args.length is None:
    #     print("Please specify the captcha length")
    #     exit(1)

    if args.count is None:
        print("Please specify the captcha count to generate")
        exit(1)

    if args.output_dir is None:
        print("Please specify the captcha output directory")
        exit(1)

    if args.symbols is None:
        print("Please specify the captcha symbols file")
        exit(1)

    font_path = 'clouds-smile-too.regular.ttf'
    # font_path = 'eamonexpbold.woff.ttf'
    # create ImageCaptcha
    captcha_generator = captcha.image.ImageCaptcha(fonts=[font_path], width=args.width, height=args.height)

    symbols_file = open(args.symbols, 'r')
    captcha_symbols = symbols_file.readline().strip()
    symbols_file.close()

    print("Generating captchas with symbol set {" + captcha_symbols + "}")

    if not os.path.exists(args.output_dir):
        print("Creating output directory " + args.output_dir)
        os.makedirs(args.output_dir)

    with tf.device('/device:GPU:0'):
        for i in range(args.count):
            random_length = random.randint(1, 6)
            random_str = ''.join([random.choice(captcha_symbols) for j in range(random_length)])
            image_path = os.path.join(args.output_dir, complete_captcha_name(random_length, random_str, "", 0))
            if os.path.exists(image_path):
                version = 1
                while os.path.exists(
                        os.path.join(args.output_dir, complete_captcha_name(random_length, random_str, version, 1))):
                    version += 1
                image_path = os.path.join(args.output_dir, complete_captcha_name(random_length, random_str, version, 1))

            image = numpy.array(captcha_generator.generate_image(random_str))
            cv2.imwrite(image_path, image)


def complete_captcha_name(captcha_length, random_captcha, version, path_exist):
    remain_length = 6 - captcha_length
    remain_str = ''.join("¥" for i in range(remain_length))
    if path_exist:
        str_tmp = random_captcha + remain_str
        str_encoded = base64.urlsafe_b64encode(str_tmp.encode()).decode()
        return str_encoded + '.png'
    else:
        str_tmp = random_captcha + remain_str + '_' + str(version)
        str_encoded = base64.urlsafe_b64encode(str_tmp.encode()).decode()
        return str_encoded + '.png'

def preprocess_cleaner_image(img):
    # # Invert color
    # img = numpy.subtract(255, numpy.uint8(img))
    # # Remove background color
    # # TODO(clean): scipi seems unnecessary here
    # bg = scipy.stats.mode(img[[0,0,-1,-1],[0,-1,0,-1]])[0][0]
    # img = numpy.subtract(img.astype(numpy.int16), bg)
    # img = img.clip(0, 255).astype(numpy.uint8)
    # # Convert to grayscale
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # to grayscale
    img = numpy.reshape(img, (img.shape[0], img.shape[1], 1))
    # Convert to float32 in [0, 1] range
    img = numpy.array(img, dtype=numpy.float32) / 255.0
    # Resize to the desired size
    img = cv2.resize(img, (128, 64), interpolation=cv2.INTER_LINEAR)
    return img

if __name__ == '__main__':
    main()






