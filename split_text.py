import os
from tqdm import tqdm

def split_text_by_blank_lines(text):
    """
    根据空行拆分文本，返回拆分后的字符串列表。
    如果需要更复杂的空白行处理逻辑，可以在此函数中定制。
    """
    # 将所有换行符 '\r\n' 替换为 '\n' 并去除首尾空格
    normalized_text = text.replace('\r\n', '\n').strip()
    # 以空行（\n\n）为分割标识拆分，并过滤掉可能的空段
    chunks = [chunk.strip() for chunk in normalized_text.split('\n\n') if chunk.strip()]
    return chunks

def process_txt_files(input_folder, output_folder):
    """
    遍历 input_folder 下的所有 .txt 文件，按空行拆分后，
    将结果写入 output_folder 文件夹中，每段生成一个新文件。
    """
    # 确保输出文件夹存在，否则自动创建
    os.makedirs(output_folder, exist_ok=True)

    # 遍历文件夹内所有文件
    for filename in tqdm(os.listdir(input_folder)):
        if filename.lower().endswith('.txt'):
            # 构造输入文件的完整路径
            input_file_path = os.path.join(input_folder, filename)
            
            # 读取文件内容
            with open(input_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 拆分
            chunks = split_text_by_blank_lines(content)
            
            # 获取文件名去掉后缀部分，用于输出命名
            file_basename = os.path.splitext(filename)[0]
            
            # 将拆分后的每部分写入新的文件
            for idx, chunk in enumerate(chunks, start=1):
                # 命名：原文件名 + "_" + 序号 + ".txt"
                new_filename = f"{file_basename}_{idx}.txt"
                new_file_path = os.path.join(output_folder, new_filename)
                
                # 将 chunk 写入新的 txt 文件
                with open(new_file_path, 'w', encoding='utf-8') as out_f:
                    out_f.write(chunk)

def main():
    # 输入文件夹
    attraction_input = 'data/wiki/attraction'
    city_input = 'data/wiki/city'
    
    # 输出文件夹
    attraction_output = 'data/wiki/attraction_split'
    city_output = 'data/wiki/city_split'
    
    # 处理
    process_txt_files(attraction_input, attraction_output)
    process_txt_files(city_input, city_output)

if __name__ == '__main__':
    main()
