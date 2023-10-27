#!/usr/bin/env python3
import csv
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
import cv2
import numpy
import string
import random
import argparse
import tensorflow as tf
from tensorflow import keras
import tflite_runtime.interpreter as tflite


def decode(characters, y):
    y = numpy.argmax(numpy.array(y), axis=2)[:,0]
    result = ''.join([characters[x] for x in y])
    return result.replace(' ', '')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-name', help='Model name to use for classification', type=str)
    parser.add_argument('--captcha-dir', help='Where to read the captchas to break', type=str)
    parser.add_argument('--output', help='File where the classifications should be saved', type=str)
    parser.add_argument('--symbols', help='File with the symbols to use in captchas', type=str)
    args = parser.parse_args()

    if args.model_name is None:
        print("Please specify the CNN model to use")
        exit(1)

    if args.captcha_dir is None:
        print("Please specify the directory with captchas to break")
        exit(1)

    if args.output is None:
        print("Please specify the path to the output file")
        exit(1)

    if args.symbols is None:
        print("Please specify the captcha symbols file")
        exit(1)

    symbols_file = open(args.symbols, 'r')
    captcha_symbols = symbols_file.readline().strip('\n')
    symbols_file.close()

    print("Classifying captchas with symbol set {" + captcha_symbols + "}")

    with tf.device('/cpu:0'):
        with open(args.output, 'w') as output_file:
            interpreter = tflite.Interpreter(model_path=args.model_name + '.tflite')
            interpreter.allocate_tensors()
            index = interpreter.get_input_details()[0]['index']
            output_details = interpreter.get_output_details()

            username = "welin"
            output_file.write(f"{username}\n")
            for x in sorted(os.listdir(args.captcha_dir)):
                # load image and preprocess it
                raw_data = cv2.imread(os.path.join(args.captcha_dir, x))
                rgb_data = cv2.cvtColor(raw_data, cv2.COLOR_BGR2RGB)
                img = numpy.array(rgb_data, numpy.float32) / 255.0
                img = img.reshape((-1, *img.shape))
                interpreter.set_tensor(index, img)
                interpreter.invoke()
                predictions = [interpreter.get_tensor(out['index'])
                               for out in output_details]
                output_file.write(x + "," + decode(captcha_symbols, predictions).replace("¥", "").lower().strip() + "\n")

                print('Classified ' + x)


if __name__ == '__main__':
    main()
