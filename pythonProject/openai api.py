import openai

openai.api_key = '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'
file_path_input ='txts/message_to_api.txt'
file_path_output = 'txts/message_to_GUI.txt'

with open(file_path_input, "r") as file:
  prompt_input = file.read()

response = openai.Completion.create(
  model="gpt-4",                # 指定模型名称
  prompt=prompt_input,   # 输入提示文本
  temperature=0.7,              # 控制创造性的参数
  max_tokens=100,               # 生成文本的最大长度
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)

with open(file_path_output, "w") as file:
  # 写入内容到文件
  file.write(response.choices[0].text.strip())