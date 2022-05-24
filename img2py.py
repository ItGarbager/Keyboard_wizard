import base64
import os


def pic_to_py(filename):
    """
    将图像文件转换为py文件
    :param filename:
    :return:
    """
    with open(os.path.join('images', filename), "rb") as f:
        read_pic = f.read()

    b64str = base64.b64encode(read_pic)
    key = 'img_' + filename.replace('.', '_')
    write_data = key + " = " + '"' + b64str.decode("utf-8") + '"\n'
    print(write_data)

    write_path = os.path.join('images', 'var.py')
    with open(write_path, "a") as f:
        f.write(write_data)


if __name__ == '__main__':
    for file in os.listdir('images'):
        if file.endswith('png'):
            pic_to_py(file)
