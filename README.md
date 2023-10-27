#captchaIdentify

## Group-31 Member: 
Weilong Lin (23359816) 
Rasika Burde (23331395)

## Generate training data

```bash
python generate.py --width 128 --height 64 --symbols symbols_generate.txt --count 160000 --output-dir training_data

```

## Generate validation data

```bash
python generate.py --width 128 --height 64 --symbols symbols_generate.txt --count 16000 --output-dir validation_data

```

## Run training

```bash
nohup python train.py --width 128 --height 64 --length 6 --symbols symbols_train_classfy.txt --batch-size 32 --epochs 5 --output-model-name welin --train-dataset training_data --validate-dataset validation_data  > output.log 2>&1 &

```

## Classify captchas example and transfer tflite model

```bash
python classify.py --model-name welin --captcha-dir images/ --output welin.csv --symbols symbols_train_classfy.txt

```

## Classify on Pi

```bash
python classify_pi.py --model-name classify_model_pi --captcha-dir images-captcha/ --output welin_re_pi.csv --symbols symbols-pi.txt

```