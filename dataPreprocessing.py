import xml.etree.cElementTree as ET
import pandas as pd


def semeval_rest_xml2csv():
    # 处理SemEval 2014 restaurant数据
    #
    #
    xml_path = "datasets/SemEval-2014/"
    test_tree = ET.parse(xml_path + "Restaurants_Test.xml")
    test_root = test_tree.getroot()
    test_data = []
    train_tree = ET.parse(xml_path + "Restaurants_Train.xml")
    train_root = train_tree.getroot()
    train_data = []
    f = open(xml_path + "Restaurants_all.txt", "w")
    for sentence in test_root.findall("sentence"):
        text = sentence.find("text").text
        f.write(text + "\r\n")
        aspect_categories = sentence.find("aspectCategories")
        for aspect_category in aspect_categories.findall("aspectCategory"):
            category = aspect_category.get("category")
            polarity = aspect_category.get("polarity")
            test_data.append((text, category, polarity))
    df_test = pd.DataFrame(test_data, columns=["text", "category", "polarity"])
    df_test = df_test[df_test["polarity"].isin(['positive', 'negative', 'neutral'])]
    df_test["polarity"] = df_test["polarity"].map({'positive': 1, 'neutral': 0, 'negative': -1})
    df_test["category"] = df_test["category"].map({"food": 0, "service": 1, "ambience": 3,
                                        "anecdotes/miscellaneous": 4, "price": 5})
    print(df_test.shape)
    df_test.to_csv(xml_path + "Restaurants_Test.csv")
    for sentence in train_root.findall("sentence"):
        text = sentence.find("text").text
        f.write(text + "\r\n")
        aspect_categories = sentence.find("aspectCategories")
        for aspect_category in aspect_categories.findall("aspectCategory"):
            category = aspect_category.get("category")
            polarity = aspect_category.get("polarity")
            train_data.append((text, category, polarity))
    df_train = pd.DataFrame(train_data, columns=["text", "category", "polarity"])
    df_train = df_train[df_train["polarity"].isin(['positive', 'negative', 'neutral'])]
    df_train["polarity"] = df_train["polarity"].map({'positive': 1, 'neutral': 0, 'negative': -1})
    df_train["category"] = df_train["category"].map({"food": 0, "service": 1, "ambience": 3,
                                        "anecdotes/miscellaneous": 4, "price": 5})
    print(df_train.shape)
    df_train.to_csv(xml_path + "Restaurants_Train.csv")
    f.close()


def all_xml2csv():
    # 将所有的xml文件全部转换
    semeval_rest_xml2csv()


all_xml2csv()




