import re
import urllib.request

# మీరందజేసిన పర్ఫెక్ట్ తెలుగు బేస్ లిస్ట్
TELUGU_BASE_M3U = """#EXTM3U
#EXTINF:-1 tvg-id="4SiDESTV.in@SD" tvg-logo="https://jiotvimages.cdn.jio.com/dare_images/images/4sites.png" group-title="News",4 SiDES TV (1080p)
https://stream.ottlive.co.in/4sidestv/index.m3u8
#EXTINF:-1 tvg-id="6TVTelugu.in@SD" tvg-logo="https://i.imgur.com/l3EcRnZ.png" group-title="News",6 TV Telugu (576p)
https://yuppparoriglin.akamaized.net/181224/smil:6tv.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b
#EXTINF:-1 tvg-id="9PlusNews.in@SD" tvg-logo="https://jiotvimages.cdn.jio.com/dare_images/images/9plusnews.png" group-title="News",9 Plus News (1080p)
https://stream.ottlive.co.in/9plusnews/index.m3u8
#EXTINF:-1 tvg-id="10TV.in@SD" tvg-logo="https://xstreamcp-assets-msp.streamready.in/assets/LIVETV/LIVECHANNEL/LIVETV_LIVETVCHANNEL_10TV/images/LOGO_HD/image.png" group-title="News",10 TV (720p)
https://mumbai-edge.smartplaytv.in/10TV/index.m3u8
#EXTINF:-1 tvg-id="99TV.in@SD" tvg-logo="https://i.imgur.com/dZA4gel.png" group-title="News",99TV (720p)
https://cdn.pishow.tv/ott/live/1211/master.m3u8
#EXTINF:-1 tvg-id="AasthaTelugu.in@SD" tvg-logo="https://dtil.tmsimg.com/assets/s158136_ld_h15_aa.png?lock=720x540" group-title="Religious",Aastha Telugu (576p)
https://mumbai-edge.smartplaytv.in/AasthaTelugu/index.m3u8
#EXTINF:-1 tvg-id="ABNAndhraJyoti.in@SD" tvg-logo="https://dtil.tmsimg.com/assets/s142517_ld_h15_aa.png?lock=720x540" group-title="News",ABN Andhra Jyoti (720p)
https://mumbai-edge.smartplaytv.in/ABNAJ/index.m3u8
#EXTINF:-1 tvg-id="BhakthiTV.in@SD" tvg-logo="https://upload.wikimedia.org/wikipedia/en/6/61/Bhakthi_TV_logo.jpg" group-title="Religious",Bhakthi TV (720p)
https://cdn.pishow.tv/ott/live/397/master.m3u8
#EXTINF:-1 tvg-id="BIGTV.in@SD" tvg-logo="https://jiotvimages.cdn.jio.com/dare_images/images/Big_TV.png" group-title="News",BIG TV (720p)
https://cdn.pishow.tv/ott/live/1059/master.m3u8
#EXTINF:-1 tvg-id="BRKNews.in@SD" tvg-logo="https://d229kpbsb5jevy.cloudfront.net/yuppfast/content/common/channel/logos/brk-news.png" group-title="News",BRK News (720p)
https://mumbai-edge.smartplaytv.in/BRKNEWS/index.m3u8
#EXTINF:-1 tvg-id="CVRHealth.in@SD" tvg-logo="https://i.imgur.com/bCyW32I.png" group-title="Lifestyle",CVR Health (576p)
https://mumbai-edge.smartplaytv.in/CVRHealth/index.m3u8
#EXTINF:-1 tvg-id="CVRNews.in@SD" tvg-logo="https://xstreamcp-assets-msp.streamready.in/assets/LIVETV/LIVECHANNEL/LIVETV_LIVETVCHANNEL_CVR_NEWS/images/LOGO_HD/LOGO_HD_image.png" group-title="News",CVR News (576p)
https://mumbai-edge.smartplaytv.in/CVRNews/index.m3u8
#EXTINF:-1 tvg-id="CVROMSpiritual.in@SD" tvg-logo="https://jiotvimages.cdn.jio.com/dare_images/images/CVR_OM_Spiritual.png" group-title="Religious",CVR OM Spiritual (576p)
https://yuppnimrestreammum.akamaized.net/181224/smil:cvrom1.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b
#EXTINF:-1 tvg-id="DDSaptagiri.in@SD" tvg-logo="https://xstreamcp-assets-msp.streamready.in/assets/LIVETV/LIVECHANNEL/LIVETV_LIVETVCHANNEL_DD_SAPTAGIRI/images/LOGO_HD/image.png" group-title="General",DD Saptagiri (504p)
https://d2lk5u59tns74c.cloudfront.net/out/v1/26e915d6d12b4a06822c5e33c088ed56/index.m3u8
#EXTINF:-1 tvg-id="DDYadagiri.in@SD" tvg-logo="https://xstreamcp-assets-msp.streamready.in/assets/LIVETV/LIVECHANNEL/LIVETV_LIVETVCHANNEL_DD_YADAGIRI/images/LOGO_HD/image.png" group-title="General",DD Yadagiri (576p)
https://cdn.pishow.tv/ott/live/21/master.m3u8
#EXTINF:-1 tvg-id="ETVAndhraPradesh.in@SD" tvg-logo="https://i.imgur.com/pFNCRnf.png" group-title="News",ETV Andhra Pradesh (1080p)
https://d1g35elx8qnif3.cloudfront.net/v1/master/9d43eacaed199f8d5883927e7aef514a8a08e108/ETV_AP_H264_cloud_in/index.m3u8
#EXTINF:-1 tvg-id="ETVBalBharat.in@SD" tvg-logo="https://i.imgur.com/zsTxPV9.png" group-title="Kids",ETV Bal Bharat (576p)
http://103.185.24.134:3001/ETV-BAL-BHARAT/index.m3u8
#EXTINF:-1 tvg-id="ETVBeats.in@HD" tvg-logo="https://jiotvimages.cdn.jio.com/dare_images/images/ETVBeats1.png" group-title="Music",ETV Beats (1080p)
https://jmp2.uk/stvp-IN4900002RV
#EXTINF:-1 tvg-id="ETVCinema.in@SD" tvg-logo="https://dtil.tmsimg.com/assets/s143026_ld_h15_aa.png?lock=720x540" group-title="Movies",ETV Cinema (396p)
https://yupplivegcpusa.yuppcdn.net/100823/smil:etvcinema.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b
#EXTINF:-1 tvg-id="ETVCinema.in@HD" tvg-logo="https://dtil.tmsimg.com/assets/s143026_ld_h15_aa.png?lock=720x540" group-title="Movies",ETV Cinema HD (1080p)
https://d27zlkxhgwrfgo.cloudfront.net/v1/master/9d43eacaed199f8d5883927e7aef514a8a08e108/ETV_CINEMA_H264_cloud_in/index.m3u8
#EXTINF:-1 tvg-id="ETVComedy.in@HD" tvg-logo="https://jiotvimages.cdn.jio.com/dare_images/images/ETV_Comedy.png" group-title="Comedy",ETV Comedy (1080p)
https://cc-wie8j8y69d2uy.akamaized.net/WWBI/Amagi/ETV_Comedy_IN/playlist.m3u8
#EXTINF:-1 tvg-id="ETVJosh.in@HD" tvg-logo="https://jiotvimages.cdn.jio.com/dare_images/images/ETV_Josh.png" group-title="Entertainment",ETV Josh (1080p)
https://cc-uyh1ow5zouoio.akamaized.net/WWBI/Amagi/ETV_Josh_IN/playlist.m3u8
#EXTINF:-1 tvg-id="ETVLife.in@SD" tvg-logo="https://xstreamcp-assets-msp.streamready.in/assets/LIVETV/LIVECHANNEL/LIVETV_LIVETVCHANNEL_ETV_LIFE/images/LOGO_HD/image.png" group-title="Lifestyle",ETV Life (1080p)
https://mumbai-edge.smartplaytv.in/ETVLIFE/index.m3u8
#EXTINF:-1 tvg-id="ETVMusic.in@SD" tvg-logo="https://jiotvimages.cdn.jio.com/dare_images/images/ETVMusic12.png" group-title="Music",ETV Music (1080p)
https://mumbai-edge.smartplaytv.in/ETVABHIRUCHI/index.m3u8
#EXTINF:-1 tvg-id="ETVNews.in@HD" tvg-logo="https://jiotvimages.cdn.jio.com/dare_images/images/ETV_News.png" group-title="News",ETV News (1080p)
https://cc-3448kp65yhc5w.akamaized.net/WWBI/Amagi/ETV_News_IN/playlist.m3u8
#EXTINF:-1 tvg-id="ETVPlus.in@SD" tvg-logo="https://xstreamcp-assets-msp.streamready.in/assets/LIVETV/LIVECHANNEL/LIVETV_LIVETVCHANNEL_ETV_PLUS/images/LOGO_HD/image.png" group-title="Entertainment",ETV Plus (396p)
https://yupplivegcpusa.yuppcdn.net/100823/smil:etvplus.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b
#EXTINF:-1 tvg-id="ETVPlus.in@HD" tvg-logo="https://xstreamcp-assets-msp.streamready.in/assets/LIVETV/LIVECHANNEL/LIVETV_LIVETVCHANNEL_ETV_PLUS/images/LOGO_HD/image.png" group-title="Entertainment",ETV Plus HD (1080p)
https://d12ee3o8yfkkhd.cloudfront.net/c6a4b411295f47f48c908d2ac0605bad/index.m3u8
#EXTINF:-1 tvg-id="ETVTelangana.in@SD" tvg-logo="https://dtil.tmsimg.com/assets/s143032_ld_h15_aa.png?lock=720x540" group-title="News",ETV Telangana (1080p)
https://d37d7pfp7vjqhh.cloudfront.net/v1/master/9d43eacaed199f8d5883927e7aef514a8a08e108/ETV_TS_H264_cloud_in/index.m3u8
#EXTINF:-1 tvg-id="ETVTelugu.in@HD" tvg-logo="https://xstreamcp-assets-msp.streamready.in/assets/LIVETV/LIVECHANNEL/LIVETV_LIVETVCHANNEL_ETV_HD/images/LOGO_HD/image.png" group-title="Entertainment",ETV Telugu HD (1080p)
https://mumbai-edge.smartplaytv.in/ETVHD/index.m3u8
#EXTINF:-1 tvg-id="HinduDharmam.in@SD" tvg-logo="https://dtil.tmsimg.com/assets/s143131_ld_h15_aa.png?lock=720x540" group-title="Religious",Hindu Dharmam (1080p)
https://mumbai-edge.smartplaytv.in/Hindudharmam/index.m3u8
#EXTINF:-1 tvg-id="HMTV.in@SD" tvg-logo="https://dtil.tmsimg.com/assets/s143136_ld_h15_aa.png?lock=720x540" group-title="News",HMTV (India) (720p)
https://cdn.pishow.tv/ott/live/280/master.m3u8
#EXTINF:-1 tvg-id="INews.in@SD" tvg-logo="https://jiotvimages.cdn.jio.com/dare_images/images/I_News.png" group-title="News",INews (720p)
https://cdn.pishow.tv/ott/live/411/master.m3u8
#EXTINF:-1 tvg-id="MahaaBhakti.in@SD" tvg-logo="https://yt3.googleusercontent.com/OWECRvCVJh-dXU2MTRZhMRIDvFvcWan0YMoWWfXsM5_WEHobQy2QoHQbGr7AZUXzMOByTMAXbg=s900-c-k-c0x00ffffff-no-rj" group-title="Religious",Mahaa Bhakti (1080p)
https://mumbai-edge.smartplaytv.in/MahaBhakthi/index.m3u8
#EXTINF:-1 tvg-id="MahaaMax.in@SD" tvg-logo="https://objectstorage.ap-mumbai-1.oraclecloud.com/p/7Eg7LPw1gBcncVDrfwf__7yyrg13awaU6DmMk4gutavGYZgoAuAziv8e0aSEdU4G/n/bmaqqlwez184/b/GTPL_CHANNEL_LOGO/o/gtpl/MAHAA+MAX+LOGO.png" group-title="Entertainment",Mahaa Max (1080p)
https://mumbai-edge.smartplaytv.in/MahaMax/index.m3u8
#EXTINF:-1 tvg-id="MahaaNews.in@SD" tvg-logo="https://i.imgur.com/buT76vR.png" group-title="News",Mahaa News (1080p)
https://mumbai-edge.smartplaytv.in/MahaNews/index.m3u8
#EXTINF:-1 tvg-id="MangoMobileTV.in@HD" tvg-logo="https://dvvlqr1rtlak3.cloudfront.net/Mango/MANGOTVLOGO.jpg" group-title="Entertainment",Mango Mobile TV (1080p)
https://amg01911-mangotv-amg01911c1-xiaomi-in-1270.playouts.now.amagi.tv/playlist/amg01911-mangomassmedia-mangotv-xiaomiin/playlist.m3u8
#EXTINF:-1 tvg-id="MetroTV.in@SD" tvg-logo="https://jiotvimages.cdn.jio.com/dare_images/images/Metro_TV.png" group-title="General",Metro TV (India) (1080p)
https://mercury.streambridge.link:8042/telugu/metrotv/index.m3u8
#EXTINF:-1 tvg-id="MojoTV.in@SD" tvg-logo="https://upload.wikimedia.org/wikipedia/en/1/19/MOJO_TV_LOGO.png" group-title="News",Mojo TV (576p)
https://mumt07.tangotv.in/zHjX9OFlMOJOTV/index.m3u8
#EXTINF:-1 tvg-id="NTVTelugu.in@SD" tvg-logo="https://i.imgur.com/WqTIoWS.png" group-title="News",NTV Telugu (1080p)
https://mumbai-edge.smartplaytv.in/NTVTelugu/index.m3u8
#EXTINF:-1 tvg-id="PMCTelugu.in@SD" tvg-logo="https://jiotvimages.cdn.jio.com/dare_images/images/PMC_Telugu.png" group-title="Religious",PMC Telugu (1080p)
https://mumbai-edge.smartplaytv.in/PMC/index.m3u8
#EXTINF:-1 tvg-id="Prime9News.in@SD" tvg-logo="https://jiotvimages.cdn.jio.com/dare_images/images/Prime_9_News.png" group-title="News",Prime9 News (1080p)
https://mumbai-edge.smartplaytv.in/Prime9News/index.m3u8
#EXTINF:-1 tvg-id="RajMusixTelugu.in@SD" tvg-logo="https://xstreamcp-assets-msp.streamready.in/assets/LIVETV/LIVECHANNEL/LIVETV_LIVETVCHANNEL_RAJ_MUSIX_TELUGU/images/LOGO_HD/image.png" group-title="Music",Raj Musix Telugu (720p)
https://cdn.pishow.tv/ott/live/1213/master.m3u8
#EXTINF:-1 tvg-id="RajNewsTelugu.in@SD" tvg-logo="https://xstreamcp-assets-msp.streamready.in/assets/LIVETV/LIVECHANNEL/LIVETV_LIVETVCHANNEL_RAJ_NEWS_TELUGU/images/LOGO_HD/image.png" group-title="News",Raj News Telugu (576p)
https://mumt04.tangotv.in/m18aqlK4RAJNEWSTELUGU/index.m3u8
#EXTINF:-1 tvg-id="SakshiTV.in@SD" tvg-logo="https://xstreamcp-assets-msp.streamready.in/assets/LIVETV/LIVECHANNEL/LIVETV_LIVETVCHANNEL_SAKSHI_TV/images/LOGO_HD/image.png" group-title="News",Sakshi TV (576p)
https://yuppmedtaorire.akamaized.net/v1/master/a0d007312bfd99c47f76b77ae26b1ccdaae76cb1/sakshi_nim_https/240122/sakshi/playlist.m3u8
#EXTINF:-1 tvg-id="StarMaa.in@HD" tvg-logo="https://i.imgur.com/5c9PVS0.png" group-title="Entertainment",Star Maa HD (720p)
https://da86m1sqpm3o0.cloudfront.net/28072023/smil:starmaa1.smil/chunklist_b2628000.m3u8
#EXTINF:-1 tvg-id="StarMaaMovies.in@HD" tvg-logo="https://dtil.tmsimg.com/assets/s143826_ld_h15_aa.png?lock=720x540" group-title="Movies",Star Maa Movies HD (720p)
https://da86m1sqpm3o0.cloudfront.net/28072023/smil:maamovies.smil/chunklist_b2628000.m3u8
#EXTINF:-1 tvg-id="SunGemini.in@SD" tvg-logo="https://sund-images.sunnxt.com/194396/300x300_SunGemini_194396_22c18c1e-7eb9-4855-9c4e-12e109911559.png" group-title="General",Sun Gemini (576p)
http://ptuf.ridsys.in/riptv/live/GEMINI_TV/index.m3u8
#EXTINF:-1 tvg-id="SVBC.in@SD" tvg-logo="https://dtil.tmsimg.com/assets/s143889_ld_h9_ab.png?lock=720x540" group-title="Religious",SVBC (1080p)
https://player.mslivestream.net/telugu/5d076e5c3d34cb8bb08e54a4bb7e223e.sdp/playlist.m3u8
#EXTINF:-1 tvg-id="SwatantraTV.in@SD" tvg-logo="https://jiotvimages.cdn.jio.com/dare_images/images/Swatantra_News.png" group-title="News",Swatantra TV (1080p)
https://mumbai-edge.smartplaytv.in/SwatantraTV/index.m3u8
#EXTINF:-1 tvg-id="TNews.in@SD" tvg-logo="https://dtil.tmsimg.com/assets/s143919_ld_h15_aa.png?lock=720x540" group-title="News",T News (720p)
https://cdn.pishow.tv/ott/live/385/master.m3u8
#EXTINF:-1 tvg-id="TeluguOne.in@HD" tvg-logo="https://jiotvimages.cdn.jio.com/dare_images/images/teluguone.png" group-title="Entertainment",Telugu One (1080p)
https://teluguone-yupptv.vgcdn.net/v1/019be9e3f04d1ea55784338b5c3e89/019be9e4474415fc60e93459e1e808/teluguone_2500k.m3u8
#EXTINF:-1 tvg-id="TollyTV.in@HD" tvg-logo="https://d229kpbsb5jevy.cloudfront.net/yuppfast/content/common/channel/logos/aumnrs.png" group-title="Movies",Tolly TV (1080p)
https://streams2.sofast.tv/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/13b5735d-52c3-4be0-853d-e0ec0127e708/manifest.m3u8
#EXTINF:-1 tvg-id="TV5News.in@SD" tvg-logo="https://xstreamcp-assets-msp.streamready.in/assets/LIVETV/LIVECHANNEL/LIVETV_LIVETVCHANNEL_TV5_TELUGU/images/LOGO_HD/image.png" group-title="News",TV5 News (576p)
https://yuppmedtaorire.akamaized.net/v1/master/a0d007312bfd99c47f76b77ae26b1ccdaae76cb1/tv5_nim_https/110322/tv5/playlist.m3u8
#EXTINF:-1 tvg-id="TV9Telugu.in@SD" tvg-logo="https://xstreamcp-assets-msp.streamready.in/assets/LIVETV/LIVECHANNEL/LIVETV_LIVETVCHANNEL_TV9_TELUGU_NEWS/images/LOGO_HD/image.png" group-title="News",TV9 Telugu (720p)
https://dyjmyiv3bp2ez.cloudfront.net/pub-iotv9telcmjhcs/liveabr/playlist.m3u8
#EXTINF:-1 tvg-id="V6News.in@SD" tvg-logo="https://dtil.tmsimg.com/assets/s144047_ld_h15_aa.png?lock=720x540" group-title="News",V6 News (576p)
https://yuppmedtaorire.akamaized.net/v1/master/a0d007312bfd99c47f76b77ae26b1ccdaae76cb1/v6news_nim_https/140622/v6news/playlist.m3u8
#EXTINF:-1 tvg-id="VanithaTV.in@SD" tvg-logo="https://jiotvimages.cdn.jio.com/dare_images/images/Vanitha.png" group-title="Entertainment",Vanitha TV (576p)
https://mumt01.tangotv.in/O5aw8Zn3VANITHA/index.m3u8
#EXTINF:-1 tvg-id="VissaTV.in@SD" tvg-logo="https://xstreamcp-assets-msp.streamready.in/assets/LIVETV/LIVECHANNEL/LIVETV_LIVETVCHANNEL_VISSA_TV/images/LOGO_HD/image.png" group-title="Entertainment",Vissa TV (576p)
https://mumt07.tangotv.in/zHjX9OFlVISSATV/index.m3u8
#EXTINF:-1 tvg-id="WOWKidz.in@Telugu" tvg-logo="https://d229kpbsb5jevy.cloudfront.net/yupptvnew/content/common/channel/logos/mjvezt.png" group-title="Animation;Kids",WOW Kidz Telugu (720p)
https://yuppparoriglin.akamaized.net/181224/smil:wowkidztelgu.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b
#EXTINF:-1 tvg-id="ZeeTelugu.in@HD" tvg-logo="https://xstreamcp-assets-msp.streamready.in/assets/LIVETV/LIVECHANNEL/LIVETV_LIVETVCHANNEL_ZEE_TELUGU/images/LOGO_HD/LOGO_HD_image.png" group-title="Entertainment",Zee Telugu HD (576p)
https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/in/YuppTV/ZeeTeluguHD.m3u8
#EXTINF:-1 tvg-id="ZeeTeluguNews.in@SD" tvg-logo="https://dtil.tmsimg.com/assets/GNLZZGG0023178R.png?lock=720x540" group-title="News",Zee Telugu News (720p)
https://d116gfrn8orazi.cloudfront.net/index.m3u8?akes=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3NjcxOTc5NzJ9.O4qmdMPbHwKrCg6hFXvD70vjSPWKQd0a7NrjmFdeMB8
"""

def process_ap_playlist():
    # 1. custom_tel.m3u ని సృష్టిస్తుంది (Telugu Only)
    with open("custom_tel.m3u", "w", encoding="utf-8") as f:
        f.write(TELUGU_BASE_M3U.strip() + "\n")
    print("custom_tel.m3u created successfully!")

    # 2. custom_ap.m3u ని సృష్టిస్తుంది (Telugu Base + Extra Groups)
    url = "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/in.m3u"
    output_ap_file = "custom_ap.m3u"

    print("Downloading India streams for custom_ap.m3u...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            india_content = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error downloading file: {e}")
        return

    final_ap_lines = [TELUGU_BASE_M3U.strip() + "\n"]
    lines = india_content.splitlines()
    unwanted_keywords = ["gospel", "calvary", "divyavani", "subhavaartha", "peace tv", "quran", "islam", "shopping", "aaseervatham", "hebron", "salaam", "shekinah", "shalom"]

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

            if any(kw in ch_lower for kw in unwanted_keywords):
                continue

            target_group = None
            if any(sp in ch_lower for sp in ["star sports", "sports18", "sony ten", "sony six", "dd sports", "eurosport"]):
                target_group = "All Sports"
            elif any(hm in ch_lower for hm in ["mtv", "9xm", "9x jalwa", "mastiii", "b4u music", "zoom"]):
                target_group = "Hindi Music"
            elif any(em in ch_lower for em in ["vh1", "clubbing tv", "stingray"]):
                target_group = "English Music"
            elif any(hw in ch_lower for hw in ["sony pix", "mnx", "movies now", "star movies", "wb", "hbo", "flix", "bflix"]):
                target_group = "Hollywood Movies"

            if target_group:
                if 'group-title="' in extinf:
                    extinf = re.sub(r'group-title="[^"]*"', f'group-title="{target_group}"', extinf)
                else:
                    extinf = extinf.replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{target_group}"')
                
                final_ap_lines.append(extinf + "\n")
                for u in url_lines:
                    final_ap_lines.append(u + "\n")
        else:
            i += 1

    with open(output_ap_file, "w", encoding="utf-8") as f:
        f.writelines(final_ap_lines)

    print("custom_ap.m3u created successfully!")

if __name__ == "__main__":
    process_ap_playlist()
