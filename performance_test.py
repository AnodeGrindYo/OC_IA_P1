from language_detection import Language_Detection
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns


# langs = ["English", "Chinese", "Chinese Simplified", "Chinese Traditional", "Hindi", "Spanish", "French"]
langs = ["English", "Chinese", "Standard Chinese", "Literary Chinese", "Hindi", "Spanish", "French"]


base_dir = "./data"
labels_file = base_dir + "/labels.csv"
x_test_file = base_dir + "/x_test.txt"
y_test_file = base_dir + "/y_test.txt"

labels_df = pd.read_csv(labels_file, sep=";")

# récupère les labels utilisés dans y_train.txt et y_test.txt
lang_labels = list(labels_df[labels_df['English'].isin(langs)]['Label'])
# print(lang_labels)

lang_names = (list(labels_df[labels_df['English'].isin(langs)]['English']))
# print(lang_names)

def read_file(x_file, y_file):
    # Récupère le contenu de  'y_file' dans un dataframe
    y_df = pd.read_csv(y_file, header=None)
    # y_df a une seule colonne qui s'appelera "labels"
    y_df.columns = ["Label"]
    
    # Récupère le contenu de 'x_file' dans une liste de strings
    with open(x_file, encoding="utf8") as f:
        x_pars = f.readlines()
    
    # Enlève les espaces et autres caractères invisibles (comme '\n') au début et à la fin des strings
    x_pars = [t.strip() for t in x_pars]
    # Convertit la liste en dataframe avec une colonne "Paragraph"
    x_df = pd.DataFrame(x_pars, columns=['Paragraph']) 
    # Ne garde que les paragraphes des langues connues (et enlève les autres)
    x_df = x_df[y_df['Label'].isin(lang_labels)]
    # Ne garde que ces langues dans lang_labels
    y_df = y_df[y_df['Label'].isin(lang_labels)]
    
    return (x_df, y_df)

def verify_predictions():
    # structure du résultat des tests : paragraphe, expected, predicted, confidence score, valid
    lang_df, label_df = read_file(x_test_file, y_test_file)
    
    test_results = []
    for i in lang_df.index:
        valid = False
        lang_par = lang_df["Paragraph"][i]
        if(len(lang_par) > 5120):
            lang_par = lang_par[:5119]
        lbl = label_df["Label"][i]
        lang_name = labels_df.loc[labels_df["Label"] == lbl, "English"].iloc[0]
        api_res = json.loads(Language_Detection().detect(lang_par, str(i)))
        predicted_lang_name = api_res["documents"][0]["detectedLanguage"]["name"]
        confidenceScore = api_res["documents"][0]["detectedLanguage"]["confidenceScore"]
        if(lang_name == predicted_lang_name):
            valid = True
        print(api_res["documents"][0]["detectedLanguage"])
        test_results.append([lang_par, lang_name, predicted_lang_name, confidenceScore, valid])
    # print(test_results)
    df_test_results = pd.DataFrame(test_results, columns=["paragraphs", "expected", "predicted","confidenceScore", "valid"])
    return df_test_results


def verif_predictions():
    # structure du resultat des tests : paragraphe, expected, predicted, confidence score, valid
    lang_df, label_df = read_file(x_test_file, y_test_file)
    lang_df.index.name = "id"
    label_df.index.name = "id"
    last_index = lang_df.index[-1]
    max_doc_amount = Language_Detection().MAX_DOC_AMOUNT
    max_txt_size = Language_Detection().MAX_TXT_SIZE
    test_results = []
    doc_amount = 0
    payload = {}
    payload["documents"] = []
    
    for i in lang_df.index:
        if(doc_amount < max_doc_amount):
            doc_amount += 1
        # lang par est le paragraphe de langue qui a été extrait
        lang_par = lang_df["Paragraph"][i]
        if(len(lang_par) > max_txt_size):
            lang_par = lang_par[:max_txt_size - 1]
        document = {}
        document["id"] = i
        document["text"] = lang_par
        payload["documents"].append(document)
        if((doc_amount == max_doc_amount) or (i == last_index)):
            res = json.loads(Language_Detection().call_api(json.dumps(payload)))
            print(res)
            for document in res["documents"]:
                test_results.append([document["id"], 
                                 document["detectedLanguage"]["name"], 
                                 document["detectedLanguage"]["confidenceScore"]])
            payload = {}
            payload["documents"] = []
            doc_amount= 0
            if(i == last_index):
                df_results = pd.DataFrame(test_results, columns=["id", "Predicted", "confidenceScore"])
                df_results.set_index("id", inplace=True)
                df_results.index = df_results.index.astype(int)
                
                
                df_final = pd.merge(df_results, pd.merge(lang_df, label_df, left_index=True, right_index=True), left_index=True, right_index=True)
                df_final = pd.merge(df_final, labels_df, on="Label", how="left").set_index(df_final.index)
                df_final = df_final.drop(["Wiki Code", "ISO 369-3", "German", "Language family", "Writing system", "Remarks", "Synonyms", "Label"], axis=1)
                df_final = df_final.rename(columns={"English": "Expected"})
                df_final = df_final[["Paragraph", "Predicted", "Expected", "confidenceScore"]]
                # dans le dataset wili-2018, les langues chinoises n'ont pas le même nom
                # remplaçons donc les noms des langues de la colonne "Expected" par ceux correspondants pour les langues chinoises
                df_final.replace({"Standard Chinese": "Chinese Simplified"}, regex=True)
                df_final.replace({"Literary Chinese": "Chinese Traditional"}, regex=True)
                df_final["Valid"] = (df_final["Predicted"] == df_final["Expected"])
                return df_final


def main():
    df_results = verif_predictions()
    # obtention du pourcentage de bonnes et de mauvaises prédictions :
    df_results["Valid"].value_counts(normalize=True) * 100


if __name__ == "__main__":
    main()
