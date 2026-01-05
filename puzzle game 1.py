import streamlit as st
import random
from PIL import Image
import os

st.set_page_config(page_title="EduPuzzle - Learning Game", layout="centered")

# 1. GitHub එකේ තියෙන රූපය ලබා ගැනීම
# ඔයාගේ රූපය 'puzzle_img.jpg' නමින් GitHub එකේ තියෙන්න ඕනේ
IMAGE_PATH = "puzzle_img.jpg" 

def load_image():
    if os.path.exists(IMAGE_PATH):
        return Image.open(IMAGE_PATH).resize((450, 450))
    else:
        st.error("රූපය සොයාගත නොහැක! කරුණාකර 'puzzle_img.jpg' GitHub එකට upload කරන්න.")
        return None

# 2. රූපය කොටස්වලට කැඩීම
def split_image(img, rows, cols):
    w, h = img.size
    tile_w, tile_h = w // cols, h // rows
    tiles = []
    for r in range(rows):
        for c in range(COLS):
            box = (c * tile_w, r * tile_h, (c + 1) * tile_w, (r + 1) * tile_h)
            tiles.append(img.crop(box))
    return tiles

st.title("🎓 EduPuzzle: ඉගෙනගන්න ගමන් සෙල්ලම් කරමු")

img = load_image()

if img:
    # Game State එක පාලනය
    if 'order' not in st.session_state:
        st.session_state.tiles = split_image(img, 3, 3)
        st.session_state.order = list(range(9))
        random.shuffle(st.session_state.order)
        st.session_state.selected = None

    # පසල් එක පෙන්වීම
    cols_ui = st.columns(3)
    for i in range(9):
        idx = st.session_state.order[i]
        with cols_ui[i % 3]:
            if st.button(f"තෝරන්න {i}", key=f"tile_{i}"):
                if st.session_state.selected is None:
                    st.session_state.selected = i
                else:
                    sel = st.session_state.selected
                    st.session_state.order[sel], st.session_state.order[i] = \
                        st.session_state.order[i], st.session_state.order[sel]
                    st.session_state.selected = None
                    st.rerun()
            st.image(st.session_state.tiles[idx], use_container_width=True)

    # දිනුම්දැයි පරීක්ෂා කිරීම සහ අධ්‍යාපනික විස්තරය
    if st.session_state.order == list(range(9)):
        st.balloons()
        st.success("🎉 නියමයි! ඔයා පසල් එක විසඳුවා.")
        
        # මෙතනට ඔයාට ඕන කරන අධ්‍යාපනික විස්තරය ඇතුළත් කරන්න
        st.info("""
        ### 📚 ඔබ දන්නවාද?
        මේ රූපයෙන් දැක්වෙන්නේ [මෙහි රූපය ගැන විස්තරයක් ලියන්න]. 
        මෙය ඉගෙනීම සඳහා ඉතා වැදගත් වේ...
        """)
