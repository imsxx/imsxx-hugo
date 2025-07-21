---
title: iPhoneX刷机失败变砖如何进入dfu模式恢复和强制刷入新系统？
author: 梦随乡兮
date: 2019-06-05 18:48:27+00:00
slug: iphonex-dfu
tags:
- iphonex
- dfu
---
接上一篇文章，<a href="https://imsxx.com/itunes-ios.html" target="_blank" rel="noopener noreferrer">win10下iTunes恢复iOS版本提示“磁盘已满”的解决办法</a>。
iOS13降级到iOS12并不容易，通过iTunes恢复后开机出现白苹果并自动关机。原以为是数据有个熄屏的恢复过程，结果等了半个小时都没好。于是猜想可能是iOS13和iOS12的文件结构不同导致降级恢复出现问题。
那么解决办法就很简单了，首先我们在这种开不了机的情况下需要进入dfu模式，以iPhoneX为例，首先链接到电脑并打开爱思助手，按一下音量+松开，按一下音量-松开，按下电源键，一直等到手机出现连接iTunes的界面松开即可。
这里用爱思助手的理由是，它比苹果自家的iTunes好用多了，还有其他的助手软件可以用，这里不多介绍了。
然后下载与你备份的iOS版本一样的固件版本，下载完成后进入一键刷固件就好了，全程傻瓜式等待它完成。拔掉数据线。
全新的固件刷入后就像是一个新手机，开机会有引导做基础的手机设置。不管它。
插入数据线连接电脑，打开iTunes我们就能看到提示我们将手机恢复到之前我们做过的备份(如果你在用爱思刷机刷入了其他版本号，iTunes是不允许你回复备份的，因为对iOS系统而言不同的系统版本号意为着不兼容，所以不会让你刷入。故，在爱思刷机的时候我们需要在dfu模式中强刷到与备份相同的iOS版本号。以免做无用功)
验证了备份密码后，我们就可以进入恢复模式了。
恢复过程中如果出现了“磁盘已满无法恢复”这样的沙雕提示，就点击这里看这篇文章：<a href="https://imsxx.com/itunes-ios.html" target="_blank" rel="noopener noreferrer">win10下iTunes恢复iOS版本提示“磁盘已满”的解决办法</a>。
跑完这个非常漫长的恢复备份后，就会出现上图这样的提示，这时就可以拔掉数据线了，手机会自动开机，并且让你向上滑动输入密码开始恢复数据。
接下来一切就很简单了，等待在手机上恢复，这个过程很快，接下来会验证你以前备份时的Apple ID，然后是验证手机号码，再然后是更新icloud设置，之后还有一些乱七八糟的小设置，搞定后就正式回到iOS12版本了！
完结，撒花！
: https://r2.imsxx.com/wp-content/uploads/2019/06/iOS-12-Beta-2-without-developer-account.png
: https://r2.imsxx.com/wp-content/uploads/2019/06/Snipaste_2019-06-06_02-44-53.jpg
: https://r2.imsxx.com/wp-content/uploads/2019/06/Snipaste_2019-06-06_03-35-40.jpg
