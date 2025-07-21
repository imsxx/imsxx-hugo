---
title: VPS + Docker + Vaultwarden 自动化备份至 OneDrive 超详细图文指南（含所有踩坑点及解决方案）
author: 梦随乡兮
date: 2025-07-18T00:00:00+00:00
slug: "VPS-Docker-Vaultwarden-OneDrive"
categories: ["笔记"]
tags: 
- VPS
- Docker
- Vaultwarden
- OneDrive
---

## 前言

大家好，前几天不是开启用Vaultwarden来保存密码么，虽然我经常也在思考银行为什么要用6位数来保存我3位数的余额~不过嘛，安全意识总归没错。自从在自己的 VPS 上用 Docker 搭建了 Vaultwarden 密码管理器后，使用体验非常好。但心里总有一个疙瘩：我所有密码都存在这个 VPS 上，虽然谷歌云服务还是挺靠谱的，但万一哪天服务器硬盘损坏、被黑客攻击或者我手滑误删了数据，后果不堪设想。

因此，建立一个**自动化、异地**的备份策略就显得至关重要。我选择的方案是将 Vaultwarden 的数据每天自动打包，并上传到免费又大碗的 Microsoft OneDrive 上。大碗是因为我常年开office365有1T存储，用都用不完。其实免费5G也完全够用了，备份密码这些压根用不到多少存储。

这篇文章记录了我从零开始实现这一目标的完整过程，包括我遇到的**每一个坑**和**最终的解决方案**。希望能帮助到和我有同样需求的朋友们，让你们少走弯路。

## 我的环境

*   **服务器**: Google Cloud VPS  免费额度内的小玩意儿(Debian 系统)
*   **密码服务**: Vaultwarden (通过 Docker 部署)
*   **备份目标**: Microsoft OneDrive

## 备份流程图

我们的最终目标是实现这样一个自动化流程：

`VPS 定时任务 (Cron)` -> `运行备份脚本` -> `停止 Vaultwarden 容器` -> `打包数据` -> `重启容器` -> `上传备份文件到 OneDrive` -> `删除本地旧备份`

## 第一步：安装并配置 Rclone 连接 OneDrive

Rclone 是一款强大的命令行工具，是连接 VPS 和 OneDrive 之间的桥梁。

**1. 安装 Rclone**

在 VPS 命令行中，运行官方安装脚本：
```bash
sudo -v ; curl https://rclone.org/install.sh | sudo bash
```

> **⚠️ 新手踩坑点 #1：解压工具缺失**
>
> **我的遭遇**：我第一次运行时，脚本报错 `None of the supported tools for extracting zip archives (unzip 7z busybox) were found.`
> **原因分析**：这个错误很直白，我的 VPS 是一个非常纯净的系统，连最基础的 `unzip` 解压缩工具都没有。Rclone 的安装脚本需要它来解压下载的程序文件。
> **解决方案**：先安装 `unzip` 即可。
> ```bash
> # 适用于 Debian/Ubuntu 系统
> sudo apt-get update
> sudo apt-get install unzip -y
> ```
> 安装完 `unzip` 后，再重新运行上面的 Rclone 安装脚本，就顺利成功了。

**2. 配置 Rclone**

这是整个过程中最关键、交互最多的一步，请务必仔细。

运行配置命令：
```bash
rclone config
```

接下来，Rclone 会一步步引导你。下面是我选择的关键步骤：

*   `n) New remote` -> 输入 `n` 新建一个连接。
*   `name>` -> 输入一个你喜欢的名字，我用的是 `onedrive`。
*   `Storage>` -> 在长长的列表中找到 `Microsoft OneDrive`，输入它前面的数字（我的是 `38`）。
*   `client_id>` 和 `client_secret>` -> **直接按回车**，留空即可。
*   `region>` -> **直接按回车**，选择默认的 `global` 全球区域。除非你明确知道自己用的是世纪互联运营的特殊版本。
*   `Edit advanced config?` -> 输入 `n`。
*   `Use auto config?` -> **输入 `n`**。这是关键！因为我们的 VPS 没有浏览器。

> **⚠️ 新手踩坑点 #2：在没有浏览器的服务器上如何授权？**
>
> **我的遭遇**：选择了 `n` 之后，终端显示需要我运行 `rclone authorize "onedrive"` 并把结果粘贴回来。
> **原因分析**：这是 Rclone 的远程授权机制。它需要在**一台有浏览器的电脑**上生成一个授权“令牌 (Token)”，然后我们把这个令牌“喂”给在 VPS 上的 Rclone。
> **解决方案**：
>
> 1.  **在我的个人电脑上 (Windows)**：
>     *   去 Rclone 官网下载了 Windows 版的 `rclone.exe`。
>     *   打开电脑的 CMD (命令提示符)，用 `cd` 命令进入到 `rclone.exe` 所在的文件夹。
>     *   运行命令：`rclone.exe authorize "onedrive"`
>     *   这时，我的电脑自动弹出了浏览器，让我登录微软账户并授权。
>     *   授权成功后，回到 CMD 窗口，它显示了一大长串以 `{...}` 包裹的文本。**完整地**复制这一大串文本。
> 2.  **回到我的 VPS 终端**：
>     *   将刚才复制的 `{...}` 文本，完整地粘贴到 `config_token>` 这个提示符后面，按回车。
>
> 这样，授权就成功传递给了 VPS！

*   接下来的步骤就很简单了，选择你的 OneDrive 类型（我选 `OneDrive Personal or Business`），确认 Drive 信息，最后一路选 `y` (Yes) 保存，再按 `q` 退出配置。

## 第二步：编写智能的备份脚本 `backup.sh`

这个脚本是整个自动化流程的核心。

**1. 创建并编辑脚本**
```bash
nano backup.sh
```

**2. 粘贴最终版的脚本内容**

这是我们经历了九九八十一难后，最终调优完成的完美脚本：

```bash
#!/bin/bash

# 任何命令失败则立即退出
set -e

# --- 开始配置 ---
# 你的 Vaultwarden Docker 容器的名称
CONTAINER_NAME="vaultwarden"
# Vaultwarden 数据在 VPS 上的存储目录 (重要！)
VAULTWARDEN_DATA_DIR="/vw-data"
# 备份文件在 VPS 上的临时存放目录
BACKUP_DIR="/home/imsxx_com/vaultwarden_backups"
# Rclone 远程连接的名称
RCLONE_REMOTE_NAME="onedrive"
# OneDrive 中用于存放备份的文件夹名称
ONEDRIVE_BACKUP_DIR="VaultwardenBackups"
# --- 结束配置 ---


# --- 脚本主体 (通常无需修改) ---
echo "备份流程开始于: $(date +"%Y-%m-%d %H:%M:%S")"

mkdir -p "$BACKUP_DIR"

BACKUP_FILE="vaultwarden-backup-$(date +%Y%m%d-%H%M%S).tar.gz"
BACKUP_FILE_PATH="$BACKUP_DIR/$BACKUP_FILE"

echo "准备停止 Vaultwarden 容器..."
sudo docker stop "$CONTAINER_NAME"

echo "容器已停止，开始创建备份文件: $BACKUP_FILE_PATH"
tar -czf "$BACKUP_FILE_PATH" -C "$VAULTWARDEN_DATA_DIR" .

echo "备份文件创建完成，准备重启 Vaultwarden 容器..."
sudo docker start "$CONTAINER_NAME"

echo "容器已重启。本地备份完成。"

echo "开始上传备份文件到 OneDrive 的 '$ONEDRIVE_BACKUP_DIR' 文件夹..."
# 使用带有正确配置文件路径的 rclone 命令，这是关键！
rclone --config "/home/imsxx_com/.config/rclone/rclone.conf" copy "$BACKUP_FILE_PATH" "$RCLONE_REMOTE_NAME:$ONEDRIVE_BACKUP_DIR" --progress

echo "文件上传成功。"

echo "开始清理7天前的本地旧备份..."
find "$BACKUP_DIR" -type f -name "*.tar.gz" -mtime +7 -delete
echo "旧备份清理完毕。"

echo "备份流程全部完成于: $(date +"%Y-%m-%d %H:%M:%S")"
```

> **⚠️ 新手踩坑点 #3：如何找到正确的 `VAULTWARDEN_DATA_DIR`？**
>
> **我的遭遇**：我不确定这个路径到底是什么。
> **原因分析**：这个路径不是 Docker 容器里的 `/data`，而是你当初运行 `docker run` 命令时，通过 `-v` 参数映射到宿主机（VPS）上的真实路径。
> **解决方案**：运行 `sudo docker inspect vaultwarden` 命令，在输出的一大堆信息里，找到 `"Mounts"` 部分，里面的 `"Source"` 对应的路径，就是我们需要的正确路径！对我来说，就是 `"/vw-data"`。

**3. 赋予脚本执行权限**

> **⚠️ 新手踩坑点 #4：脚本无法运行，提示 `Permission denied`**
>
> **我的遭遇**：我满心欢喜地运行 `./backup.sh`，结果无情地被 `Permission denied`。
> **原因分析**：在 Linux 中，新创建的文件默认没有“执行”权限。
> **解决方案**：用 `chmod` 命令给它加上执行权限。
> ```bash
> chmod +x backup.sh
> ```

**4. 测试脚本**

> **⚠️ 新手踩坑点 #5：脚本能停 Docker，但 Rclone 报错找不到配置**
>
> **我的遭遇**：我使用 `sudo ./backup.sh` 运行测试，Docker 正常启停，但 Rclone 报错 `Config file "/root/.config/rclone/rclone.conf" not found`。
> **原因分析**：这是个很微妙的权限问题！
> *   因为脚本里操作 Docker 需要 `sudo` 权限，所以我用 `sudo` 来运行整个脚本。
> *   当用 `sudo` 运行时，脚本的执行身份就从我的普通用户 `imsxx_com` 变成了超级用户 `root`。
> *   `root` 用户运行 `rclone` 时，会去它自己的主目录 `/root/.config/...` 找配置文件，但我们的配置文件明明在 `/home/imsxx_com/.config/...` 里，它当然找不到了！
> **解决方案**：在脚本的 `rclone` 命令里，使用 `--config` 参数，**明确地**告诉它配置文件的绝对路径！同时，为了让定时任务也能正常运行，脚本内操作 Docker 的命令前也要加上 `sudo`。这就是上面最终版脚本里那样写的原因。

经过修改后，再次运行 `sudo ./backup.sh`，终于！我看到了上传成功的进度条！

### 第三步：设置 Cron 定时任务，实现全自动！

这是我们的最后一步，让系统每天自动执行这个完美的脚本。但这也是**最容易出问题、最迷惑人**的一步。

**1. 编辑定时任务**

```bash
crontab -e
```

选择 `nano` 作为编辑器后，在打开的文件末尾添加以下任务指令：

```
0 3 * * * /home/imsxx_com/backup.sh >> /home/imsxx_com/vaultwarden_backup.log 2>&1
```

**2. 见证奇迹……失败了？—— 终极踩坑点降临！**

我满心欢喜地设置好定时任务，然后等了两天。结果，我的 OneDrive 里空空如也！备份并没有自动执行。

> **⚠️ 新手踩坑点 #6：手动执行一切正常，定时任务却“装死”**
> 
> **我的遭遇**：我手动运行 `sudo ./backup.sh` 时，脚本完美执行，文件成功上传。但到了设定时间，`cron` 却好像什么都没做。
> **原因分析（破案关键）**：我们之前为了排查问题，在定时任务命令的末尾加上了一段日志记录代码 `>> ... .log 2>&1`。现在，正是它派上用场的时候！我立刻登录 VPS，查看这个“黑匣子”：
> 
> ```bash
> cat /home/imsxx_com/vaultwarden_backup.log
> ```
> 
> 日志里赫然显示着这样的错误信息：
> 
> ```
> sudo: a terminal is required to read the password; ...
> sudo: a password is required
> ```
> 
> **真相大白！**
> 
> * 我们手动执行时，是在一个**交互式终端**里。当脚本里的 `sudo docker...` 命令需要管理员权限时，系统会提示我们输入密码，我们输入后，授权通过，脚本继续。
> * 但 `cron` 是在**后台非交互式环境**中执行任务的。当 `sudo` 命令需要密码时，它找不到一个可以弹出提示框的地方，也等不到任何人来输入密码。因此，它只能卡在那里，然后报错退出，导致整个备份流程中断。
> 
> **解决方案（最安全、最专业的做法）**：我们需要明确地告诉系统，允许我的用户 `imsxx_com` 在执行**指定的 Docker 命令**时，**无需输入密码**。
> 
> 1. **使用 `visudo` 安全地编辑权限文件**。这个命令会在保存时检查语法，防止我们手滑把系统搞坏。
>     
>     ```bash
>     sudo visudo
>     ```
> 2. **在文件末尾添加免密授权规则**。在打开的编辑器里，移动到最底部，添加下面这一行：
>     
>     ```
>     imsxx_com ALL=(ALL) NOPASSWD: /usr/bin/docker stop vaultwarden, /usr/bin/docker start vaultwarden
>     ```
>     
>     这行配置的意思是：仅授权 `imsxx_com` 用户，在执行“停止 vaultwarden 容器”和“启动 vaultwarden 容器”这两个**具体操作**时，不需要输入密码。这既解决了自动化的问题，又最大限度地保证了系统的安全。
> 3. **保存并退出** (`Ctrl + X` -> `Y` -> `Enter`)。

在解决了这个终极 `sudo` 密码问题后，我终于可以安心地等待下一个凌晨3点的到来。第二天早上，我惊喜地在 OneDrive 的 `VaultwardenBackups` 文件夹里，看到了两个崭新的备份文件！成功了！

## 总结

至此，我已经为我的 Vaultwarden 建立了一个强大、可靠且全自动的异地备份系统。整个过程虽然踩了不少坑，尤其是最后那个关于 `cron` 和 `sudo` 交互的经典问题，但每解决一个问题，都让我对 Linux 的理解更深了一层。

希望我这份详尽的“踩坑”指南能对你有所帮助。给重要的数据一份备份，就是给自己一份安心。现在，我终于可以高枕无忧了！

