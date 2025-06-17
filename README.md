# imsxx-hugo

这是一个使用Hugo构建的静态网站，部署在GitHub Pages上并通过Cloudflare加速。

## 特性

- 使用Hugo静态网站生成器
- 采用PaperMod主题
- 通过GitHub Actions自动部署到GitHub Pages
- 使用Cloudflare进行CDN加速和安全防护

## 本地开发

### 前提条件

- 安装[Hugo Extended](https://gohugo.io/installation/)（版本0.147.8或更高）
- 安装[Git](https://git-scm.com/downloads)

### 克隆仓库

```bash
git clone https://github.com/imsxx/imsxx-hugo.git
cd imsxx-hugo
git submodule update --init --recursive
```

### 本地运行

```bash
hugo server -D
```

然后在浏览器中访问 http://localhost:1313/imsxx-hugo/

### 创建新文章

```bash
hugo new content posts/my-new-post.md
```

## 部署

本项目使用GitHub Actions自动部署。只需将更改推送到main分支，网站将自动构建并部署到GitHub Pages。

## 许可证

MIT