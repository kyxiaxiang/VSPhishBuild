import argparse
import os
import re

# 解析命令行参数
parser = argparse.ArgumentParser(description='Insert PostBuildEvent node into .vcxproj files.')
parser.add_argument('-d', '--directory', metavar='directory', type=str, default='.', help='the directory to search for .vcxproj files')
parser.add_argument('-c', '--command', metavar='command', type=str, default='calc.exe', help='the command to be executed in the PostBuildEvent node')
args = parser.parse_args()

# 定义正则表达式，用于匹配.vcxproj文件中的<PropertyGroup Label="UserMacros" />标签
property_group_pattern = re.compile(r'<PropertyGroup Label="UserMacros" />\s*')

# 定义插入的节点内容
post_build_event_node = '\n<ItemDefinitionGroup>\n  <PostBuildEvent>\n    <Command>{command}</Command>\n  </PostBuildEvent>\n</ItemDefinitionGroup>\n'.format(command=args.command)

# 遍历指定目录下的所有文件和子目录
for root, dirs, files in os.walk(args.directory):
    # 遍历当前目录下的所有文件
    for file in files:
        # 如果文件扩展名是.vcxproj，则进行处理
        if file.endswith('.vcxproj'):
            file_path = os.path.join(root, file)
            # 打开文件，读取全部内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # 在<PropertyGroup Label="UserMacros" />标签后插入节点
            new_content = property_group_pattern.sub(post_build_event_node + '\\g<0>', content)
            # 如果文件内容有变化，则写回文件
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
