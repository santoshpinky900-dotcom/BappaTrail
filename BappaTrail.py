import streamlit as st
import folium
from streamlit_folium import st_folium
import os, base64, html

st.set_page_config(page_title='BappaTrail', page_icon='🪔', layout='wide')
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR=os.path.join(BASE_DIR,'images')

def path(f): return os.path.join(IMAGE_DIR,f)
def exists(f): return os.path.exists(path(f))
def b64(f):
    if not exists(f): return None
    with open(path(f),'rb') as x: return base64.b64encode(x.read()).decode()
def mime(f): return {'png':'image/png','jpg':'image/jpeg','jpeg':'image/jpeg','webp':'image/webp','avif':'image/avif'}.get(f.lower().split('.')[-1],'image/png')
def img(f,h='220px',r='18px'):
    d=b64(f)
    if not d: return f'<div style="height:{h};border:1px solid #8f2424;border-radius:{r};display:flex;align-items:center;justify-content:center;background:#240606;color:#d8b46a;font-weight:700">Image not found</div>'
    return f'<img src="data:{mime(f)};base64,{d}" style="width:100%;height:{h};object-fit:cover;border-radius:{r};display:block">'

G={
'GSB Ganpati':dict(image='gsb.avif',location="King's Circle, Matunga, Mumbai",year='Established 1951; Ganeshotsav began in 1955',lat=19.0275,lon=72.8550,short='A major South Indian GSB community Ganeshotsav known for traditional rituals and seva.',history='GSB Seva Mandal was established in 1951 at King’s Circle. Its public Ganeshotsav began in 1955 with a small 14-inch idol and gradually grew into one of Mumbai’s well-known Ganpati celebrations. The mandal combines devotion with social service, traditional rituals, cultural activities and community participation.',culture='GSB Ganpati represents the cultural heritage of the Gowd Saraswat Brahmin community in Mumbai. The festival brings together devotion, traditional rituals, music, seva and community service.',why='People visit GSB Ganpati to experience its traditional atmosphere, rituals, beautiful decorations and strong connection between Ganeshotsav and community service.',facts=['King’s Circle / Matunga','GSB Seva Mandal','Traditional rituals','Community seva']),
'Chinchpokli Chintamani Ganpati':dict(image='chintamain.png',location='Chinchpokli, Mumbai',year='Established 1920',lat=18.9995,lon=72.8275,short='One of Mumbai’s historic public Ganpati mandals, with a century-long legacy.',history='Chinchpokli Chintamani Sarvajanik Utsav Mandal was established in 1920. Its public Ganeshotsav developed during the period when community festivals were becoming an important part of Mumbai’s social and cultural life. Over the decades, Chintamani has become closely associated with Chinchpokli and is remembered for its long-standing tradition and public participation.',culture='The festival reflects Mumbai’s neighbourhood culture: people from different backgrounds gather together for darshan, cultural activities and community celebration.',why='Devotees visit for the historic legacy, energetic festival atmosphere and the sense of tradition connected with Chinchpokli’s identity.',facts=['Chinchpokli','Established 1920','Historic Mumbai mandal','Community celebration']),
'Girgaoncha Raja':dict(image='GirgaonchaRaja.webp',location='Girgaon, Mumbai',year='Mandal founded 1928',lat=18.9530,lon=72.8170,short='A historic Girgaon Ganeshotsav known for eco-friendly celebration and cultural activities.',history='Nikadwari Lane Sarvajanik Ganeshotsav Mandal, associated with Girgaoncha Raja, was founded in 1928. The mandal has continued its Ganeshotsav tradition while also taking up social, cultural and educational activities. Eco-friendly practices have also been an important part of its public identity.',culture='Girgaoncha Raja represents the close relationship between Ganeshotsav and Girgaon’s rich neighbourhood culture. The festival connects devotion with social and cultural participation.',why='Visitors come for the historic Girgaon atmosphere, darshan, cultural spirit and the mandal’s focus on responsible and community-oriented celebration.',facts=['Girgaon','Founded 1928','Eco-friendly focus','Cultural activities']),
'Kasba Ganpati':dict(image='kasba.webp',location='Kasba Peth, Pune',year='Sarvajanik Ganeshotsav since 1893',lat=18.5196,lon=73.8567,short='The Gram Daivat of Pune and the first honoured Ganpati in Pune’s immersion procession.',history='Kasba Ganpati is traditionally regarded as the Gram Daivat, or presiding deity, of Pune. The public Ganeshotsav tradition associated with the mandal dates to 1893. Kasba Ganpati holds a special place in Pune’s Ganeshotsav because it receives the first honour in the city’s traditional immersion procession.',culture='Kasba Ganpati is deeply connected with Pune’s cultural identity. Its place in the traditional procession demonstrates the historical importance of public Ganeshotsav in the city.',why='Devotees visit to experience one of Pune’s most historically significant Ganpati traditions and to seek darshan of the city’s revered Gram Daivat.',facts=['Kasba Peth, Pune','Gram Daivat of Pune','Public festival since 1893','First honour in procession']),
'Mayureshwar Ganpati':dict(image='-Mayureshwar.webp',location='Morgaon, Pune District',year='Ancient temple tradition',lat=18.2735,lon=74.2555,short='The principal Ashtavinayak temple, traditionally regarded as the first and last stop of the yatra.',history='Mayureshwar, also known as Moreshwar, is the most significant shrine in the Ashtavinayak pilgrimage tradition. The temple is located at Morgaon in Pune district. According to traditional legend, Lord Ganesha appeared as Mayureshwar and defeated the demon Sindhu. The deity is associated with a peacock (mayur), giving the form its name.',culture='Morgaon is an important pilgrimage centre in Maharashtra. The temple’s architecture, rituals, festivals and place in the Ashtavinayak circuit make it a major part of the state’s living religious heritage.',why='Pilgrims visit Morgaon as a central destination in the Ashtavinayak yatra. The temple combines mythology, architecture, ritual and pilgrimage tradition.',facts=['Morgaon','Ashtavinayak','Mayureshwar / Moreshwar','Pilgrimage centre']),
'Mumbai Cha Raja':dict(image='mumbaicharaja.jpg',location='Ganesh Galli, Lalbaug, Mumbai',year='Established 1928',lat=18.9970,lon=72.8310,short='A famous Lalbaug Ganpati mandal with a long tradition of cultural programmes.',history='Lalbaug Sarvajanik Utsav Mandal, popularly associated with Mumbai Cha Raja, was established in 1928. The celebration began in Peru Chawl and later moved to Ganesh Galli in 1938. The mandal became known not only for Ganeshotsav but also for cultural activities such as plays, lectures and folk theatre.',culture='Mumbai Cha Raja shows how public Ganeshotsav became a platform for both devotion and neighbourhood cultural life. Ganesh Galli remains an important part of Lalbaug’s festival landscape.',why='People visit for darshan, the historic Lalbaug atmosphere, cultural heritage and the long-running tradition of public celebration.',facts=['Ganesh Galli, Lalbaug','Established 1928','Cultural programmes','Historic mandal']),
'Lalbaugcha Raja':dict(image='lalbag.avif',location='Lalbaug, Mumbai',year='Established 1934',lat=18.9937,lon=72.8370,short='Mumbai’s iconic Lalbaug Ganpati, famous for its long-standing public devotion and huge annual participation.',history='Lalbaugcha Raja traces its public history to 1934. The story is closely connected with the working communities of Lalbaug and their wish for a permanent marketplace. The Ganpati became a powerful symbol of hope and faith for the local community. Over the decades, Lalbaugcha Raja grew into one of Mumbai’s most visited Ganpati celebrations.',culture='Lalbaugcha Raja represents the relationship between Mumbai’s working-class neighbourhoods, public Ganeshotsav and collective devotion. The festival has also supported social and educational activities over many decades.',why='Devotees visit because of its historic legacy, strong public faith, iconic Lalbaug identity and the atmosphere created by one of Mumbai’s biggest Ganeshotsav gatherings.',facts=['Lalbaug, Mumbai','Established 1934','Iconic public Ganpati','Social & educational activities'])}
ORDER=list(G)

st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:Poppins,sans-serif}.stApp{background:radial-gradient(circle at 70% 5%,rgba(145,18,18,.28),transparent 30%),linear-gradient(135deg,#100202,#260505 45%,#140202);color:#fff7df}.block-container{padding-top:1rem;max-width:1500px}[data-testid="stSidebar"]{background:linear-gradient(180deg,#170202,#2d0505 50%,#120101);border-right:1px solid #8f2424}[data-testid="stSidebar"] *{color:#fff2c7!important}h1,h2,h3,h4{font-family:Cinzel,serif!important;color:#ffe5a1!important}.hero{min-height:180px;border:1px solid #c28a25;border-radius:22px;padding:28px 38px;margin-bottom:18px;background:linear-gradient(90deg,rgba(20,0,0,.95),rgba(95,8,8,.72)),radial-gradient(circle at 80% 50%,#a93a16,#360505 60%,#140101);box-shadow:0 12px 35px #0006}.hero h1{font-size:44px!important;margin:0}.tagline{font-family:Cinzel,serif;color:#ffd979;font-size:19px;font-weight:600}.sub{max-width:760px;color:#ffeede;font-size:14px;margin-top:9px}.section-title{font-family:Cinzel,serif;font-size:27px;color:#ffe3a0;margin:8px 0 3px}.section-sub{color:#d8b9a1;margin-bottom:10px}.card,.detail-box{background:linear-gradient(145deg,rgba(76,8,8,.96),rgba(30,3,3,.98));border:1px solid #9d2929;border-radius:17px;padding:14px;box-shadow:0 8px 25px #0004;margin-bottom:10px}.intro-card{border-color:#d7a62b}.card-title{color:#ffe5a5;font-family:Cinzel,serif;font-size:19px;font-weight:700}.small{color:#cbb1a6;font-size:11px}.quote{border:1px solid #c79420;border-radius:15px;padding:15px;text-align:center;color:#ffd86d;font-family:Cinzel,serif;background:#5b2b031c;margin-top:12px}.trail{border:1px solid #8c2525;border-radius:17px;padding:14px;background:#310404e8;margin-top:15px}.stButton>button{border-radius:11px!important;border:1px solid #b43a3a!important;background:linear-gradient(135deg,#741010,#3c0505)!important;color:#fff2cf!important;font-weight:600!important}.stButton>button:hover{border-color:#e0b23d!important;color:#ffe19a!important}[data-testid="stLinkButton"] a{background:linear-gradient(135deg,#8b1717,#4c0606)!important;border:1px solid #d19a2c!important;color:#ffe9b0!important;border-radius:11px!important;font-weight:700!important}.footer{text-align:center;color:#a98d7c;padding:20px 0 5px;font-size:11px}
</style>''',unsafe_allow_html=True)

if 'selected' not in st.session_state: st.session_state.selected='Ganpati Bappa'
with st.sidebar:
    st.markdown('<div style="text-align:center;padding:10px 0 18px"><div style="font-size:46px">🪔</div><div style="font-family:Cinzel,serif;font-size:29px;color:#ffe3a0;font-weight:700">BappaTrail</div><div style="color:#c9a89a;font-size:12px">Explore • Learn • Discover</div></div>',unsafe_allow_html=True)
    if st.button('🏠  Home',use_container_width=True): st.session_state.selected='Ganpati Bappa';st.rerun()
    if st.button('🗺️  Cultural Trail',use_container_width=True): st.session_state.selected='Cultural Trail';st.rerun()
    if st.button('ℹ️  About Project',use_container_width=True): st.session_state.selected='About';st.rerun()
    st.markdown('<div style="position:fixed;bottom:25px;width:250px;text-align:center;color:#e7bd5d;font-family:Cinzel,serif">॥ गणपती बाप्पा मोरया ॥</div>',unsafe_allow_html=True)

st.markdown('''<div class="hero"><h1>🪔 BappaTrail</h1><div class="tagline">A Cultural Trail of Devotion, Heritage & Tradition</div><div style="width:250px;height:2px;background:linear-gradient(90deg,transparent,#e5b84e,transparent);margin:12px 0"></div><div class="sub">A digital journey through iconic Ganpati temples and public Ganeshotsav spaces across Mumbai, Pune and Maharashtra.</div><div style="margin-top:12px;color:#e8c78e;font-size:13px">॥ गणपती बाप्पा मोरया ॥</div></div>''',unsafe_allow_html=True)

if st.session_state.selected=='About':
    st.markdown('<div class="section-title">About BappaTrail</div><div class="section-sub">Digital documentation of public art, culture and living heritage.</div>',unsafe_allow_html=True)
    st.markdown('<div class="detail-box"><h2>Why this website?</h2><p>BappaTrail is a digital documentation project created to help visitors discover important Ganpati cultural spaces in Maharashtra.</p><p>Instead of presenting only names, the website connects each Bappa with its location, history, cultural significance and visitor information. It combines storytelling, digital mapping and visual presentation in one interactive platform.</p></div>',unsafe_allow_html=True)
    a,b,c=st.columns(3)
    for col,title,text in [(a,'📍 Location','Discover where each Ganpati is located and open the place in Google Maps.'),(b,'📜 Heritage','Read the history and cultural background behind each celebration.'),(c,'🪔 Storytelling','Learn traditional stories and the meaning connected with Lord Ganesha.')]:
        with col: st.markdown(f'<div class="card"><div class="card-title">{title}</div><p>{text}</p></div>',unsafe_allow_html=True)
    if st.button('⬅ Back to Home',use_container_width=True): st.session_state.selected='Ganpati Bappa';st.rerun()
    st.markdown('<div class="footer">BappaTrail • Digital Documentation of Ganpati Heritage</div>',unsafe_allow_html=True);st.stop()

if st.session_state.selected=='Cultural Trail':
    st.markdown('<div class="section-title">🗺️ Bappa Cultural Trail</div><div class="section-sub">Seven documented Ganpati destinations across Mumbai, Pune and Morgaon.</div>',unsafe_allow_html=True)
    m=folium.Map(location=[19.15,73.45],zoom_start=8,tiles='OpenStreetMap',control_scale=True); coords=[]
    for i,n in enumerate(ORDER,1):
        x=G[n];coords.append([x['lat'],x['lon']]);d=b64(x['image'])
        icon=f'''<div style="position:relative;width:55px;height:55px"><div style="width:49px;height:49px;border-radius:50%;border:3px solid #f4c64d;overflow:hidden;background:#250303;box-shadow:0 2px 10px #000a"><img src="data:{mime(x['image'])};base64,{d}" style="width:100%;height:100%;object-fit:cover"></div><div style="position:absolute;right:-5px;top:-8px;width:20px;height:20px;border-radius:50%;background:#a31313;color:white;border:2px solid #ffe29a;text-align:center;font:bold 11px Arial;line-height:16px">{i}</div></div>''' if d else f'<div style="width:40px;height:40px;border-radius:50%;background:#a31313;border:3px solid #f4c64d;color:white;text-align:center;line-height:34px;font:bold 14px Arial">{i}</div>'
        pop=f'<div style="width:220px;font-family:Arial"><h4>{html.escape(n)}</h4><div>📍 {html.escape(x["location"])}</div></div>'
        folium.Marker([x['lat'],x['lon']],tooltip=f'{i}. {n}',popup=folium.Popup(pop,max_width=260),icon=folium.DivIcon(html=icon)).add_to(m)
    folium.PolyLine(coords,color='#d93434',weight=4,opacity=.85,dash_array='9,8').add_to(m)
    st_folium(m,width=None,height=600,returned_objects=[])
    cols=st.columns(4)
    for i,n in enumerate(ORDER,1):
        with cols[(i-1)%4]:
            st.markdown(f'<div class="card">{img(G[n]["image"],"120px")}<div class="card-title" style="font-size:15px;margin-top:7px">{i}. {html.escape(n)}</div><div class="small">📍 {html.escape(G[n]["location"])}</div></div>',unsafe_allow_html=True)
            if st.button(f'Explore {i} →',key=f't{i}',use_container_width=True): st.session_state.selected=n;st.rerun()
    if st.button('⬅ Back to Home',use_container_width=True): st.session_state.selected='Ganpati Bappa';st.rerun()
    st.markdown('<div class="footer">BappaTrail • A digital cultural trail across Maharashtra</div>',unsafe_allow_html=True);st.stop()

L,M,R=st.columns([1.05,2.15,1.45],gap='medium')
with L:
    st.markdown('<div class="section-title">🪔 Quick Explore</div><div class="section-sub">Choose a Bappa to explore.</div>',unsafe_allow_html=True)
    st.markdown(img('gsb.avif','90px','13px'),unsafe_allow_html=True)
    if st.button('📖  Introduction to Lord Ganesha',key='intro',use_container_width=True): st.session_state.selected='Ganpati Bappa';st.rerun()
    st.caption('Story • elephant head • worship • quick facts')
    for i,n in enumerate(ORDER,1):
        x=G[n];d=b64(x['image'])
        if d: st.markdown(f'<div style="display:flex;gap:9px;align-items:center;border:1px solid #7f2020;border-radius:11px;padding:6px;margin:4px 0;background:#2b0505"><img src="data:{mime(x["image"])};base64,{d}" style="width:45px;height:45px;border-radius:50%;object-fit:cover;border:2px solid #d6a53d"><div><div style="color:#ffe2a0;font-weight:700;font-size:12px">{i}. {html.escape(n)}</div><div style="color:#bfa397;font-size:9px">{html.escape(x["location"])}</div></div></div>',unsafe_allow_html=True)
        if st.button(f'Explore {i} →',key=f'q{i}',use_container_width=True): st.session_state.selected=n;st.rerun()

with M:
    sel=st.session_state.selected
    if sel=='Ganpati Bappa':
        st.markdown('<div class="card intro-card"><div class="card-title" style="font-size:26px">Introduction to Lord Ganesha</div><div style="color:#e9c99d;font-style:italic">The Divine Guide • Wisdom • New Beginnings</div></div>',unsafe_allow_html=True)
        tabs=st.tabs(['📜 The Story','🐘 Why Elephant Head?','🙏 Why Worshipped?','✨ Quick Facts'])
        with tabs[0]: st.markdown('<div class="detail-box"><h3>🌺 The Story of Lord Ganesha</h3><p>Lord Ganesha, also known as Ganapati, is one of the most widely worshipped deities in Hindu tradition. Traditional stories describe him as the son of Goddess Parvati and Lord Shiva.</p><p>Ganesha is associated with wisdom, knowledge, intelligence and the removal of obstacles. His stories are often told as lessons about devotion, patience, responsibility and good judgement.</p><p>This is why people traditionally remember Ganesha at the beginning of important activities and new journeys.</p></div>',unsafe_allow_html=True)
        with tabs[1]: st.markdown('<div class="detail-box"><h3>🐘 Why does Bappa have an elephant head?</h3><p>A famous traditional story tells that Goddess Parvati created Ganesha and asked him to guard her. When Lord Shiva arrived, Ganesha stopped him because he did not know him as his father.</p><p>A conflict followed and Ganesha lost his original head. Seeing Parvati’s grief, Shiva promised to restore Ganesha’s life. According to the traditional story, an elephant’s head was placed on Ganesha, giving him the form worshipped today.</p><p>Symbolically, the elephant head is associated with wisdom, strength, patience, intelligence and the ability to overcome difficulties.</p></div>',unsafe_allow_html=True)
        with tabs[2]: st.markdown('<div class="detail-box"><h3>🙏 Why is Ganpati worshipped?</h3><p>Ganesha is traditionally worshipped as the remover of obstacles and the deity of wisdom and auspicious beginnings.</p><p>Devotees seek blessings before studies, examinations, careers, business, journeys, ceremonies and other important beginnings.</p><p>Ganesh Chaturthi also turns individual devotion into a community celebration through art, music, decoration, cultural programmes, social service and public participation.</p></div>',unsafe_allow_html=True)
        with tabs[3]:
            for f in ['Also known as Ganapati, Vinayaka and Vighnaharta','Associated with wisdom and new beginnings','Ganesh Chaturthi is a major annual festival','The mouse is traditionally his vahana (vehicle)','Modak is traditionally associated with Ganesha','His worship is popular across many regions of India']: st.markdown('🔸 '+f)
        st.markdown('<div class="quote">“Ganpati Bappa represents hope, wisdom, learning and new beginnings.”</div>',unsafe_allow_html=True)
    else:
        x=G[sel];st.markdown(f'<div class="section-title">{html.escape(sel)}</div><div class="section-sub">📍 {html.escape(x["location"])} • {html.escape(x["year"])}</div>',unsafe_allow_html=True)
        st.markdown(img(x['image'],'250px'),unsafe_allow_html=True)
        tabs=st.tabs(['📜 History','🌺 Cultural Significance','🙏 Why Visit?','✨ Quick Facts'])
        with tabs[0]: st.markdown(f'<div class="detail-box"><h3>📜 History</h3><p>{html.escape(x["history"])}</p></div>',unsafe_allow_html=True)
        with tabs[1]: st.markdown(f'<div class="detail-box"><h3>🌺 Cultural Significance</h3><p>{html.escape(x["culture"])}</p></div>',unsafe_allow_html=True)
        with tabs[2]: st.markdown(f'<div class="detail-box"><h3>🙏 Why devotees visit</h3><p>{html.escape(x["why"])}</p></div>',unsafe_allow_html=True)
        with tabs[3]:
            st.markdown('<div class="detail-box">',unsafe_allow_html=True)
            for f in x['facts']: st.markdown(f'🔸 **{f}**')
            st.markdown('</div>',unsafe_allow_html=True)
        st.link_button('📍 Open Location in Google Maps',f'https://www.google.com/maps/search/?api=1&query={x["lat"]},{x["lon"]}')
        if st.button('⬅ Back to Bappa Introduction',use_container_width=True): st.session_state.selected='Ganpati Bappa';st.rerun()

with R:
    st.markdown('<div class="section-title" style="font-size:22px">🗺️ Bappa Cultural Trail</div><div class="section-sub">Small circular Ganpati images mark the locations.</div>',unsafe_allow_html=True)
    m=folium.Map(location=[19.10,73.15],zoom_start=8,tiles='OpenStreetMap',control_scale=True);coords=[]
    for i,n in enumerate(ORDER,1):
        x=G[n];coords.append([x['lat'],x['lon']]);d=b64(x['image'])
        icon=f'''<div style="position:relative;width:52px;height:52px"><div style="width:46px;height:46px;border-radius:50%;border:3px solid #f4c64d;overflow:hidden;background:#250303"><img src="data:{mime(x['image'])};base64,{d}" style="width:100%;height:100%;object-fit:cover"></div><div style="position:absolute;right:-5px;top:-7px;width:19px;height:19px;border-radius:50%;background:#a31313;color:white;border:2px solid #ffe29a;text-align:center;font:bold 10px Arial;line-height:15px">{i}</div></div>''' if d else f'<div style="width:38px;height:38px;border-radius:50%;background:#a31313;border:3px solid #f4c64d;color:white;text-align:center;line-height:32px;font:bold 13px Arial">{i}</div>'
        folium.Marker([x['lat'],x['lon']],tooltip=f'{i}. {n}',popup=folium.Popup(f'<b>{html.escape(n)}</b><br>📍 {html.escape(x["location"])}',max_width=250),icon=folium.DivIcon(html=icon)).add_to(m)
    folium.PolyLine(coords,color='#d93434',weight=4,opacity=.85,dash_array='9,8').add_to(m)
    st_folium(m,width=None,height=560,returned_objects=[])

st.markdown('<div class="trail"><div class="section-title" style="font-size:20px">📍 Your Maharashtra Bappa Trail</div><div class="small">7 iconic Ganpatis • Mumbai • Pune • Morgaon • One digital journey</div></div>',unsafe_allow_html=True)
cols=st.columns(7)
for i,n in enumerate(ORDER):
    with cols[i]:
        d=b64(G[n]['image'])
        if d: st.markdown(f'<div style="text-align:center"><img src="data:{mime(G[n]["image"])};base64,{d}" style="width:58px;height:58px;border-radius:50%;object-fit:cover;border:3px solid #d6a53d"><div style="font-size:9px;color:#ffe0a0;font-weight:600">{i+1}. {html.escape(n)}</div></div>',unsafe_allow_html=True)
st.markdown('<div class="footer">BappaTrail | Digital Documentation of Public Art & Cultural Spaces | ॥ गणपती बाप्पा मोरया ॥</div>',unsafe_allow_html=True)
