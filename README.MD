# Bilibili signature auto change

![GitHub stars](https://img.shields.io/github/stars/ThebestkillerTBK/bili-signature?style=flat)![GitHub stars](https://img.shields.io/github/forks/ThebestkillerTBK/bili-signature?style=flat)

English | [中文](README-zh.md)

A Python port for [wuziqian211/bili-auto-change-sign](https://github.com/wuziqian211/bili-auto-change-sign)

## ❓Introduction

This program changes your Bilibili signature depending on your account fans data.

## 🚀Usage

Run ``python bili-signature.py``

## ⚙Configuration

``SESSDATA`` Your SESSDATA.

``bili_jct`` Your bili_jct.

``freq`` Update frequency (In seconds). Too low may trigger the anti-bot system.

``signature`` Your personal signature. %d is the fans count.

``advanced`` Conditional mode.

* ``enabled`` Whether Advanced mode is enabled.
* ``RPN`` Reversed Polish Notation.
* ``type`` Change signature based on condition when result >=,>,<=,<,= compared value。
* ``value`` The value the result will compare with. ONLY integers. (RPN type value)
* ``ifTrue`` The signature when it returns true.
* ``ifFalse`` The signature when it returns false.
* The two keys above, ``text``is your signature, %d is fans number, ``RPN`` is Reversed Polish Notation.

## 🚗Running

* Run ``pip install -r requirements.txt``.
* Edit ``config.json`` to configure the arguments.
* Enjoy~

## ✔Notice

🍪 How to get cookies: Use your favorite browser to get it.

⭐ If you enjoy the program, you can  ``star`` to support this program!

🐛 If you find any bugs, feel free to create issues or pull requests.
