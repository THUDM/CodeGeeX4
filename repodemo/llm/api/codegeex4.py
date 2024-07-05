import requests
import json

URL = "" #the url you deploy codegeex service
def codegeex4(prompt, temperature=0.8, top_p=0.8):
    url = URL
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'inputs': prompt,
        'parameters': {
            'best_of':1,
            'do_sample': True,
            'max_new_tokens': 4012,
            'temperature': temperature,
            'top_p': top_p,
            'stop': ["<|endoftext|>", "<|user|>", "<|observation|>", "<|assistant|>"],
        }
    }
    response = requests.post(url, json=data, headers=headers, verify=False, stream=True)

    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8').replace('data:', '').strip()
                if decoded_line:
                    try:

                        content = json.loads(decoded_line)
                    
                        token_text = content.get('token', {}).get('text', '')
                        if '<|endoftext|>' in token_text:
                            break  
                        yield token_text
                    except json.JSONDecodeError:
                        continue
    else:
        print('请求失败:', response.status_code)


