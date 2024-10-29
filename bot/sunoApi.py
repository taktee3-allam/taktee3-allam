import time
import requests

# replace your vercel domain
base_url = 'https://suno-api-pi-lake.vercel.app'


def custom_generate_audio(payload):
    url = f"{base_url}/api/custom_generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()


def extend_audio(payload):
    url = f"{base_url}/api/extend_audio"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()

def generate_audio_by_prompt(payload):
    url = f"{base_url}/api/generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()


def get_audio_information(audio_ids):
    url = f"{base_url}/api/get?ids={audio_ids}"
    response = requests.get(url)
    return response.json()


def get_quota_information():
    url = f"{base_url}/api/get_limit"
    response = requests.get(url)
    return response.json()

def get_clip(clip_id):
    url = f"{base_url}/api/clip?id={clip_id}"
    response = requests.get(url)
    return response.json()

def generate_whole_song(clip_id):
    payloyd = {"clip_id": clip_id}
    url = f"{base_url}/api/concat"
    response = requests.post(url, json=payload)
    return response.json()


# if __name__ == '__main__':
#     prompt='''
#     write arabic sad romantic song and here the lyrics 
# مين فينا اللي خان مين فينا غلطان مين فينا اللي باع مين الجاسي والاناني واللي ناسي ومين الصان بعدك مش تعبان ولس حتزعل لا تكسب وتطلع مين فينا اللي خان مين فينا غلطان مين فينا اللي باع مين الجاسي والاناني واللي ناسي نصان بعدك مش تعبان ولسه حتزعل لا تكسبه طمني عنك يا قلبي شو ضايل لي منك انت وشو مخبي كم كسره لازمك لا تفهم وتعدي انك مش قد الغرام وانا لسه اتني جنبي انا بطي بج روحي بيدي كلها يومين وه سنين تعد مش هم اللي جالوا يومين وليه م صرتن القصه وين ولاش نا وتسمع مين ها الغص مرجت كلها لسنين وانت لسه اه لليوم مش [موسيقى] ناسي [موسيقى] ا طيب مين الفاز مين الخسران وين الانجاز لما تكسر انسان شايفني بغرق ومادد هلقي خذني بحضنك انا كثير تعبان اسمع كلام واصبر عشان مموع اللي نزلت قبل ما انام بعد الكان صعب النسيان عزيز علي انك تطلع غلطان ول وصرت من القصه وين وليش ناوي تسمع الغصه مرجت كلها لسنين وانت لسه لليوم مش ناسي مين فينا غلطان فينا اللي باع مين القاسي والاناني واللي ناس ومين صام بعدك مش تعبان ولسه هتزعلنا تكسب وتطلع مين مين فينا غلطان مين فينا اللي باع مين الجاسي والاني واللي ناسي ومين نصان بعدك مش تعبان ولسه حتزعل لا تكسب وتطلع مين في فينا اللي خام مين فينا اللي باع مين الجاسي والاناني واللي ناسي [موسيقى] وص ولسه حتزعل ل تكسب وتطلع مين فينا اللي خان مين فينا غلطان مين فينا اللي باع مين القاسي والاناني واللي ناسيون صار بعدك مش تعبان ولسه ساحه تزعل لا تكسب [موسيقى] وتطلع مين فينا الليخ

#     '''
#     data = custom_generate_audio({
#         "prompt":prompt,
#         "make_instrumental": False,
#         "wait_audio": False
#     })
#     print(data)
#     ids = f"{data[0]['id']},{data[1]['id']}"
#     print(f"ids: {ids}")

#     for _ in range(60):
#         data = get_audio_information(ids)
#         if data[0]["status"] == 'streaming':
#             print(f"{data[0]['id']} ==> {data[0]['audio_url']}")
#             print(f"{data[1]['id']} ==> {data[1]['audio_url']}")
#             break
#         # sleep 5s
#         time.sleep(5)
