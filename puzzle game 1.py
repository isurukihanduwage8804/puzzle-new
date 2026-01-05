import streamlit as st
import random
from PIL import Image
import io

st.set_page_config(page_title="Image Puzzle Game", layout="centered")

st.title("🧩 Jigsaw Puzzle Game")
st.write("රූපයේ කොටස් දෙකක් click කර ඒවා නිවැරදි තැනට එන තෙක් මාරු කරන්න.")

# 1. රූපය කොටස්වලට කැඩීමේ function එක
def split_image(img, rows, cols):
    w, h = img.size
    tile_w, tile_h = w // cols, h // rows
    tiles = []
    for r in range(rows):
        for c in range(cols):
            box = (c * tile_w, r * tile_h, (c + 1) * tile_w, (r + 1) * tile_h)
            tile = img.crop(box)
            tiles.append(tile)
    return tiles

# 2. Game State එක තබා ගැනීම
if 'tiles' not in st.session_state:
    # මුලින්ම පෙන්වන්න රූපයක් තෝරන්න (ඔයාට ඕන එකක් link කරන්න පුළුවන්)
    # දැනට placeholder රූපයක් පාවිච්චි කරමු
    default_img = Image.new('RGB', (300, 300), color=(73, 109, 137))
    st.session_state.tiles = split_image(default_img, 3, 3)
    st.session_state.order = list(range(9))
    random.shuffle(st.session_state.order)
    st.session_state.selected = None

# 3. රූපයක් Upload කිරීමට ඉඩ දීම
uploaded_file = st.file_uploader("ඔයාට කැමති රූපයක් තෝරන්න", type=['jpg', 'png', 'jpeg'])
if uploaded_file:
    img = Image.open(uploaded_file).resize((450, 450))
    st.session_state.tiles = split_image(img, 3, 3)
    if st.button("Start New Game"):
        st.session_state.order = list(range(9))
        random.shuffle(st.session_state.order)
        st.session_state.selected = None

# 4. Puzzle එක පෙන්වීම (Grid එකක් ලෙස)
cols_ui = st.columns(3)
for i in range(9):
    idx = st.session_state.order[i]
    with cols_ui[i % 3]:
        # රූපයේ කොටස button එකක් ලෙස පෙන්වීම
        if st.button(f"Tile {i}", key=f"btn_{i}", use_container_width=True):
            if st.session_state.selected is None:
                st.session_state.selected = i
            else:
                # මාරු කිරීම (Swap)
                sel = st.session_state.selected
                st.session_state.order[sel], st.session_state.order[i] = \
                    st.session_state.order[i], st.session_state.order[sel]
                st.session_state.selected = None
                st.rerun()
        
        st.image(st.session_state.tiles[idx], use_container_width=True)

# 5. දිනුම්දැයි පරීක්ෂා කිරීම
if st.session_state.order == list(range(9)):
    st.balloons()
    st.success("නියමයි! ඔයා ජයග්‍රහණය කළා! 🎉")
