import re
import urllib.request

def process_playlist():
    # Direct Streams Source
    url = "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/in.m3u"
    output_file = "custom_india.m3u"

    print("Downloading playlist...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error downloading file: {e}")
        return

    lines = content.splitlines()
    filtered_lines = ["#EXTM3U\n"]

    # క్రిస్టియన్, ముస్లిం మరియు మరే ఇతర హిందూ యేతర భక్తి / షాపింగ్ ఛానెల్స్ కీవర్డ్స్
    unwanted_keywords = [
        "gospel", "calvary", "divyavani", "nireekshana", "subhavaartha",
        "peace tv", "quran", "islam", "madani", "praise", "salvation",
        "shopping", "cj grand", "tjc", "aaseervatham", "hebron", "salaam", 
        "shekinah", "shalom", "prarthana", "powervision", "velicham"
    ]

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#EXTINF:"):
            extinf = line
            url_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith("#EXTINF:"):
                url_lines.append(lines[i])
                i += 1

            full_block = extinf + "\n" + "\n".join(url_lines)
            ch_lower = full_block.lower()

            # 1. వద్దు అనుకున్న డెవోషనల్ / షాపింగ్ ఫిల్టర్ చేయడం
            if any(kw in ch_lower for kw in unwanted_keywords):
                continue

            # 2. గ్రూప్ టైటిల్ కేటాయింపు (Group Title Assignment)
            target_group = None

            # All Sports Group
            if any(sp in ch_lower for sp in ["star sports", "sports18", "sony ten", "sony six", "dd sports", "eurosport"]):
                target_group = "All Sports"

            # Telugu Music Group
            elif any(tm in ch_lower for tm in ["etv music", "raj musix telugu", "etv beats"]):
                target_group = "Telugu Music"

            # Hindi Music Group
            elif any(hm in ch_lower for hm in ["mtv", "9xm", "9x jalwa", "mastiii", "b4u music", "zoom", "bindass"]):
                target_group = "Hindi Music"

            # English Music Group
            elif any(em in ch_lower for em in ["vh1", "clubbing tv", "stingray"]):
                target_group = "English Music"

            # Hollywood Movies Group
            elif any(hw in ch_lower for hw in ["sony pix", "mnx", "movies now", "star movies", "wb", "hbo", "flix", "andflix", "bflix"]):
                target_group = "Hollywood Movies"

            # Religious / Devotional (Hindu) Group
            elif any(rel in ch_lower for rel in ["svbc", "bhakthi", "aastha", "adhyatm", "pmc", "om tv", "soham", "sharnam", "santvani"]):
                target_group = "Religious"

            # Telugu News / Entertainment Group
            elif any(tel in ch_lower for tel in ["telugu", "etv", "gemini", "maa", "zee telugu", "sakshi", "tv9", "ntv", "10tv", "v6", "htv"]):
                # ఒరిజినల్ ఫైల్ లో group-title ఉంటే ఉంచడం, లేకపోతే Entertainment అని సెట్ చేయడం
                if 'group-title="' in extinf:
                    target_group = None # ఉంచేయ్
                else:
                    target_group = "Telugu"

            # 3. group-title ను #EXTINF లో స్పష్టంగా ఇన్సర్ట్/రీప్లేస్ చేయడం
            if target_group:
                if 'group-title="' in extinf:
                    extinf = re.sub(r'group-title="[^"]*"', f'group-title="{target_group}"', extinf)
                else:
                    # group-title లేకపోతే tvg-id లేదా లాస్ట్ కామా కి ముందు స్పష్టంగా యాడ్ చేయడం
                    extinf = extinf.replace('#EXTINF:-1 ', f'#EXTINF:-1 group-title="{target_group}" ')

            # చెల్లుబాటు అయ్యే గ్రూప్ లేదా తెలుగు ఛానెల్స్ మాత్రమే యాడ్ అవ్వడం
            if target_group or any(tel in ch_lower for tel in ["telugu", "etv", "gemini", "maa", "zee telugu", "sakshi", "tv9", "ntv", "10tv", "v6"]):
                filtered_lines.append(extinf + "\n")
                for u in url_lines:
                    filtered_lines.append(u + "\n")
        else:
            i += 1

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(filtered_lines)

    print("custom_india.m3u updated with strict group-title tags!")

if __name__ == "__main__":
    process_playlist()
