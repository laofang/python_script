import json

QUESTION_TYPE = { "JUDGE":"0","CHOICE":"1"}

# 从文本中获取将选择题与判断题构造成字符串，并返回包含这些字符串的列表
def getSubjectList(fileName):
    object = open(fileName,"r",-1,encoding="ansi")
    lines = object.readlines()
    lineSize = len(lines)
    resultList = []
    for i in range(0,lineSize):
        line = str(lines[i])
        if line.find("、") != -1 and line[0:line.index("、")].strip().isdigit():
            tempStr = line
            j = i + 1
        
            while j < lineSize:
                if(lines[j].find("、") != -1 and lines[j][0:lines[j].index("、")].strip().isdigit()):
                    i = j
                    break       
                
                # if lines[j].find("、") != -1 and not lines[j][0:lines[j].index("、")].strip().isdigit() and not lines[j][0:lines[j].index("、")].strip().encode("utf-8").isalpha():
                #     i = j
                #     break
                
                if lines[j].find("、") != -1 and lines[j][0:lines[j].index("、")].strip().encode("utf-8").isalpha():
                    tempStr = tempStr + "|" + lines[j]               
                else:
                    tempStr = tempStr + lines[j]
                j = j + 1
            if j >= lineSize:
                tempStr = tempStr.replace("\t","")
                tempStr = tempStr.replace("\n","")
                resultList.append(tempStr.strip())
                break
            else:
                tempStr = tempStr.replace("\t","")
                tempStr = tempStr.replace("\n","")
                resultList.append(tempStr.strip())              

    object.close()
    return resultList



def getQuestionType(question):
    if str(question).find("√") != -1 or str(question).find("×") != -1:
        return QUESTION_TYPE["JUDGE"]
    else:
        return QUESTION_TYPE["CHOICE"]



def parseChoice(id,choice):
    lis = choice.split("|")
    result = {}
    stem = lis[0]
    lis = lis[1:]
    anwserTitles = list(stem[stem.find("（")+1:stem.find("）")].strip())
    stem = stem.replace("(","（")
    stem = stem.replace(")","）")
    stem = stem[stem.find("、")+1:stem.find("（")+1]+stem[stem.find("）"):]
    
    anwserContent = ""
    options = []
    anwser = []
    for option in lis:
        index = option.find("、")
        title = option[0:index].strip()
        content = option[index+1:].strip()
        optionTemp = {"title":title,"content":content}
        options.append(optionTemp)
        for anwserTitle in anwserTitles:
            if anwserTitle == title:
                anserTemp = {"title":title,"content":content}
                anwser.append(anserTemp)

        result["options"] = options
    result["id"] = id
    result["stem"] = stem
    result["anwser"] = anwser
    return result


def parseJudge(id,judge):
    id = id

lis = getSubjectList("demoM.txt")

result = []
count = 1
for temp  in lis:
    if getQuestionType(temp) == QUESTION_TYPE["CHOICE"]:
        result.append(parseChoice(count,str(temp)))
        count = count + 1


#print(json.dumps(parseChoice(1,result),ensure_ascii=False))

text = open("m.json","w",-1,"utf-8")
text.write(json.dumps(result,ensure_ascii=False))