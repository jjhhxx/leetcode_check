import json, os, re


def init_question_obj():
    question_dic = {}
    for meta_file in os.walk("./questions"):
        file_list = meta_file[2]
        for file_name in file_list:
            file_path = os.path.join(meta_file[0], file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                _meta = json.loads(f.read())
                if "data" in _meta.keys():
                    _meta = _meta["data"]
                problemsetQuestionListV2 = _meta["problemsetQuestionListV2"]
                _questions = problemsetQuestionListV2["questions"]
                for _question in _questions:
                    questionFrontendId = _question["questionFrontendId"]
                    titleSlug = _question["titleSlug"]
                    paidOnly = _question["paidOnly"]
                    _id = _question["id"]
                    question_dic[questionFrontendId] = {
                        "questionFrontendId": questionFrontendId,
                        "titleSlug": titleSlug,
                        "paidOnly": paidOnly,
                        "question_id": _id,
                    }

    with open("./persistence/question_obj.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(question_dic, ensure_ascii=False))

    return True


def load_question_obj():
    question_dic = json.loads(open("./persistence/question_obj.json", "r", encoding="utf-8").read())
    return question_dic


def init_code_obj():
    with open("./Go.txt", 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r"--- Start of (\d+)\.txt ---(.*?)--- End of \1\.txt ---"
    matches = re.findall(pattern, content, re.DOTALL)  # re.DOTALL让.匹配换行符

    # 构建结果字典
    code_dict = {}
    for num_str, code_content in matches:
        # 转换数字为整数，去除代码内容前后的空白字符（保留内部格式）
        code_dict[int(num_str)] = code_content.strip()

    with open("./persistence/code_obj.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(code_dict, ensure_ascii=False))


def load_code_obj():
    code_dic = json.loads(open("./persistence/code_obj.json", "r", encoding="utf-8").read())
    return code_dic


def update_code_completed(questionFrontendId):
    with open("./persistence/completed.txt", "a", encoding="utf-8") as f:
        f.writelines(questionFrontendId + "\n\n")


def update_code_failed(questionFrontendId):
    with open("./persistence/failed.txt", "a", encoding="utf-8") as f:
        f.writelines(questionFrontendId + "\n\n")


def update_code_succeeded(questionFrontendId):
    with open("./persistence/succeeded.txt", "a", encoding="utf-8") as f:
        f.writelines(questionFrontendId + "\n\n")


def update_code_errored(questionFrontendId):
    with open("./persistence/errored.txt", "a", encoding="utf-8") as f:
        f.writelines(questionFrontendId + "\n\n")


def update_code_paid(questionFrontendId):
    with open("./persistence/paidOnly.txt", "a", encoding="utf-8") as f:
        f.writelines(questionFrontendId + "\n\n")


def load_completed():
    questionFrontendId_list = []
    with open("./persistence/completed.txt", "r", encoding="utf-8") as f:
        _metas = f.readlines()
        for _meta in _metas:
            if not _meta or _meta == "\n":
                continue
            questionFrontendId_list.append(_meta.strip())

    return questionFrontendId_list

