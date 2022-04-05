# 哔哩哔哩自动更改个人简介

![GitHub stars](https://img.shields.io/github/stars/ThebestkillerTBK/bili-signature?style=flat)![GitHub stars](https://img.shields.io/github/forks/ThebestkillerTBK/bili-signature?style=flat)

[English](README.md) | 中文

[wuziqian211/bili-auto-change-sign](https://github.com/wuziqian211/bili-auto-change-sign)的Python版。

## ❓介绍

本程序可以根据自己的哔哩哔哩账号的粉丝数, 自动更改您的个人简介。

## 🚀使用方法

运行 ``python bili-signature.py``

## ⚙配置

``SESSDATA`` 你的 SESSDATA.

``bili_jct`` 你的 bili_jct.

``freq`` 更新频率(秒).

``signature`` 你的个人简介, %d是粉丝数.

``advanced`` 用来判断条件.

* ``enabled`` 是否高级模式.
* ``RPN`` 逆波兰表达式.
* ``type`` 当结果>=,>,<=,<,=比较的值时，根据条件更改简介.
* ``value`` 与结果比较的值. 只支持整数. (RPN type value)
* ``ifTrue`` 返回真时的简介.
* ``ifFalse`` 返回假时的简介.
* 以上两个``text``是简介, %d是粉丝数, ``RPN`` 是逆波兰表达式.

## 🚗运行

* 运行 ``pip install -r requirements.txt``.
* 编辑 ``config.json`` 来配置参数.
* 享受吧~

## ✔注意事项

🍪 如何获取cookies: 打开你的浏览器获取(这不用说谁都知道吧).

⭐ 如果喜欢的话请帮忙`star`支持一下！

🐛 有Bug可以开Issue或PR
