#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复Hugo文章中空的categories和tags字段
"""

import os
import re
import glob

def fix_empty_fields(file_path):
    """修复单个文件的空categories和tags字段"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 删除空的categories和tags行
    content = re.sub(r'^categories:\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^tags:\s*$', '', content, flags=re.MULTILINE)
    
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
    
    fixed_count = 0
    
    for file_path in md_files:
        try:
            if fix_empty_fields(file_path):
                print(f'已修复: {os.path.basename(file_path)}')
                fixed_count += 1
        except Exception as e:
            print(f'处理文件 {os.path.basename(file_path)} 时出错: {e}')
    
    print(f'\n修复完成！共处理了 {fixed_count} 个文件。')
    print('已删除空的categories和tags字段。')

if __name__ == '__main__':
    main()