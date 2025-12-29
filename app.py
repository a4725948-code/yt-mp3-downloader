import streamlit as st
import yt_dlp
import os
import subprocess
import sys

# --- 自動更新功能 ---
def check_for_updates():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"])
        return True
    except:
        return False

if 'updated' not in st.session_state:
    with st.spinner('正在檢查組件更新...'):
        check_for_updates()
        st.session_state['updated'] = True

# --- 進度條回傳函式 ---
def progress_hook(d):
    if d['status'] == 'downloading':
        # 提取數據
        p = d.get('_percent_str', '0%').replace('%','')
        percent = float(p) / 100
        speed = d.get('_speed_str', '未知')
        eta = d.get('_eta_str', '未知')
        
        # 更新 Streamlit 介面
        progress_bar.progress(percent)
        status_text.text(f"🚀 下載速度：{speed} | ⏳ 預計剩餘時間：{eta}")
    
    if d['status'] == 'finished':
        status_text.text("✅ 下載完成，正在轉換 MP3 格式...")

def download_mp3(url):
    ydl_opts = {
    'format': 'bestaudio/best',
    # 加入以下這幾行
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'no_warnings': True,
    'quiet': True,
    'extract_flat': False,
    # ----------------
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'downloaded_audio.%(ext)s',
    'progress_hooks': [progress_hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
            return filename, info.get('title', 'music')
    except Exception as e:
        return None, str(e)

# --- 網頁介面 ---
st.title("🎵 高階版 YouTube MP3 下載器")
video_url = st.text_input("輸入網址：")

if st.button("開始下載"):
    if video_url:
        # 建立進度條與文字佔位符
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        file_path, title = download_mp3(video_url)
        
        if file_path and os.path.exists(file_path):
            st.success(f"🎉 成功完成：{title}")
            with open(file_path, "rb") as f:
                st.download_button("點我存檔到電腦", f, file_name=f"{title}.mp3")
        else:
            st.error(f"下載失敗：{title}")

# 新增這個自動更新函式
def check_for_updates():
    try:
        # 在背景執行更新 yt-dlp 的指令
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"])
        return True
    except Exception as e:
        return False

# 每次 App 啟動時執行更新
if 'updated' not in st.session_state:
    with st.spinner('正在檢查組件更新，確保下載成功率...'):
        if check_for_updates():
            st.session_state['updated'] = True
            # st.toast("組件已更新至最新版本！") # 小提示
def download_mp3(url):
    # 設定 yt-dlp 參數
    ydl_opts = {
    'format': 'bestaudio/best',
    # 加入以下這幾行
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'no_warnings': True,
    'quiet': True,
    'extract_flat': False,
    # ----------------
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'downloaded_audio.%(ext)s',
    'progress_hooks': [progress_hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 獲取影片資訊
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
            return filename, info.get('title', 'music')
    except Exception as e:
        return None, str(e)

# --- 網頁介面設計 ---
st.title("🎵 YouTube 轉 MP3 下載器")
st.write("這是一個教育用途的練習專案，請尊重版權內容。")

video_url = st.text_input("請輸入 YouTube 影片網址：", placeholder="https://www.youtube.com/watch?v=...")

if st.button("開始處理"):
    if video_url:
        with st.spinner("正在解析並下載音訊，請稍候..."):
            file_path, title = download_mp3(video_url)
            
            if file_path and os.path.exists(file_path):
                st.success(f"完成！準備下載：{title}")
                
                # 提供下載按鈕
                with open(file_path, "rb") as f:
                    st.download_button(
                        label="點擊下載 MP3",
                        data=f,
                        file_name=f"{title}.mp3",
                        mime="audio/mpeg"
                    )
                
                # 清理伺服器端的暫存檔（選用）
                # os.remove(file_path)
            else:
                st.error(f"發生錯誤：{title}")
    else:

        st.warning("請先輸入網址！")

