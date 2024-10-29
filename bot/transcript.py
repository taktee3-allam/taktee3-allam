import requests
def takeTranscript2(videoID):
    # URL and Headers
    url = f'https://notegpt.io/api/v1/get-transcript-v2?video_id={videoID}&platform=youtube'
    headers = {
        'authority': 'notegpt.io',
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,ar;q=0.7,ru;q=0.6',
        'cookie': 'sbox-guid=MTcwNTU3NjA1MXw1Njd8OTg3ODQ4NDU2; _uab_collina=170557605316511595840735; _ga_PFX3BRW5RQ=GS1.1.1705576053.1.0.1705576053.0.0.0; anonymous_user_id=31de18b44442c52500a24fc44a9054cf; is_first_visit=true; _ga=GA1.2.576764985.1705576054; _gid=GA1.2.1091687766.1705576056; _trackUserId=G-1705576056000',
        'referer': 'https://notegpt.io/youtube-video-summarizer',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }

    # Sending request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        json_data = response.json()
        # print(json_data)
        # Extract the first transcript object and its .default property
        transcripts = json_data.get('data', {}).get('transcripts', [])
        print(transcripts)
        if transcripts:
            print(transcripts)
            first_transcript = transcripts['ar_auto_auto'] # Get the first transcript object
            transcript_default = first_transcript.get('custom', [])

            # Concatenate the text from each segment into a single paragraph
            text_content = [segment.get('text', '').strip() for segment in transcript_default]
            paragraphs = ' '.join(text_content)
            
            print(paragraphs)
            return paragraphs
        else:
            print("No transcripts found.")
            return None
    else:
        print(f"Failed to get transcript. Status code: {response.status_code}")
        return None

# takeTranscript2("Il-hyg0XzAI")