from language_detection import Language_Detection
import argparse
import json

'''
Command list :
    help about the commands:
        python3 P1_01_script.py -t "<your text>" -i "<:id>" -h

    get api's raw json response :
        python3 P1_01_script.py -t "<your text>" -i "<:id>" -j

    get api's raw json response, but prettified :
        python3 P1_01_script.py -t "<your text>" -i "<:id>" -p

    get only the name of the detected language :
        python3 P1_01_script.py -t "<your text>" -i "<:id>" -n
    
    get only the ISO 639-1 name :
        python3 P1_01_script.py -t "<your text>" -i "<:id>" -I
'''


def main():

    parser = argparse.ArgumentParser(description="detects the language of a text using Azure's Text Analytics service")
    
    requiredNamed = parser.add_argument_group("required named arguments")
    requiredNamed.add_argument("-t", 
                        "--text", 
                        help="the text whose language you want to recognize", 
                        required=True)
    
    parser.add_argument("-i", 
                        "--id", 
                        help="the id of the text")
    
    parser.add_argument("-j", 
                        "--json",
                        help="use this flag if you want json output", 
                        action="store_true")
    
    parser.add_argument("-n", 
                        "--name", 
                        help="use this flag if you want the name of the detected language",
                        action="store_true")
    
    parser.add_argument("-I", 
                        "--iso", 
                        help="use this flag if you want the ISO 639-1 standard language code. For more informations about these codes, visit https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes", 
                        action="store_true")
    
    parser.add_argument("-p", 
                        "--pretty", 
                        help="pretty output :-)", 
                        action="store_true")
    
    
    args = parser.parse_args()
    
    if(args.id is None):
            args.id = "1"
            
    if(args.json or (not args.iso and not args.pretty and not args.name)):
        lang = Language_Detection().detect(args.text, args.id)
        print(lang)
        
    if(args.name):
        name = Language_Detection().get_language_name(args.text, args.id)
        print(name)
        
    if(args.iso):
        iso_name = Language_Detection().get_language_iso(args.text, args.id)
        print(iso_name)
        
    if(args.pretty):
        lang = Language_Detection().detect(args.text, args.id)
        lang = json.loads(lang)
        lang = lang["documents"][0]["detectedLanguage"]
        print("detected language name : {}".format(lang["name"]))
        print("ISO 639-1 : {}".format(lang["iso6391Name"]))
        print("confidence score : {}".format(lang["confidenceScore"]))

    
    

if __name__ == "__main__":
    main()