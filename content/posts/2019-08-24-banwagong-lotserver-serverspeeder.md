---
title: '搬瓦工安装锐速 教程'
author: 梦随乡兮
date: 2019-08-23T16:28:37+00:00
categories:
- 笔记
tags:
- BBR
- 搬瓦工
- 网络优化
- 锐速
slug: "banwagong-lotserver-serverspeeder"
---
据说锐速比BBR更好用，所以准备试试。
文章中尝试的是萌咖大佬的全自动安装脚本：
**全自动安装**
bash <(wget --no-check-certificate -qO- https://github.com/MoeClub/lotServer/raw/master/Install.sh) install
**卸载(萌咖大佬的这个脚本支持完全卸载，不残留)**
bash <(wget --no-check-certificate -qO- https://github.com/MoeClub/lotServer/raw/master/Install.sh) uninstall
还有选择内核的手动脚本，由于我懒就不测试了，大家可以自己上库里面研究自测：
**Github**：<a rel="nofollow" href="https://github.com/MoeClub/lotServer">https://github.com/MoeClub/lotServer</a>
## **下面开始吧~**
首先尝试的是debian9 64位，结果报错了。网上查了一下据说是搬瓦工不支持换内核，但锐速对内核又有严格要求。So&#8230;
重新安装debian8 64位，这次不报错了，但提示：
> ERROR(ETHTOOL): "ethtool" not found, please install "ethtool" using "yum install ethtool" or "apt-get install ethtool" according to your linux distribution
提示vps缺少一个叫<strong>ethtool</strong>的组建，我们用
`yum install ethtool`
试试，如果报错，就用
`apt-get install ethtool`
应该就成功了。
接下来使用上面的自动安装代码，即可安装成功，安装成功的界面如下：
看上上面的界面，你就可以正常使用锐速了。不过现在它还不是那么好用，因为默认的配置并不适用于不同环境和配置的vps。
所以你需要研究一下如何调试锐速，来让它彻底发挥出来。萌咖大佬做了详细的教程，你可以前去学习研究：
<a rel="nofollow" href="https://github.com/MoeClub/lotServer/blob/master/lotServer.pdf">https://github.com/MoeClub/lotServer/blob/master/lotServer.pdf</a>
使用方法:
启动命令 `/appex/bin/lotServer.sh start`
停止加速 `/appex/bin/lotServer.sh stop`
状态查询 `/appex/bin/lotServer.sh status`
重新启动 `/appex/bin/lotServer.sh restart`
教程完~
: https://r2.imsxx.com/wp-content/uploads/2019/08/QQ截图20190824001650.png
: https://r2.imsxx.com/wp-content/uploads/2019/08/QQ截图20190824002542.png
