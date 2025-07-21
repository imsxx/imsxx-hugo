# imsxx-hugo 博客

这是我的个人博客仓库，使用 [Hugo](https://gohugo.io/) 和 [hugo-narrow](https://github.com/bep/hugo-narrow) 主题构建。

## 开发

请按照以下说明在本地运行网站以进行开发和测试。

### 环境依赖

- [Hugo](https://gohugo.io/installation) (推荐使用 extended 版本)
- [Node.js](https://nodejs.org/) (包含 npm)
- [Tailwind CSS](https://tailwindcss.com/)

### 运行服务

1.  克隆本仓库。
2.  安装依赖:
    ```bash
    npm install
    ```
3.  运行 Hugo 服务:
    ```bash
    hugo server -D
    ```
网站将在 `http://localhost:1313/` 上可用。

## 主题定制

本博客使用 `hugo-narrow` 主题。自定义，特别是样式方面，需要特定的步骤。

### 添加自定义配色方案

1.  **创建新的 CSS 文件**: 在 `themes/hugo-narrow/assets/css/custom/` 目录下为你的主题创建一个新的 `.css` 文件。例如: `themes/hugo-narrow/assets/css/custom/my-theme.css`。

2.  **定义主题**: 在你的新 CSS 文件中，在 `data-theme` 属性选择器下定义颜色变量。例如:
    ```css
    [data-theme="my-theme"] {
      --color-primary: #ff0000;
      --color-secondary: #00ff00;
      /* ... 其他颜色变量 ... */
    }
    ```

3.  **导入新主题**: 打开 `themes/hugo-narrow/assets/css/custom.css` 并导入你的新主题文件:
    ```css
    @import "./custom/my-theme.css";
    ```

4.  **在 `hugo.toml` 中注册主题**: 将新主题添加到项目根目录下的 `hugo.toml` 文件中的 `[params.themes]` 部分。确保 `name` 与你在 CSS 中使用的 `data-theme` 属性匹配。
    ```toml
    [params.themes.my-theme]
      name = "my-theme"
      order = 6 # 或任何其他唯一的顺序编号
    ```

5.  **重新编译 CSS**: 添加或修改任何 CSS 后，你必须使用 Tailwind CSS 重新编译样式。从项目根目录运行以下命令:
    ```bash
    npx tailwindcss -i ./themes/hugo-narrow/assets/css/main.css -o ./themes/hugo-narrow/assets/css/compiled.css
    ```

6.  **重启服务**: 如果 Hugo 服务正在运行，请重启它以查看更改。

## 部署

该网站已配置为在 Vercel 上部署。将更改推送到 `main` 分支将触发自动部署。

## 推送到 GitHub

要将您的更改保存到远程仓库:

```bash
git add .
git commit -m "你的提交信息"
git push origin main
```
