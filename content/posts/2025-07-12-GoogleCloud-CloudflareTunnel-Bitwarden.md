---
title: 终极指南：利用Google Cloud+Cloudflare Tunnel免费部署私人密码库Bitwarden（保姆级教程）
author: 梦随乡兮
date: 2025-07-12T00:00:00+00:00

slug: "Bitwarden"
---

最近一些网站密码被泄露了，才发现自己用谷歌浏览器已经存了700+密码，而且不少密码都是相同的，这还是蛮危险的。今天把所有密码都迁移到Bitwarden了，这篇教程将手把手教你利用 **Google Cloud** 和 **Cloudflare** 提供的永久免费服务，搭建一个完全属于你自己的、安全、私密且**零成本**的**Bitwarden**密码库。

你将获得：
*   一个功能与付费版 Bitwarden 完全一致的密码管理器。
*   数据100%存储在自己的服务器上，彻底告别隐私泄露风险。
*   无需公网IP，通过 Cloudflare 的隧道技术，安全又快速地从全球任何地方访问。
*   每月成本：**$0**。

## 核心理念：为什么这套方案能实现免费和安全？

这套方案的精妙之处在于“白嫖”了两大云服务巨头的免费套餐，并将它们无缝结合：

1.  **Google Cloud (GCP) - 你的免费服务器**
    *   **作用**：提供一台位于美国，24小时运行的微型虚拟服务器 (`e2-micro`)。
    *   **免费点**：GCP 提供[“始终免费”层级](https://cloud.google.com/free/docs/gcp-free-tier#always-free)，其中就包含了这台服务器、30GB的硬盘和每月1GB的对外流量。这对密码库来说绰绰有余。

2.  **Cloudflare Tunnel - 你的安全加密通道**
    *   **作用**：像一条加密的秘密地道，一头连接着你在GCP的服务器，另一头连接着Cloudflare的全球网络。
    *   **安全点**：你的服务器**不需要公网IP**，就像一个隐形人，黑客在互联网上根本找不到它。所有访问都必须经过Cloudflare的防火墙和加密通道，安全性极高。
    *   **免费点**：Cloudflare的这个隧道服务和它带来的流量是完全免费的。

3.  **Vaultwarden - 你的轻量级密码管家**
    *   **作用**：这是一个开源项目，用更高效的编程语言重写了Bitwarden的官方服务端，功能完全一样，但对服务器资源要求极低，非常适合在GCP的免费微型服务器上运行。

## 准备工作

1.  **一个Google Cloud账号**：[点击注册](https://cloud.google.com/)。需要绑定一张信用卡用于身份验证，但只要你不超出免费额度，就不会被收费。
2.  **一个Cloudflare账号**：[点击注册](https://www.cloudflare.com/)。免费套餐即可。
3.  **一个你自己的域名**：这是你访问密码库的地址。可以在[Namecheap](https://www.namecheap.com/)、[GoDaddy](https://www.godaddy.com/)等平台购买，一年费用通常几十元人民币。购买后，需要按照Cloudflare的提示，将域名的DNS服务器修改为Cloudflare的服务器。

## 第一部分：搭建服务器 (Google Cloud)

1.  登录 [Google Cloud Console](https://console.cloud.google.com/)。
2.  导航到 **“计算引擎 (Compute Engine)” > “VM 实例”**，然后点击 **“创建实例”**。
3.  按照以下**关键配置**进行设置，确保免费：
    *   **名称**：随意，例如 `bitwarden-server`。
    *   **区域 (Region)**：**务必**选择以下三个之一（`us-west1`离中国最近）：
        *   `us-west1` (俄勒冈)
        *   `us-central1` (爱荷华)
        *   `us-east1` (南卡罗来纳)
    *   **机器类型 (Machine type)**：选择 **`e2-micro`**。
    *   **启动磁盘 (Boot disk)**：点击“更改”，将**“启动磁盘类型”**修改为 **“标准永久性磁盘”**，大小设置为`30` GB或更小。
    *   **防火墙 (Firewall)**：**不要**勾选 "允许 HTTP 流量" 或 "允许 HTTPS 流量"。

> **⚠️ 注意：** 此时右侧的“每月估算费用”可能会显示约$7.11，**请忽略它！** 这是标准价格，GCP会在月底结算时自动应用免费额度进行抵扣，只要你的配置完全符合上述要求，最终账单就是$0。

4.  点击 **“创建”**，等待几分钟，你的免费服务器就准备好了。

## 第二部分：安装密码管家 (Vaultwarden)

1.  在VM实例列表中，找到你刚创建的服务器，点击最右侧的 **“SSH”** 按钮，浏览器会弹出一个终端窗口。
2.  在终端里，依次输入以下命令来安装 Docker（一个容器化工具）：
    ```bash
    sudo apt-get update
    sudo apt-get install -y docker.io
    ```
3.  运行下面这行命令，一键启动你的Vaultwarden密码库服务：
    ```bash
    sudo docker run -d --name vaultwarden -v /vw-data/:/data/ -p 8080:80 --restart unless-stopped vaultwarden/server:latest
    ```

## 第三部分：创建安全通道 (Cloudflare Tunnel)

1.  登录 Cloudflare 仪表板，选择你的域名。
2.  在左侧菜单中，找到并点击 **“Zero Trust”**。
3.  进入Zero Trust仪表板后，在左侧导航到 **“Networks” > “Tunnels”**。
4.  点击 **“Create a tunnel”**，给隧道起个名字（如`bitwarden-gcp`），保存。
5.  在“Choose your environment”页面，选择 **“Debian”**，然后复制下面框里的那段以`curl`开头的命令。
6.  回到你GCP的**SSH终端窗口**，粘贴并运行刚刚复制的命令。这会自动安装并配置好通道。
7.  稍等片刻，Cloudflare页面会显示你的连接器已激活。点击 **“Next”**。
8.  现在配置公共访问地址：
    *   **子域名 (Subdomain)**：输入你想要的地址前缀，例如 `bw`。
    *   **域名 (Domain)**：选择你的域名。
    *   **服务 (Service)**：
        *   **Type**: 选择 `HTTP`。
        *   **URL**: 输入 `localhost:8080`。

> **解惑：** 这里使用HTTP是安全的，因为这是`cloudflared`在服务器**内部**与Vaultwarden通信，流量并未离开服务器，不产生任何费用。你从外部访问`https://bw.yourdomain.com`的全程都是被Cloudflare加密的。

9.  点击 **“Save hostname”**。

**恭喜你！部署已全部完成！** 等待一两分钟，现在访问 `https://bw.yourdomain.com`，你应该能看到Bitwarden的登录页面了。

## 第四部分：安全加固与数据迁移

### 1. 【必须做！】禁止新用户注册

在你注册完自己的账号后，为了安全，必须禁止其他人注册。

1.  回到GCP的SSH终端。
2.  依次执行以下三条命令，用新的配置重建容器（数据不会丢失）：
    ```bash
    # 停止当前容器
    sudo docker stop vaultwarden
    # 移除旧容器
    sudo docker rm vaultwarden
    # 使用禁止注册的配置重新启动
    sudo docker run -d --name vaultwarden -e SIGNUPS_ALLOWED=false -v /vw-data/:/data/ -p 8080:80 --restart unless-stopped vaultwarden/server:latest
    ```
3.  刷新你的登录页面，会发现“创建账户”的按钮已经消失了。

### 2. 从Chrome浏览器导入密码

1.  **导出**：在Chrome地址栏输入 `chrome://settings/passwords`，在右侧菜单中选择“导出密码”。
2.  **导入**：登录你的Vaultwarden网页版，进入 **“工具” > “导入数据”**，格式选择“Chrome (csv)”，然后上传文件即可。
3.  **清理**：导出的`.csv`文件是明文，导入后请**立即彻底删除它**。

### 3. 配置浏览器插件，接管一切

1.  从[Chrome应用商店](https://chrome.google.com/webstore/detail/bitwarden-free-password-m/nngceckbapebfimnlniiabkocgnaoemj)安装官方**Bitwarden**插件。
2.  点击插件图标，点击左上角的**齿轮设置**。
3.  在**“服务器URL”**中，填入你的完整域名 `https://bw.yourdomain.com`，保存。
4.  用你的主密码登录插件。
5.  回到`chrome://settings/passwords`，关闭“要约保存密码”和“自动登录”。

自此，Bitwarden插件将全面接管你的密码管理，提供自动填充和保存功能。

## 第五部分：常见问题（FAQ）

**问：如果我忘记了Vaultwarden的主密码怎么办？**

**答：没办法。** 这是Bitwarden零知识加密设计的核心，意味着**连作为服务器管理员的你也无法查看或重置密码**。服务器上只存了一堆谁也解不开的乱码。这是为了极致的安全。
*   **唯一的机会**：注册时设置的“密码提示”。
*   **最后的手段**：作为管理员，你可以登录服务器后台删除这个账户，让用户用原邮箱重新注册一个**空的**密码库。之前的数据将**永久丢失**。所以，请务必牢记你的主密码！
---

至此，你已经拥有了一个功能强大、安全可靠且完全免费的私人密码库。享受掌控自己数据的自由吧！