from PIL import Image
import streamlit as st
c = st.columns(3)
img = Image.open("/home/h/PycharmProjects/BasketOfArt/salon.png")
img = img.resize((250,250))
c[0].button("✔",c[0].image(img))

img = Image.open("/home/h/PycharmProjects/BasketOfArt/salon.png")
img = img.resize((250,250))
c[1].button("✔",c[1].image(img))

