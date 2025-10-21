# leetcode_check

代码可以调用 Leetcode 官方的提交和结果查询接口；你需要按照下面的流程进行：

- 代码某些路径是硬编码进去的，你需要修改
- pip install -r req.txt
- 上传你要校验的代码，例如 Go.txt 至根目录下（与 load_obj.py 同级）
- 执行对象初始化：
  ```python
  from load_obj import init_question_obj, init_code_obj

  init_question_obj()
  init_code_obj() # 注意修改里面的路径，硬编码进去的
  ```
- 浏览器登录你的 leetcode 账号，找到自己的 cookie 和 x-csrftoken
- 将 cookie 和 x-csrftoken 硬编码到 leetcode_solution.py 中，执行该文件即可
- 在 leetcode 上自己跑一个提交，看看自己的 user-agent；把这个值替换到 leetcode_solution.py 去
- 需要修改 leetcode_solution.py 文件中 submit_code 函数的 lang 为自己校验的语言！当前是 "lang": "golang"，在 leetcode 里面找道题目选择语言提交以下，看看传进去的参数。python 是 python3
- ./persistence/completed.txt 中是已经执行了的 id（txt 文件中的 start of xx）
- ./persistence/succeeded.txt 中是校验通过的 id（txt 文件中的 start of xx）
- ./persistence/failed.txt 中是校验不通过的 id（txt 文件中的 start of xx），基本上都是格式问题，需要修改一下提供的代码手动在官网上根据题号跑一下
- ./persistence/errored.txt 中是接口异常的 id（txt 文件中的 start of xx），检查一下是哪里有问题
- ./persistence/paidOnly.txt 中是付费的题目，不管
- leetcode_solution.py 中有两个限制需要注意，一个是 counts 限制一次跑 500 个接口，跑完建议检查一下 cookie 和 账户有没有被限制提交；限制了就换一个，没限制就继续运行，已经检查过的不会再检查。第二个限制是接口之间的时间间隔，建议不要再改小了，容易被识别成 many requests

