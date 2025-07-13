#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理Hugo文章中的WordPress特有front matter属性
"""

import os
import re
import glob

# WordPress特有的front matter属性列表
wordpress_attributes = [
    'type',
    'featured_image', 
    'views',
    'like',
    'b2_vote',
    'zrz_favorites',
    '日志头图',
    'bigfa_ding'
]

def clean_frontmatter(file_path):
    """清理单个文件的front matter"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 使用正则表达式匹配和删除WordPress属性
    for attr in wordpress_attributes:
        # 匹配单行属性（如 type: post）
        pattern1 = rf'^{re.escape(attr)}:.*$'
        content = re.sub(pattern1, '', content, flags=re.MULTILINE)
        
        # 匹配多行属性（如 views: 后跟 - 1911）
        pattern2 = rf'^{re.escape(attr)}:\s*\n(^- .*$\n?)*'
        content = re.sub(pattern2, '', content, flags=re.MULTILINE)
    
    # 清理孤立的数组值行（以 - 开头且前面是空行）
    content = re.sub(r'\n\n- .*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^- .*$\n', '', content, flags=re.MULTILINE)
    
    # 清理多余的空行
    content = re.sub(r'\n\n+', '\n\n', content)
    content = re.sub(r'\n+---', '\n---', content)
    
    # 如果内容有变化，写回文件
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    """主函数"""
    posts_dir = 'f:/TraeWeb/imsxx-hugo/imsxx-hugo/content/posts'
    
    # 获取所有markdown文件
    md_files = glob.glob(os.path.join(posts_dir, '*.md'))
    
    cleaned_count = 0
    
    for file_path in md_files:
        try:
            if clean_frontmatter(file_path):
                print(f'已清理: {os.path.basename(file_path)}')
                cleaned_count += 1
        except Exception as e:
            print(f'处理文件 {os.path.basename(file_path)} 时出错: {e}')
    
    print(f'\n清理完成！共处理了 {cleaned_count} 个文件。')
    print('\n已删除的WordPress属性:')
    for attr in wordpress_attributes:
        print(f'  - {attr}')

if __name__ == '__main__':
    main()