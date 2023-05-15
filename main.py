'''
Description: 
Version: 1.0
Author: Glenn
Email: chenluda01@outlook.com
Date: 2023-05-15 14:07:20
FilePath: \17-zhuhu2mdWeb\pdf.py
Copyright (c) 2023 by Kust-BME, All Rights Reserved. 
'''
import PyPDF2
import pikepdf
from tqdm import tqdm
import os

import os
import pikepdf
from tqdm import tqdm

def crack_pdf_password(input_file, dictionary_folder):
    """
    使用字典破解PDF密码
    """
    # 遍历字典文件夹
    for root, _, files in os.walk(dictionary_folder):
        for file in files:
            # 获取子字典文件的路径
            dictionary_file = os.path.join(root, file)
            # 打开子字典文件
            with open(dictionary_file, 'r', encoding='utf-8') as dict_file:
                # 读取密码列表
                passwords = dict_file.readlines()
                
            # 尝试每个密码
            for password in tqdm(passwords, desc='正在尝试密码'):
                try:
                    # 使用密码尝试打开 PDF
                    with pikepdf.open(input_file, password=password.strip()) as pdf:
                        print(f"\n找到密码：{password.strip()}")
                        return password
                except pikepdf.PasswordError as e:
                    pass

def remove_pdf_password(input_file, output_file, dictionary_folder):
    """
    移除 PDF 文件的密码保护
    """
    try:
        with open(input_file, 'rb') as file:
            # 创建PDF阅读器对象
            pdf_reader = PyPDF2.PdfReader(file)

            # 检查是否有密码
            if pdf_reader.is_encrypted:
                print("PDF 文件受到密码保护。")
                print("尝试使用空密码进行解密...")
                
                # 尝试使用空密码解密，若改PDF文件仅是在编辑时需要密码，则这一步即可去密
                if pdf_reader.decrypt(''):
                    print("解密成功。")
                else:
                    print("解密失败。尝试字典破解...")
                    password = crack_pdf_password(input_file, dictionary_folder)
                    pdf_reader.decrypt(password)

            # 创建一个PDF编写器对象
            pdf_writer = PyPDF2.PdfWriter()

            # 将每一页添加到PDF编写器对象
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)

            # 将解密的PDF内容写入新文件
            with open(output_file, 'wb') as output:
                pdf_writer.write(output)

        print(f"解密成功，已生成新文件：{output_file}")

    except Exception as e:
        print(f"发生错误：{e}")

def set_encrypt_pdf(input_file, output_file, password):
    """
    为PDF文件添加密码保护
    """
    try:
        # 创建 PDF 文件读取器对象
        pdf_reader = PyPDF2.PdfReader(input_file)

        # 检查是否已加密
        if pdf_reader.is_encrypted:
            print("PDF 文件已受到密码保护。")
            return
        
        # 创建一个PDF编写器对象
        pdf_writer = PyPDF2.PdfWriter()

        # 将每一页添加到PDF编写器对象
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

        # 为 PDF 文件添加密码
        pdf_writer.encrypt(password)

        # 将加密后的 PDF 内容写入新文件
        with open(output_file, 'wb') as output:
            pdf_writer.write(output)

        print(f"成功加密 PDF 文件，已生成新文件：{output_file}")

    except Exception as e:
        print(f"发生错误：{e}")


if __name__ == '__main__':

    input_file = 'test.pdf'  # 替换为输入的PDF文件名
    output_file = 'test_add_password.pdf'  # 替换为输出的PDF文件名
    password = "123456"
    # 为PDF文件添加密码保护
    set_encrypt_pdf(input_file, output_file, password)

    dictionary_folder = './password_brute_dictionary'
    input_file = 'test_add_password.pdf'  # 替换为输入的PDF文件名
    output_file = 'test_remove_password.pdf'  # 替换为输出的PDF文件名
    # 移除 PDF 文件的密码保护
    remove_pdf_password(input_file, output_file, dictionary_folder)
