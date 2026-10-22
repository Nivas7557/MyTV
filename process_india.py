import re
import urllib.request

def process_playlist():
    url = "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/in.m3u"
    output_file = "custom_india.m3u"

    print("Downloading India streams playlist...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error downloading file: {e}")
        return

    lines = content.splitlines()
    filtered_lines = ["#EXTM3U\n"]

    # మతపరమైన/షాపింగ్ ఫిల్టర్స్
    unwanted_keywords = [
        "gospel", "calvary", "divyavani", "nireekshana", "subhavaartha",
        "peace tv", "quran", "islam", "madani", "praise", "salvation",
        "shopping", "cj grand", "tjc"
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

            # 1. వద్దనుకున్న డెవోషనల్ / షాపింగ్ ఛానెల్స్ వదిలేయడం
            if any(kw in ch_lower for kw in unwanted_keywords):
                continue

            # 2. కేవలం మనం కోరుకున్న ఛానెల్స్ ని మాత్రమే అలౌ చేయడం (Strict Inclusion)
            is_valid = False

            # All Sports Group
            if 'group-title="sports"' in ch_lower or any(sp in ch_lower for sp in ["star sports", "sports18", "sony ten", "sony six", "dd sports", "eurosport"]):
                extinf = re.sub(r'group-title="[^"]*"', 'group-title="All Sports"', extinf)
                is_valid = True

            # Telugu Music Group
            elif any(tm in ch_lower for tm in ["etv music", "raj musix telugu", "etv beats"]):
                extinf = re.sub(r'group-title="[^"]*"', 'group-title="Telugu Music"', extinf)
                is_valid = True

            # Hindi Music Group
            elif any(hm in ch_lower for hm in ["mtv", "9xm", "9x jalwa", "mastiii", "b4u music", "zoom", "bindass"]):
                extinf = re.sub(r'group-title="[^"]*"', 'group-title="Hindi Music"', extinf)
                is_valid = True

            # English Music Group
            elif any(em in ch_lower for em in ["vh1", "clubbing tv", "stingray"]):
                extinf = re.sub(r'group-title="[^"]*"', 'group-title="English Music"', extinf)
                is_valid = True

            # Hollywood Movies Group
            elif any(hw in ch_lower for hw in ["sony pix", "mnx", "movies now", "star movies", "wb", "hbo", "flix", "andflix"]):
                extinf = re.sub(r'group-title="[^"]*"', 'group-title="Hollywood Movies"', extinf)
                is_valid = True

            # Telugu Channels (Entertainment, News, Hindu Devotional, Kids)
            elif any(tel in ch_lower for tel in ["telugu", "etv", "gemini", "maa", "zee telugu", "sakshi", "tv9 telugu", "ntv", "10tv", "v6", "svbc", "bhakthi tv"]):
                is_valid = True

            # మనం కోరుకున్న కేటగిరీ అయితేనే లిస్ట్‌కి యాడ్ చేయడం
            if is_valid:
                filtered_lines.append(extinf + "\n")
                for u in url_lines:
                    filtered_lines.append(u + "\n")
        else:
            i += 1

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(filtered_lines)

    print("custom_india.m3u updated cleanly with selected channels only!")

if __name__ == "__main__":
    process_playlist()
