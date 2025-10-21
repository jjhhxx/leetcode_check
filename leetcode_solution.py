import requests, json
import brotli, time
from load_obj import (
    load_question_obj,
    load_code_obj,
    update_code_completed,
    update_code_failed,
    update_code_succeeded,
    update_code_errored,
    update_code_paid,
    load_completed
)


def submit_code(cookie, x_csrftoken, questionFrontendId, titleSlug, code):
    # 请求URL
    url = f"https://leetcode.cn/problems/{titleSlug}/submit/"
    print(url)

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "connection": "keep-alive",
        "content-type": "application/json",
        # 替换为你自己的cookie（时效性，需从浏览器中获取当前有效的值）
        "cookie": cookie,
        "host": "leetcode.cn",
        "origin": "https://leetcode.cn",
        "referer": f"https://leetcode.cn/problems/{titleSlug}/",
        "sec-ch-ua": '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        "x-csrftoken": x_csrftoken
    }

    # 构建请求体（LeetCode提交格式，需根据实际情况调整）
    # 两数之和的question_id为1，语言为python3，代码为解题逻辑
    payload = {
        "lang": "golang",
        "question_id": f"{questionFrontendId}",
        "typed_code": code,
    }

    # 发送POST请求
    response = requests.post(
        url=url,
        headers=headers,
        json=payload  # 自动序列化JSON并设置Content-Type为application/json
    )

    # 打印响应结果
    print("响应状态码：", response.status_code)
    print("响应：", response.text)
    return response.json()["submission_id"]


def get_submit_status(cookie, x_csrftoken, titleSlug, submission_id):
    submit_id = submission_id
    # 状态查询URL：将submit_id嵌入到URL路径中
    url = f"https://leetcode.cn/submissions/detail/{submit_id}/check/"

    # 2. 构建请求头：复制所有提供的头信息，关键字段（cookie、x-csrftoken）需保持有效
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "connection": "keep-alive",
        "content-type": "application/json",  # 虽为GET请求，但保留浏览器原头信息以避免反爬
        # 替换为你自己的有效cookie（时效性，失效后需从浏览器重新获取）
        "cookie": cookie,
        "host": "leetcode.cn",
        "referer": f"https://leetcode.cn/problems/{titleSlug}/description/",
        "sec-ch-ua": '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        # 替换为你自己的有效x-csrftoken（从cookie或浏览器请求头中提取）
        "x-csrftoken": x_csrftoken
    }

    response = requests.get(
        url=url,
        headers=headers,
        timeout=10  # 设置超时时间，避免长期阻塞
    )
    print(response.status_code)
    response.raise_for_status()  # 若状态码非200，抛出HTTP错误
    submit_status = response.json()
    return submit_status


def get_submit_result(cookie, x_csrftoken, titleSlug, submission_id):
    submit_id = submission_id
    # 状态查询URL：将submit_id嵌入到URL路径中
    url = f"https://leetcode.cn/graphql/"

    # 2. 构建请求头：复制所有提供的头信息，关键字段（cookie、x-csrftoken）需保持有效
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "connection": "keep-alive",
        "content-type": "application/json",  # 虽为GET请求，但保留浏览器原头信息以避免反爬
        # 替换为你自己的有效cookie（时效性，失效后需从浏览器重新获取）
        "cookie": cookie,
        "host": "leetcode.cn",
        "referer": f"https://leetcode.cn/problems/{titleSlug}/description/",
        "sec-ch-ua": '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        # 替换为你自己的有效x-csrftoken（从cookie或浏览器请求头中提取）
        "x-csrftoken": x_csrftoken
    }
    payload = {
      "query": "\n    query submissionDetails($submissionId: ID!) {\n  submissionDetail(submissionId: $submissionId) {\n    code\n    timestamp\n    statusDisplay\n    isMine\n    runtimeDisplay: runtime\n    memoryDisplay: memory\n    memory: rawMemory\n    lang\n    langVerboseName\n    question {\n      questionId\n      titleSlug\n      hasFrontendPreview\n    }\n    user {\n      realName\n      userAvatar\n      userSlug\n    }\n    runtimePercentile\n    memoryPercentile\n    submissionComment {\n      flagType\n    }\n    passedTestCaseCnt\n    totalTestCaseCnt\n    fullCodeOutput\n    testDescriptions\n    testInfo\n    testBodies\n    stdOutput\n    ... on GeneralSubmissionNode {\n      outputDetail {\n        codeOutput\n        expectedOutput\n        input\n        compileError\n        runtimeError\n        lastTestcase\n      }\n    }\n    ... on ContestSubmissionNode {\n      outputDetail {\n        codeOutput\n        expectedOutput\n        input\n        compileError\n        runtimeError\n        lastTestcase\n      }\n    }\n  }\n}\n    ",
      "variables": {
        "submissionId": submission_id
      },
      "operationName": "submissionDetails"
    }

    response = requests.get(
        url=url,
        headers=headers,
        json=payload,
        timeout=10  # 设置超时时间，避免长期阻塞
    )
    print(response.status_code)
    return response.json()


if __name__ == '__main__':
    cookie = ""
    x_csrftoken = ""

    question_obj, code_obj = load_question_obj(), load_code_obj()
    completed_obj = load_completed()
    counts = 0

    for i in list(code_obj.keys()):
        # 已完成
        if i in completed_obj:
            continue
        # 账户提交次数限制
        if counts >= 500:
            break
        code = code_obj[i]
        try:
            questionFrontendId, titleSlug, paidOnly, question_id = question_obj[i]["questionFrontendId"], question_obj[i]["titleSlug"], question_obj[i]["paidOnly"], question_obj[i]["question_id"]
            # 付费
            if paidOnly:
                update_code_paid(questionFrontendId)
                continue
            time.sleep(5)
            print(f"Will submit code for {i} and check!")
            submission_id = submit_code(cookie, x_csrftoken, question_id, titleSlug, code)
            counts += 1
            print(submission_id)
            time.sleep(10)
            update_code_completed(questionFrontendId)

            submit_result = get_submit_result(cookie, x_csrftoken, titleSlug, submission_id)
            if submit_result["data"]["submissionDetail"]["statusDisplay"] != "Accepted":
                update_code_failed(questionFrontendId)
            else:
                update_code_succeeded(questionFrontendId)
        except Exception as e:
            print(e)
            update_code_errored(i)

