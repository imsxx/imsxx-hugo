---
title: hugo-narrow主题配色定制指南：从零到一，避开这些坑
date: 2025-07-20T21:53:19+08:00
draft: false
author: 梦随乡兮
slug: "hugo-theme-color-customization-guide"
tags: 
- Hugo
- Web开发
- 主题定制
- TailwindCSS
categories: ["建站"]
---

## 前言

最近我开始使用 Hugo 搭建自己的博客，并选择了一款名为 `hugo-narrow` 的主题。这款主题简洁、美观，但在个性化方面，我希望能拥有自己独特的配色方案。于是，我踏上了为 `hugo-narrow` 主题定制配色方案的旅程。作为一个 Hugo 新手，我遇到了不少问题，也踩了不少坑。在这篇文章里，我将分享我如何为 `hugo-narrow` 主题创建一套名为 `yuqi` 的自定义配色，并总结一些新手容易遇到的问题，希望能帮助你少走弯路。

值得一提的是，这套 `yu7` 配色方案的灵感，来源于小米 YU7 的宝石绿，我非常喜欢这款颜色的质感，希望能在我的博客上复现类似的感觉。

你可以在这里找到 `hugo-narrow` 主题的官方仓库：[https://github.com/tom2almighty/hugo-narrow](https://github.com/tom2almighty/hugo-narrow){target="_blank"}。

## 为什么需要自定义配色？

`hugo-narrow` 主题自带了多种配色方案，例如 `light`, `dark`, `bumblebee` 等。这些配色方案已经非常出色，但如果你像我一样，希望博客能更具特色，那么自定义一套专属配色就非常有必要了。

## 定制配色的第一步：创建 `custom` 文件夹

在 `hugo-narrow` 主题中，为了方便用户进行自定义，开发者预留了 `assets/css/custom` 目录。我们所有的自定义样式都应该放在这里。这样做的好处是，当主题更新时，我们的自定义文件不会被覆盖。

所以，第一步是在 `themes/hugo-narrow/assets/css/` 目录下创建一个名为 `custom` 的文件夹。

## 创建你的配色文件

接下来，在 `custom` 文件夹中，我创建了一个名为 `yu7.css` 的文件。这个文件将用来定义我自己的配色方案。文件内容如下：

```css
[data-theme="yu7"] {
  --color-primary: oklch(0.65 0.19 150); /* 深翠绿色 */
  --color-primary-foreground: oklch(0.98 0.007 150);
  --color-secondary: oklch(0.70 0.11 130); /* 草地/树林绿 */
  --color-secondary-foreground: oklch(0.98 0.007 150);
  --color-accent: oklch(0.88 0.02 150); 
  --color-accent-foreground: oklch(0.45 0.02 150);
  --color-background: oklch(0.97 0.01 150); /* 浅灰中带一点绿 */
  --color-foreground: oklch(0.22 0.03 150); /* 深绿文字 */
  --color-muted: oklch(0.88 0.02 150);
  --color-muted-foreground: oklch(0.45 0.02 150);
  --color-border: oklch(0.80 0.015 150);
  --color-card: oklch(0.96 0.01 150);
  --color-card-foreground: oklch(0.22 0.03 150);
  --color-popover: oklch(0.95 0.01 150);
  --color-popover-foreground: oklch(0.22 0.03 150);

  /* Notes */
  --color-note: oklch(0.70 0.12 240);     /* 蓝调提示 */
  --color-tip: oklch(0.70 0.13 160);      /* 草绿提示 */
  --color-important: oklch(0.70 0.15 30); /* 烈日黄棕 */
  --color-warning: oklch(0.75 0.17 85);   /* 阳光橙 */
  --color-caution: oklch(0.65 0.18 25);   /* 土色警示 */
}

[data-theme="yu7"].dark {
  --color-primary: oklch(0.72 0.20 150); /* 深翠绿色更亮一阶 */
  --color-primary-foreground: oklch(0.15 0.035 150);
  --color-secondary: oklch(0.65 0.13 130);
  --color-secondary-foreground: oklch(0.16 0.03 130);
  --color-accent: oklch(0.34 0.025 150);   
  --color-accent-foreground: oklch(0.84 0.01 150);
  --color-background: oklch(0.24 0.03 150); /* 夜间深绿背景，保留第一版 */
  --color-foreground: oklch(0.96 0.01 150); /* 高对比文字色 */
  --color-muted: oklch(0.34 0.025 150);
  --color-muted-foreground: oklch(0.84 0.01 150);
  --color-border: oklch(0.38 0.03 150);
  --color-card: oklch(0.26 0.025 150);
  --color-card-foreground: oklch(0.96 0.01 150);
  --color-popover: oklch(0.34 0.025 150);
  --color-popover-foreground: oklch(0.96 0.01 150);

  /* Notes */
  --color-note: oklch(0.72 0.14 240);
  --color-tip: oklch(0.74 0.12 160);
  --color-important: oklch(0.75 0.16 30);
  --color-warning: oklch(0.78 0.17 85);
  --color-caution: oklch(0.68 0.18 25);
}
```

这里我定义了一个名为 `yu7` 的配色方案，并分别为亮色模式和暗色模式设置了不同的颜色变量。

## 关键一步：编译 CSS

创建完配色文件后，我天真地以为刷新浏览器就能看到效果。然而，什么都没有发生。这就是我遇到的第一个大坑：**`hugo-narrow` 主题使用了 Tailwind CSS 框架，所有 CSS 文件都需要经过编译才能生效。**

**为什么需要编译？**

Tailwind CSS 是一个“功能优先”的 CSS 框架，它通过扫描你的 HTML、JavaScript 和其他模板文件，按需生成最终的 CSS 文件。这样做的好处是，最终生成的 CSS 文件体积非常小，只包含你用到的样式，从而大大提升了网站的加载速度。

我们的 `yu7.css` 文件虽然定义了颜色变量，但需要通过 Tailwind CSS 的构建过程，将这些变量应用到主题的各个组件中，并与其他样式一起打包成一个最终的 `compiled.css` 文件。浏览器实际加载的是这个编译后的文件。

**如何编译？**

在项目根目录下，运行以下命令：

```bash
npx tailwindcss -i ./themes/hugo-narrow/assets/css/main.css -o ./themes/hugo-narrow/assets/css/compiled.css
```

这个命令会读取 `main.css`（它导入了我们的 `yu7.css`），然后通过 Tailwind CSS 处理，最终输出到 `compiled.css`。

## 启用新主题

编译完成后，还需要在 Hugo 的配置文件 `hugo.toml` 中启用我们的新主题。在 `[params]` 部分，找到 `colorScheme` 配置项，将其值改为我们定义的配色方案名称 `yu7`。

```toml
[params]
    # ... 其他配置
    colorScheme = "yu7"
```

现在，重启 Hugo 服务器，你就能看到全新的配色方案了！

## 总结与避坑指南

回顾整个过程，我总结了以下几点经验，希望能帮助 Hugo 新手们：

1.  **自定义优于直接修改：** 尽量将你的自定义代码（如 CSS、HTML 布局）放在指定的位置（如 `assets/css/custom/`），而不是直接修改主题文件。这样可以避免在主题更新时丢失你的修改。

2.  **理解构建过程：** 很多现代主题都使用了前端构建工具（如 Tailwind CSS、Sass）。如果你发现修改了文件却没有效果，首先要检查是否需要执行编译或构建步骤。

3.  **查看主题文档：** 在开始定制之前，花点时间阅读主题的文档。通常文档会说明如何进行自定义、需要哪些依赖以及构建命令是什么。

4.  **利用 Hugo 的模板系统：** Hugo 强大的模板系统允许你覆盖主题的任何部分。例如，你可以在项目根目录的 `layouts/` 文件夹下创建同名文件来覆盖主题的布局文件，而无需修改主题本身。

希望这篇分享能让你在定制 Hugo 主题的道路上更加顺利。享受创造属于你自己的、独一无二的博客吧！
