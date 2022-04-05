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
* ``RPN`` Reversed Polish Notation, %d is fans count.
* ``type`` Criteria: >=,>,<=,<,= 。
* ``value`` The value the result will compare with. ONLY integers. (RPN type value)
* ``ifTrue`` The signature when it returns true. ``formatted`` formatted text, RPN can be removed when true. ``text`` is your signature, %d is fans count, ``RPN`` is Reversed Polish Notation.
* ``ifFalse`` The signature when it returns false. ``formatted`` formatted text, RPN can be removed when true. ``text`` is your signature, %d is fans count, ``RPN`` is Reversed Polish Notation.
* If ``tw`` is in ``ifFalse``, it will go into a new criteria. Other arguments can be removed.
* *``RPN`` Reversed Polish Notation, %d is fans count.*
* *``type`` Criteria: >=,>,<=,<,= 。*
* *``value`` The value the result will compare with. ONLY integers. (RPN type value)*
* *``ifTrue`` The signature when it returns true. ``formatted`` formatted text, RPN can be removed when true. ``text`` is your signature, %d is fans count, ``RPN`` is Reversed Polish Notation.*
* *``ifFalse`` The signature when it returns false. ``formatted`` formatted text, RPN can be removed when true. ``text`` is your signature, %d is fans count, ``RPN`` is Reversed Polish Notation.*
* *If ``tw`` is in ``ifFalse``, it will go into a new criteria. Other arguments can be removed.*

## 🚗Running

* Run ``pip install -r requirements.txt``.
* Edit ``config.json`` to configure the arguments.
* Enjoy~

## ✔Notice

🍪 How to get cookies: Use your favorite browser to get it.

⭐ If you enjoy the program, you can  ``star`` to support this program!

🐛 If you find any bugs, feel free to create issues or pull requests.
