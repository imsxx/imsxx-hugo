---
title: 网站利用cloudflare SaaS实现分流加速国外访问
author: 梦随乡兮
date: 2022-10-16 19:00:33+00:00
hide_content: null
slug: cloudflare-saas
tags:
- cloudflare
- saas
---
<nav>
</li>
</ul></nav>
## 背景
决斗链接中文网(<a rel="nofollow" href="https://ygodl.com" target="_blank" rel="noopener">ygodl.com</a>)最开始使用的是国外服务器搭建，随着来自国内访问越来越多，加上因为被恶意举报成欺诈网站，因此寻思将网站直接签回国内进行备案，合规运营。
当前国内的域名是<a rel="nofollow" href="https://duelmeta.com/" target="_blank" rel="noopener">duelmeta.com</a>，但迁入国内后，虽然解决了被提示反诈的问题，以及提升了国内的访问速度。但原本在国外访问的体验也随之变差。
因此寻思能否在国内使用腾讯云CDN的情况下，国外的访问能够进行分流加速。
最初是寻思使用cname方式接入cloudflare来实现。
但22年cloudflare官方已经修改了协议，使用笨牛网等cloudflare三方管理平台实现cname接入的方案已经不能用了。
但好在cloudflare在之后更新了SaaS功能协议，原本这个功能需要花钱才能接入，但更新后就可以免费使用了。免费支持以cname方式接入100条域名，虽然这100条域名只能指向同一个目标地址，但对我们而言足够了。
* * *
## 前期准备
1. 注册一个中转域名，该域名不是你要加速的域名。如果你没有闲置的域名或不想花钱，那么可以在这里注册免费的<a rel="nofollow" href="http://www.freenom.com" target="_blank" rel="noopener">www.freenom.com</a>；
2. 注册cloudflare账号，在cloudflare中接入你的中转域名(NS方式接入，在你域名注册的服务商那操作)。
* * *
## 开通SaaS
在cloudflare侧边栏，点击**SSL/TLS→自定义主机名**，就会看到开通SaaS的提示。
开通是免费的，但需要绑定信用卡或paypal。cloudflare作为全球最大的免费CDN服务商，并且我使用了多年，故我个人不担心被它反向扣费，所以直接绑定了信用卡，如果担心将来协议更改导致被扣费，你可以绑定paypal。
由于我已经开通了，没有那个开通界面没法截图了，按照开通步骤操作即可。
* * *
## 设置中转信息
### 解析配置
在侧栏点击**DNS**进入域名解析页面：
<img src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017020113.png" alt="" width="264" height="229" />
<img src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017021324.png" alt="" width="1032" height="350" />
添加一条记录：
* 类型：A
* 名称：任意二级域名(它也支持顶级域名。但由于我自己还需要将ygodl.com跳转到duelmeta.com，因此用了二级域名)
* 内容：源站IP地址(即你想加速域名它的服务器IP。注如果你已经开启了国内的CDN，也是填写服务器IP，而并非CDN的IP）
* 代理状态：开(默认)
* TTL：自动（默认）
然后，保存。
### 配置SaaS
先添加**回退源**：
<img src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017020825.png" alt="" width="1030" height="237" />
这里的地址就是上面我们配置的二级域名：duelmeta.ygodl.com
※如果你用的顶级域名，直接写：ygodl.com就好了。
点击“添加回退源”，保存后刷新一下，检测是否有效。有效会显示下图这样：
<img src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017021017.png" alt="" width="996" height="156" />
### 接入域名
当上面显示“有效”，就可以开始接入我们想要加速的域名了。点击 **SSL/TLS→自定义主机名→添加自定义主机名**。
<img src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017021737.png" alt="" width="1041" height="219" />
看到以下界面后，将你要加速的域名填入(顶级域名和二级域名都行)。
<img src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017021801.png" alt="" width="640" height="356" />
其他选项保持默认，直接点**添加自定义主机名。**随后cloudflare会给出两个TXT记录：**“证书验证”**和**“主机名预验证”**。
※这里我只出现**“主机名预验证”**，是因为我在写文章之前已经做过**“证书验证”**，因此就没有了。你的域名首次验证肯定会有两条，如果出现和我一样的情况，可能是你准备的中转域名接入过cloudflare，不过这也不影响。
<img src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017022303.png" alt="" width="1086" height="642" />
然后我们切换到需要加速域名的服务商这里来设置上面给出的TXT验证。
设置如下图：
<img src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017022334.png" alt="" width="1389" height="130" />
需要注意在填写“主机记录(记录值)”时，有些服务商不用填写末尾地址，比如cloudflare给我是：
<img src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017023131.png" alt="" width="342" height="102" />
值后面带了域名，而我在腾讯解析这里并不需要写后面的域名，写了域名反而会验证不了。
<img src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017023059.png" alt="" width="444" height="102" />
如果你出现了无法验证的问题，就删掉后面的域名保存后再等等是否验证成功。
当你把TXT都设置正确后，返回到cloudflare SaaS界面，就会看到“证书状态”和“主机名状态”都识别成有效了。如下图：
<img src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017022432.png" alt="" width="1061" height="436" />
这个验证过程是cloudflare自动的，一般几分钟就好了，超过5分钟没验证通过就去加速域名服务商那改一下TXT记录，上面说的那样改。
### 解析域名
然后就可以开始解析域名了。
在加速域名服务商那，设置：
<img src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017025217.png" alt="" width="1366" height="120" />
主机记录：**SSL/TLS→自定义主机名，你设置过要加速的域名。**注意不是完整填写，如果你要加速二级域名，就填写对应的前缀。如果是加速主域名，就像我上图一样，填写@。
记录值：**完整的中转域名。**
然后就是在 **线路类型** 这里，改成**境外**。如果发现部分国内访问也在走cloudflare线路，就把原本直连的A记录或CDN的cname记录改成走**“境内”**。
<img src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017025052.png" alt="" width="1294" height="510" />
这样我们的网站，被国内访问就正常走国内的直连或CDN，当被国外访问时就走了cloudflare CDN。
* * *
## 验证是否成功
你现在可以来ping一下域名：<a rel="nofollow" href="https://tools.ipip.net/newping.php" target="_blank" rel="noopener">tools.ipip.net/newping.php</a>
<img src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017030807.png" alt="" width="693" height="704" />
可以看到国外的访问速度已经直逼国内的速度啦。另外，你如果有网络条件也可以自己看看，当你分别使用国内网络和国外网络访问时，网站应用的证书也不同。因为国内访问用了我们原本的线路和证书，而国外访问则使用了cloudflare下发的证书。
<strong>至此，大功告成！</strong>
<div id='gallery-3' class='gallery galleryid-478 gallery-columns-2 gallery-size-full'>
<dl class='gallery-item'>
<dt class='gallery-icon landscape'>
<img width="545" height="544" src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017024520.png" alt="" />
</dt>
</dl>
<dl class='gallery-item'>
<dt class='gallery-icon landscape'>
<img width="547" height="535" src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017024446.png" alt="" />
</dt>
</dl>
<br style="clear: both" />
* * *
### 重定向问题
如果在完成上面配置后出现“重定向过多”的情况，是因为Https加密模式原因。
解决办法是：
1. 在源站服务器上配置SSL证书(如果是宝塔面板，则可以快速的申请免费证书)；
2. 配置完成后打开cloudflare→SSL/TLS，将加密模式切换成“完全”；
3. 再刷新就可以看到正常打开。
: https://r2.imsxx.com/wp-content/uploads/QQ截图20221017015547.png
