import requests
import json
import re

def get_video_transcript(video_id):
    # Step 1: Get video info
    url = f"https://www.youtube.com/watch?v={video_id}"
    response = requests.get(url)
    html = response.text

    # Step 2: Extract ytInitialPlayerResponse
    match = re.search(r"ytInitialPlayerResponse\s*=\s*({.+?})\s*;", html)
    if not match:
        raise ValueError("Could not find ytInitialPlayerResponse in the page")
    player_response = json.loads(match.group(1))

    # Step 3: Extract captions data
    if "captions" not in player_response or "playerCaptionsTracklistRenderer" not in player_response["captions"]:
        raise ValueError("No captions found for this video")
    
    captions_data = player_response["captions"]["playerCaptionsTracklistRenderer"]
    if "captionTracks" not in captions_data or not captions_data["captionTracks"]:
        raise ValueError("No caption tracks found")
    
    base_url = captions_data["captionTracks"][0]["baseUrl"]

    # Step 4: Request transcript data
    transcript_response = requests.get(base_url)
    transcript_data = transcript_response.text

    # Step 5: Parse and format transcript
    transcript = []
    timestamp = ""
    for line in transcript_data.split("\n"):
        if re.match(r'\d+:\d+:\d+\.\d+,\d+:\d+:\d+\.\d+', line):
            timestamp = line
        elif line.strip():
            transcript.append(f"{timestamp} {line.strip()}")

    if not transcript:
        raise ValueError("No transcript data found")

    return "\n".join(transcript)

def main():
    video_id = input("Enter the YouTube video ID: ")
    try:
        transcript = get_video_transcript(video_id)
        print("\nTranscript:")
        print(transcript)
        
        # Optionally, save to a file
        # with open(f"{video_id}_transcript.txt", "w", encoding="utf-8") as f:
        #     f.write(transcript)
        # print(f"\nTranscript saved to {video_id}_transcript.txt")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
