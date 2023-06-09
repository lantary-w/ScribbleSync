# -*- coding: utf-8 -*-
# @Author  : lantary
# @Email   : lantary-w@qq.com
# @Blog    : https://lantary.cn

import os
import sys
import yaml
import click

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core.JianShu import JianShu


def read_config():
    current_path = os.path.abspath(__file__)
    root_path = os.path.dirname(os.path.dirname(current_path))
    os.chdir(root_path)

    with open('conf/config.yaml', 'r', encoding='utf-8') as f:
        r_config = yaml.safe_load(f)

    return r_config


@click.command()
@click.option('--file', '-f', help='The file you want to post.', default='F:\\Projcet\\blog\\Blog_source\\博客文章\\简书\\23.04.16_高通量测序的数据处理与分析指北(二).md')
def main(file):
    config = read_config()

    if config['jianshu']['enable']:
        jianshu = JianShu(file=file, config=config)
        jianshu.write_blog()


if __name__ == '__main__':
    main()
