import xml.etree.cElementTree as ET
import pandas as pd


def text_process(text):
    # 全部转换成小写
    # 对一些标点符号和单词挨着的情况做个分割
    text = text.lower()
    text = text.replace(".", " .")
    text = text.replace("(", "( ")
    text = text.replace(",", " ,")
    text = text.replace(")", " )")
    text = text.replace(":", " :")
    text = text.replace("!", " !")
    text = text.replace("?", " ?")
    text = text.replace("  ", " ")
    return text
def xml2csv(xml_path, filename, category_map):

    tree = ET.parse(xml_path+filename + ".xml")
    root = tree.getroot()
    data = []
    f = open(xml_path + "data_all.txt", "a+")
    for sentence in root.findall("sentence"):
        text = sentence.find("text").text
        text = text_process(text)
        print(text)
        f.write(text + "\r\n")
        aspect_categories = sentence.find("aspectCategories")
        for aspect_category in aspect_categories.findall("aspectCategory"):
            category = aspect_category.get("category")
            polarity = aspect_category.get("polarity")
            data.append((text, category, polarity))
    df = pd.DataFrame(data, columns=["text", "category", "polarity"])
    df = df[df["polarity"].isin(["positive", "negative", "neutral"])]
    df["polarity"] = df["polarity"].map({"positive": 1, "neutral": 0, "negative": -1})
    df["category"] = df["category"].map(category_map)
    print(df.shape)
    df.to_csv(xml_path + filename + ".csv")
    f.close()


def semeval_rest_xml2csv():
    # 处理SemEval 2014 restaurant数据
    # csv文件用来训练和测试，每一条数据每一个category都进行了拆分
    # txt文件包含训练集和测试集，用来生成glove词向量
    # 把情感极性映射为{"positive": 1, "neutral": 0, "negative": -1}
    # 把方面类别映射为{"food": 0, "service": 1, "ambience": 3,
    #                                         "anecdotes/miscellaneous": 4, "price": 5}
    category_map = {"food": 0, "service": 1, "ambience": 3,
                                             "anecdotes/miscellaneous": 4, "price": 5}
    semeval_train_xml_path = "datasets/SemEval-2014/"
    xml2csv(semeval_train_xml_path, "Restaurants_Train", category_map)
    semeval_test_xml_path = "datasets/SemEval-2014/"
    xml2csv(semeval_test_xml_path, "Restaurants_Test", category_map)


def mams_acsa_xml2csv():
    category_map = {"place": 0, "food": 1, "service": 2,
                    "menu": 3, "staff": 4, "miscellaneous": 5,  "price":6 }
    mams_train_xml_path = "datasets/MAMS-ACSA/raw/"
    xml2csv(mams_train_xml_path, "train", category_map)
    mams_test_xml_path = "datasets/MAMS-ACSA/raw/"
    xml2csv(mams_test_xml_path, "test", category_map)
    mams_val_xml_path = "datasets/MAMS-ACSA/raw/"
    xml2csv(mams_val_xml_path, "val", category_map)



def all_xml2csv():
    # 将所有的xml文件全部转换
    semeval_rest_xml2csv()
    mams_acsa_xml2csv()


all_xml2csv()

# TODO :word to glove vector
# TODO :nitian_nlp_task
# TODO:




