---
title: 网站利用cloudflare SaaS实现分流加速国外访问
author: 梦随乡兮
type: post
date: 2022-10-16T19:00:33+00:00
url: /cloudflare-saas.html
featured_image: https://r2.imsxx.com/wp-content/uploads/2022101811593311.png
views:
  - 3712
hide_content:
  - close
like:
  - 1
categories:
  - 笔记
tags:
  - CDN
  - cloudflare
  - cloudflare SaaS
  - SaaS
  - 网站加速

slug: "cloudflare-saas"
---
<div id="ez-toc-container" class="ez-toc-v2_0_73 counter-hierarchy ez-toc-counter ez-toc-transparent ez-toc-container-direction">
  <div class="ez-toc-title-container">
    <p class="ez-toc-title" style="cursor:inherit">
      本文目录
    </p>
    
    <span class="ez-toc-title-toggle"><a href="#" class="ez-toc-pull-right ez-toc-btn ez-toc-btn-xs ez-toc-btn-default ez-toc-toggle" aria-label="Toggle Table of Content"><span class="ez-toc-js-icon-con"><span class=""><span class="eztoc-hide" style="display:none;">Toggle</span><span class="ez-toc-icon-toggle-span"><svg style="fill: #999;color:#999" xmlns="http://www.w3.org/2000/svg" class="list-377408" width="20px" height="20px" viewBox="0 0 24 24" fill="none"><path d="M6 6H4v2h2V6zm14 0H8v2h12V6zM4 11h2v2H4v-2zm16 0H8v2h12v-2zM4 16h2v2H4v-2zm16 0H8v2h12v-2z" fill="currentColor"></path></svg><svg style="fill: #999;color:#999" class="arrow-unsorted-368013" xmlns="http://www.w3.org/2000/svg" width="10px" height="10px" viewBox="0 0 24 24" version="1.2" baseProfile="tiny"><path d="M18.2 9.3l-6.2-6.3-6.2 6.3c-.2.2-.3.4-.3.7s.1.5.3.7c.2.2.4.3.7.3h11c.3 0 .5-.1.7-.3.2-.2.3-.5.3-.7s-.1-.5-.3-.7zM5.8 14.7l6.2 6.3 6.2-6.3c.2-.2.3-.5.3-.7s-.1-.5-.3-.7c-.2-.2-.4-.3-.7-.3h-11c-.3 0-.5.1-.7.3-.2.2-.3.5-.3.7s.1.5.3.7z"/></svg></span></span></span></a></span>
  </div><nav>
  
  <ul class='ez-toc-list ez-toc-list-level-1 ' >
    <li class='ez-toc-page-1 ez-toc-heading-level-2'>
      <a class="ez-toc-link ez-toc-heading-1" href="https://imsxx.com/cloudflare-saas.html/#%E8%83%8C%E6%99%AF" title="背景">背景</a>
    </li>
    <li class='ez-toc-page-1 ez-toc-heading-level-2'>
      <a class="ez-toc-link ez-toc-heading-2" href="https://imsxx.com/cloudflare-saas.html/#%E5%89%8D%E6%9C%9F%E5%87%86%E5%A4%87" title="前期准备">前期准备</a>
    </li>
    <li class='ez-toc-page-1 ez-toc-heading-level-2'>
      <a class="ez-toc-link ez-toc-heading-3" href="https://imsxx.com/cloudflare-saas.html/#%E5%BC%80%E9%80%9ASaaS" title="开通SaaS">开通SaaS</a>
    </li>
    <li class='ez-toc-page-1 ez-toc-heading-level-2'>
      <a class="ez-toc-link ez-toc-heading-4" href="https://imsxx.com/cloudflare-saas.html/#%E8%AE%BE%E7%BD%AE%E4%B8%AD%E8%BD%AC%E4%BF%A1%E6%81%AF" title="设置中转信息">设置中转信息</a><ul class='ez-toc-list-level-3' >
        <li class='ez-toc-heading-level-3'>
          <a class="ez-toc-link ez-toc-heading-5" href="https://imsxx.com/cloudflare-saas.html/#%E8%A7%A3%E6%9E%90%E9%85%8D%E7%BD%AE" title="解析配置">解析配置</a>
        </li>
        <li class='ez-toc-page-1 ez-toc-heading-level-3'>
          <a class="ez-toc-link ez-toc-heading-6" href="https://imsxx.com/cloudflare-saas.html/#%E9%85%8D%E7%BD%AESaaS" title="配置SaaS">配置SaaS</a>
        </li>
        <li class='ez-toc-page-1 ez-toc-heading-level-3'>
          <a class="ez-toc-link ez-toc-heading-7" href="https://imsxx.com/cloudflare-saas.html/#%E6%8E%A5%E5%85%A5%E5%9F%9F%E5%90%8D" title="接入域名">接入域名</a>
        </li>
        <li class='ez-toc-page-1 ez-toc-heading-level-3'>
          <a class="ez-toc-link ez-toc-heading-8" href="https://imsxx.com/cloudflare-saas.html/#%E8%A7%A3%E6%9E%90%E5%9F%9F%E5%90%8D" title="解析域名">解析域名</a>
        </li>
      </ul>
    </li>
    
    <li class='ez-toc-page-1 ez-toc-heading-level-2'>
      <a class="ez-toc-link ez-toc-heading-9" href="https://imsxx.com/cloudflare-saas.html/#%E9%AA%8C%E8%AF%81%E6%98%AF%E5%90%A6%E6%88%90%E5%8A%9F" title="验证是否成功">验证是否成功</a><ul class='ez-toc-list-level-3' >
        <li class='ez-toc-heading-level-3'>
          <a class="ez-toc-link ez-toc-heading-10" href="https://imsxx.com/cloudflare-saas.html/#%E9%87%8D%E5%AE%9A%E5%90%91%E9%97%AE%E9%A2%98" title="重定向问题">重定向问题</a>
        </li>
      </ul>
    </li>
  </ul></nav>
</div>

## <span class="ez-toc-section" id="%E8%83%8C%E6%99%AF"></span>背景<span class="ez-toc-section-end"></span>

决斗链接中文网(<a rel="nofollow" href="https://ygodl.com" target="_blank" rel="noopener">ygodl.com</a>)最开始使用的是国外服务器搭建，随着来自国内访问越来越多，加上因为被恶意举报成欺诈网站，因此寻思将网站直接签回国内进行备案，合规运营。

当前国内的域名是<a rel="nofollow" href="https://duelmeta.com/" target="_blank" rel="noopener">duelmeta.com</a>，但迁入国内后，虽然解决了被提示反诈的问题，以及提升了国内的访问速度。但原本在国外访问的体验也随之变差。

因此寻思能否在国内使用腾讯云CDN的情况下，国外的访问能够进行分流加速。

最初是寻思使用cname方式接入cloudflare来实现。

但22年cloudflare官方已经修改了协议，使用笨牛网等cloudflare三方管理平台实现cname接入的方案已经不能用了。

但好在cloudflare在之后更新了SaaS功能协议，原本这个功能需要花钱才能接入，但更新后就可以免费使用了。免费支持以cname方式接入100条域名，虽然这100条域名只能指向同一个目标地址，但对我们而言足够了。

* * *

## <span class="ez-toc-section" id="%E5%89%8D%E6%9C%9F%E5%87%86%E5%A4%87"></span>前期准备<span class="ez-toc-section-end"></span>

  1. 注册一个中转域名，该域名不是你要加速的域名。如果你没有闲置的域名或不想花钱，那么可以在这里注册免费的<a rel="nofollow" href="http://www.freenom.com" target="_blank" rel="noopener">www.freenom.com</a>；
  2. 注册cloudflare账号，在cloudflare中接入你的中转域名(NS方式接入，在你域名注册的服务商那操作)。

* * *

## <span class="ez-toc-section" id="%E5%BC%80%E9%80%9ASaaS"></span>开通SaaS<span class="ez-toc-section-end"></span>

在cloudflare侧边栏，点击**SSL/TLS→自定义主机名**，就会看到开通SaaS的提示。

[<img loading="lazy" decoding="async" class="aligncenter wp-image-479 size-full" src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017015547.png" alt="" width="263" height="525" />][1]

开通是免费的，但需要绑定信用卡或paypal。cloudflare作为全球最大的免费CDN服务商，并且我使用了多年，故我个人不担心被它反向扣费，所以直接绑定了信用卡，如果担心将来协议更改导致被扣费，你可以绑定paypal。

由于我已经开通了，没有那个开通界面没法截图了，按照开通步骤操作即可。

* * *

## <span class="ez-toc-section" id="%E8%AE%BE%E7%BD%AE%E4%B8%AD%E8%BD%AC%E4%BF%A1%E6%81%AF"></span>设置中转信息<span class="ez-toc-section-end"></span>

### <span class="ez-toc-section" id="%E8%A7%A3%E6%9E%90%E9%85%8D%E7%BD%AE"></span>解析配置<span class="ez-toc-section-end"></span>

在侧栏点击**DNS**进入域名解析页面：

<img loading="lazy" decoding="async" class="aligncenter size-full wp-image-480" src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017020113.png" alt="" width="264" height="229" /> 

<img loading="lazy" decoding="async" class="aligncenter size-full wp-image-484" src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017021324.png" alt="" width="1032" height="350" /> 

添加一条记录：

  * 类型：A
  * 名称：任意二级域名(它也支持顶级域名。但由于我自己还需要将ygodl.com跳转到duelmeta.com，因此用了二级域名)
  * 内容：源站IP地址(即你想加速域名它的服务器IP。注如果你已经开启了国内的CDN，也是填写服务器IP，而并非CDN的IP）
  * 代理状态：开(默认)
  * TTL：自动（默认）

然后，保存。

### <span class="ez-toc-section" id="%E9%85%8D%E7%BD%AESaaS"></span>配置SaaS<span class="ez-toc-section-end"></span>

先添加**回退源**：

<img loading="lazy" decoding="async" class="aligncenter size-full wp-image-482" src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017020825.png" alt="" width="1030" height="237" /> 

这里的地址就是上面我们配置的二级域名：duelmeta.ygodl.com

<span style="color: #999999;">※如果你用的顶级域名，直接写：ygodl.com就好了。</span>

点击“添加回退源”，保存后刷新一下，检测是否有效。有效会显示下图这样：

<img loading="lazy" decoding="async" class="aligncenter size-full wp-image-483" src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017021017.png" alt="" width="996" height="156" /> 

### <span class="ez-toc-section" id="%E6%8E%A5%E5%85%A5%E5%9F%9F%E5%90%8D"></span>接入域名<span class="ez-toc-section-end"></span>

当上面显示“有效”，就可以开始接入我们想要加速的域名了。点击 **SSL/TLS→自定义主机名→添加自定义主机名**。

<img loading="lazy" decoding="async" class="aligncenter size-full wp-image-486" src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017021737.png" alt="" width="1041" height="219" /> 

看到以下界面后，将你要加速的域名填入(顶级域名和二级域名都行)。

<img loading="lazy" decoding="async" class="aligncenter wp-image-485" src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017021801.png" alt="" width="640" height="356" /> 

其他选项保持默认，直接点**添加自定义主机名。**随后cloudflare会给出两个TXT记录：**“证书验证”**和**“主机名预验证”**。

※这里我只出现**“主机名预验证”**，是因为我在写文章之前已经做过**“证书验证”**，因此就没有了。你的域名首次验证肯定会有两条，如果出现和我一样的情况，可能是你准备的中转域名接入过cloudflare，不过这也不影响。

<img loading="lazy" decoding="async" class="aligncenter size-full wp-image-487" src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017022303.png" alt="" width="1086" height="642" /> 

然后我们切换到需要加速域名的服务商这里来设置上面给出的TXT验证。

设置如下图：

<img loading="lazy" decoding="async" class="aligncenter size-full wp-image-488" src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017022334.png" alt="" width="1389" height="130" /> 

需要注意在填写“主机记录(记录值)”时，有些服务商不用填写末尾地址，比如cloudflare给我是：

<img loading="lazy" decoding="async" class="aligncenter size-full wp-image-491" src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017023131.png" alt="" width="342" height="102" /> 

值后面带了域名，而我在腾讯解析这里并不需要写后面的域名，写了域名反而会验证不了。

<img loading="lazy" decoding="async" class="aligncenter size-full wp-image-490" src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017023059.png" alt="" width="444" height="102" /> 

如果你出现了无法验证的问题，就删掉后面的域名保存后再等等是否验证成功。

当你把TXT都设置正确后，返回到cloudflare SaaS界面，就会看到“证书状态”和“主机名状态”都识别成有效了。如下图：

<img loading="lazy" decoding="async" class="aligncenter size-full wp-image-489" src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017022432.png" alt="" width="1061" height="436" /> 

这个验证过程是cloudflare自动的，一般几分钟就好了，超过5分钟没验证通过就去加速域名服务商那改一下TXT记录，上面说的那样改。

### <span class="ez-toc-section" id="%E8%A7%A3%E6%9E%90%E5%9F%9F%E5%90%8D"></span>解析域名<span class="ez-toc-section-end"></span>

然后就可以开始解析域名了。

在加速域名服务商那，设置：

<img loading="lazy" decoding="async" class="aligncenter size-full wp-image-493" src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017025217.png" alt="" width="1366" height="120" /> 

主机记录：**SSL/TLS→自定义主机名，你设置过要加速的域名。**注意不是完整填写，如果你要加速二级域名，就填写对应的前缀。如果是加速主域名，就像我上图一样，填写@。

记录值：**完整的中转域名。**

然后就是在 **线路类型** 这里，改成**境外**。如果发现部分国内访问也在走cloudflare线路，就把原本直连的A记录或CDN的cname记录改成走**“境内”**。

<img loading="lazy" decoding="async" class="aligncenter size-full wp-image-494" src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017025052.png" alt="" width="1294" height="510" /> 

这样我们的网站，被国内访问就正常走国内的直连或CDN，当被国外访问时就走了cloudflare CDN。

* * *

## <span class="ez-toc-section" id="%E9%AA%8C%E8%AF%81%E6%98%AF%E5%90%A6%E6%88%90%E5%8A%9F"></span>验证是否成功<span class="ez-toc-section-end"></span>

你现在可以来ping一下域名：<a rel="nofollow" href="https://tools.ipip.net/newping.php" target="_blank" rel="noopener">tools.ipip.net/newping.php</a>

<img loading="lazy" decoding="async" class="aligncenter size-full wp-image-499" src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017030807.png" alt="" width="693" height="704" /> 

可以看到国外的访问速度已经直逼国内的速度啦。另外，你如果有网络条件也可以自己看看，当你分别使用国内网络和国外网络访问时，网站应用的证书也不同。因为国内访问用了我们原本的线路和证书，而国外访问则使用了cloudflare下发的证书。

<span style="color: #ff0000;"><strong>至此，大功告成！</strong></span>

<div id='gallery-3' class='gallery galleryid-478 gallery-columns-2 gallery-size-full'>
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <img loading="lazy" decoding="async" width="545" height="544" src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017024520.png" class="attachment-full size-full" alt="" />
    </dt>
  </dl>
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <img loading="lazy" decoding="async" width="547" height="535" src="https://r2.imsxx.com/wp-content/uploads/QQ截图20221017024446.png" class="attachment-full size-full" alt="" />
    </dt>
  </dl>
  
  <br style="clear: both" />
</div>

* * *

### <span class="ez-toc-section" id="%E9%87%8D%E5%AE%9A%E5%90%91%E9%97%AE%E9%A2%98"></span>重定向问题<span class="ez-toc-section-end"></span>

如果在完成上面配置后出现“重定向过多”的情况，是因为Https加密模式原因。

解决办法是：

  1. 在源站服务器上配置SSL证书(如果是宝塔面板，则可以快速的申请免费证书)；
  2. 配置完成后打开cloudflare→SSL/TLS，将加密模式切换成“完全”；
  3. 再刷新就可以看到正常打开。

 [1]: https://r2.imsxx.com/wp-content/uploads/QQ截图20221017015547.png

