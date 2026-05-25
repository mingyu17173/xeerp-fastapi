# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @Software: PyCharm

import os
import re

# 定义要添加的头部模板
HEADER_TEMPLATE = '''# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @Software: PyCharm
'''

def get_file_header(filename):
    """根据文件类型生成对应的头部注释"""
    desc_map = {
        'controller': '控制器',
        'service': '业务服务',
        'dao': '数据访问层',
        'model': '数据模型',
        'schema': '数据模式',
        'core': '核心配置',
        'utils': '工具类',
        'api': 'API模块',
        'schemas': '数据模式',
        'service': '业务服务',
        'models': '数据模型',
        'scripts': '脚本',
        'middleware': '中间件',
    }

    # 根据目录名推断描述
    desc = '模块文件'
    for key, value in desc_map.items():
        if key in filename.lower():
            desc = value
            break

    return f'''# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: {os.path.basename(filename)}
# @Software: PyCharm
# @Desc : {desc}
'''

def add_header_to_file(filepath):
    """为单个文件添加头部注释"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否已经有头部注释
        if content.startswith('# -*- coding: utf-8 -*-'):
            return False, '已有头部注释'

        # 获取文件对应的头部
        header = get_file_header(filepath)

        # 添加头部
        new_content = header + '\n' + content

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True, '成功'
    except Exception as e:
        return False, str(e)

def process_directory(root_dir):
    """处理目录下的所有Python文件"""
    count = {'success': 0, 'skip': 0, 'failed': 0}
    failed_files = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 跳过test目录
        if 'test' in dirpath or '__pycache__' in dirpath:
            continue

        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                success, msg = add_header_to_file(filepath)
                if success:
                    count['success'] += 1
                    print(f'✓ {filepath}')
                elif msg == '已有头部注释':
                    count['skip'] += 1
                else:
                    count['failed'] += 1
                    failed_files.append((filepath, msg))
                    print(f'✗ {filepath}: {msg}')

    return count, failed_files

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    else:
        root_dir = '.'

    print(f'开始处理目录: {root_dir}')
    print('-' * 50)

    count, failed_files = process_directory(root_dir)

    print('-' * 50)
    print(f'处理完成: 成功={count["success"]}, 跳过={count["skip"]}, 失败={count["failed"]}')

    if failed_files:
        print('\n失败的文件:')
        for filepath, msg in failed_files:
            print(f'  {filepath}: {msg}')
