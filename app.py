import streamlit as st
import base64
from pathlib import Path
import os
from PIL import Image
import pandas as pd

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

st.markdown("<center><h1>Basket Of Art- AI Solution</h1><center>",unsafe_allow_html=True)
c = st.columns(3)
st.markdown("<center><h3>Budget Optimisation</h3><center>",unsafe_allow_html=True)
budget = st.number_input("Put Your Budget(TND)",min_value=5000)
st.markdown("<center><h4>Get Inspired</h4><center>",unsafe_allow_html=True)
insp = []

c = st.columns(6)

c[0].text("Kitchen")
c[0].markdown(
        """
        <img src='data:image/png;base64,{}' class='img-fluid' width=50 height=50>""".format(
            img_to_bytes("inspirations/kitchen/inspiration/insp6.jpg")
        ),
        unsafe_allow_html=True,
    )
kitchen = c[0].checkbox("",key=0)

c[1].text("Bathroom")
c[1].markdown(
        """
        <img src='data:image/png;base64,{}' class='img-fluid' width=50 height=50>""".format(
            img_to_bytes("inspirations/bathroom/inspiration/insp1.jpg")
        ),
        unsafe_allow_html=True,
    )
bathroom = c[1].checkbox("",key=1)

c[2].text("Bedroom")
c[2].markdown(
        """
        <img src='data:image/png;base64,{}' class='img-fluid' width=50 height=50>""".format(
            img_to_bytes("inspirations/bedroom/inspiration/insp2.jpg")
        ),
        unsafe_allow_html=True,
    )
bedroom = c[2].checkbox("",key=2)


c[3].text("Entrance")
c[3].markdown(
        """
        <img src='data:image/png;base64,{}' class='img-fluid' width=50 height=50>""".format(
            img_to_bytes("./entrance.jpeg")
        ),
        unsafe_allow_html=True,
    )
entrance = c[3].checkbox("",key=3)

c[4].text("Salon")
c[4].markdown(
        """
        <img src='data:image/png;base64,{}' class='img-fluid' width=50 height=50 style="margin-left :5px;margin-right :5px">""".format(
            img_to_bytes("inspirations/salon/inspiration/insp7.png")
        ),
        unsafe_allow_html=True,
    )
salon = c[4].checkbox("",key=4)

c[5].text("Dining_Room")
c[5].markdown(
        """
        <img src='data:image/png;base64,{}' class='img-fluid' width=50 height=50 style="margin-left :5px ;margin-right :5px">""".format(
            img_to_bytes("inspirations/dining/inspiration/insp3.jpg")
        ),
        unsafe_allow_html=True,
    )


dining = c[5].checkbox("",key=5)
st.subheader("")
st.subheader("")
st.subheader("")

catg = [kitchen,bedroom,dining,bathroom,entrance,salon]
bg = ["kitchen","bedroom","dining","bathroom","entrance","salon"]

paths = []
for cg,bg in zip(catg,bg):
    if cg:
        images = os.listdir(f"./inspirations/{bg}/inspiration/")
        for img in images:
            path = os.path.join(f"./inspirations/{bg}/inspiration/",img)
            paths.append(path)


pts= [paths[i:i+3] for i in range(0,len(paths),3)]

for e in pts:
    c = st.columns(3)
    for idx,path in enumerate(e):
        img = Image.open(path)
        img = img.resize((250, 250))
        v = c[idx].button("✔", c[idx].image(img))

        if v:
            f = open("insp.txt","a+")
            f.write(path+"\n")
            f.close()








st.subheader("")
st.subheader("")
st.subheader("")


if max(catg):
    c = st.columns(5)
    opt = c[2].button("Optimize Budget")
    if opt:
        f = open("insp.txt", "r")
        insps = list(set(f.readlines()))
        f.close()
        os.remove("insp.txt")
        if len(insps) !=0:
            types = []
            inspit = []
            db = pd.read_csv("data.csv")
            bud = int(budget)
            for e in insps:
                e = e.strip()
                types.append(e.split("/")[2])
                inspit.append(e.split("/")[-1].split(".")[0])

            prs = []
            n_items = []

            for t, c in zip(types, inspit):
                pr = db[(db["type"] == t) & (db["inspiration_order"] == c)]["itemp_price"]
                nits = db[(db["type"] == t) & (db["inspiration_order"] == c)]["number_items"]

                n_items.append(int(nits))
                prs.append(int(pr))

            d = {}
            for ins in inspit:
                d[ins] = []
            for p in prs:
                if bud - p > 0:
                    d[inspit[prs.index(p)]].append("principale")
                    bud = bud - p

            for z in n_items:
                if z != 0:
                    dt = db[db["inspiration_order"] == inspit[n_items.index(z)]].iloc[:, 5:5 + z]
                    ob = dt.T.sort_values(by=dt.T.columns[0], ascending=False)
                    for idx in ob[ob.columns[0]].index:
                        if bud - int(dt[idx]) > 0:
                            d[inspit[n_items.index(z)]].append(str(idx))
                            bud = bud - int(dt[idx])
            d["budget"] = bud

            f = []
            prcs = []
            for p in insps:
                its = d[p.split("/")[-1].split(".")[0]]

                els = "./inspirations/"+p.split("/")[2]+"/"+"renders/"
                img_els = os.listdir(els)
                p_img_els = [os.path.join(els,i) for i in img_els if (i.split('.')[0] in its) or (i.split('.')[0]+"_price" in its)]
                f+=p_img_els
                db = pd.read_csv("data.csv")
                aux = db[(db["inspiration_order"]==p.split("/")[-1].split(".")[0])]
                for i in its:
                    if "principale" in i:
                        prcs.append(int(aux["itemp_price"]))
                    else:
                        prcs.append(int(aux[i]))



            ps = [prcs[i:i+3] for i in range(0,len(prcs),3)]
            fs= [f[i:i+3] for i in range(0,len(f),3)]
            st.subheader("")
            st.subheader("")
            st.subheader("")

            i=0
            for e in fs:
                c = st.columns(3)
                for idx, path in enumerate(e):
                    img = Image.open(path)
                    img = img.resize((300, 300))
                    v = c[idx].button(str(prcs[i])+" TND", c[idx].image(img))
                    i+=1

            f = st.columns(3)
            f[1].subheader("Your Balance is: "+str(d["budget"])+" TND")







