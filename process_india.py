import re
import urllib.request

def process_playlist():
    # Direct India streams playlist URL
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

    # Non-Hindu devotional & shopping keywords to exclude
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

            # 1. Skip non-Hindu devotional & shopping channels
            if any(kw in ch_lower for kw in unwanted_keywords):
                continue

            # 2. Custom Grouping Logic
            # All Sports Group
            if 'group-title="sports"' in ch_lower or any(sp in ch_lower for sp in ["star sports", "sports18", "sony ten", "sony six", "dd sports", "eurosport"]):
                extinf = re.sub(r'group-title="[^"]*"', 'group-title="All Sports"', extinf)

            # Telugu Music Group
            elif any(tm in ch_lower for tm in ["etv music", "raj musix telugu", "etv beats"]):
                extinf = re.sub(r'group-title="[^"]*"', 'group-title="Telugu Music"', extinf)

            # Hindi Music Group
            elif any(hm in ch_lower for hm in ["mtv", "9xm", "9x jalwa", "mastiii", "b4u music", "zoom", "bindass"]):
                extinf = re.sub(r'group-title="[^"]*"', 'group-title="Hindi Music"', extinf)

            # English Music Group
            elif any(em in ch_lower for em in ["vh1", "clubbing tv", "stingray"]):
                extinf = re.sub(r'group-title="[^"]*"', 'group-title="English Music"', extinf)

            # Hollywood Movies Group
            elif any(hw in ch_lower for hw in ["sony pix", "mnx", "movies now", "star movies", "wb", "hbo", "flix", "andflix"]):
                extinf = re.sub(r'group-title="[^"]*"', 'group-title="Hollywood Movies"', extinf)

            filtered_lines.append(extinf + "\n")
            for u in url_lines:
                filtered_lines.append(u + "\n")
        else:
            i += 1

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(filtered_lines)

    print("custom_india.m3u successfully generated!")

if __name__ == "__main__":
    process_playlist()
