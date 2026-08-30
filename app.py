import streamlit as st
import time
import pandas as pd

# --- 1. PAGE CONFIGURATION & TRANSLATIONS ---
st.set_page_config(page_title="AgriConnect", layout="wide")

# Massive Translation Dictionary for full app coverage
t = {
    "English": {
        "home": "🌾 Welcome to AgriConnect", "f_box": "👨‍🌾 Farmer", "f_desc": "List your fresh harvest.",
        "feat_box": "🛠️ Features", "feat_desc": "Schemes, AI, Q&A.", "b_box": "🛒 Customer", "b_desc": "Buy fresh produce.",
        "open": "Open", "back": "⬅️ Back to Home", "buy_now": "Buy Now", "checkout": "Checkout",
        "f_title": "👨‍🌾 Farmer Portal", "b_title": "🛒 Buyer Storefront", "feat_title": "🛠️ Helpful Features",
        "f_tabs": ["➕ Add Crop", "📊 Dashboard", "🧮 Profit", "🚚 Truck Pooling"],
        "feat_tabs": ["🏛️ Schemes", "🧪 Inputs", "📖 Guide", "🤝 B2B", "🌿 AI", "💬 Q&A Forum"],
        "demand": "🚨 High Demand Alert: Onion searches are up 40% this week. Consider planting for higher margins!",
        "voice_search": "🔍 Search for a crop (🎤 Voice Enabled)", "voice_btn": "🎤 Speak",
        "add_crop": "List Crop", "calc": "Calculate", "cart_total": "Cart Total: ₹",
        "pool_title": "🚚 Active Truck Pools", "pool_btn": "Join Transport",
        "qa_title": "Community Q&A", "qa_input": "Ask the community (🎤 Voice Enabled)...",
        "success": "🎉 Order Placed Successfully!"
    },
    "తెలుగు": {
        "home": "🌾 అగ్రి కనెక్ట్‌కు స్వాగతం", "f_box": "👨‍🌾 రైతు", "f_desc": "మీ పంటను ఇక్కడ అమ్మండి.",
        "feat_box": "🛠️ ఫీచర్లు", "feat_desc": "పథకాలు, AI, Q&A.", "b_box": "🛒 కస్టమర్", "b_desc": "తాజా కూరగాయలు కొనండి.",
        "open": "తెరువు", "back": "⬅️ వెనుకకు", "buy_now": "కొనుగోలు చేయండి", "checkout": "చెక్అవుట్",
        "f_title": "👨‍🌾 రైతు పోర్టల్", "b_title": "🛒 కస్టమర్ పోర్టల్", "feat_title": "🛠️ ఇతర ఫీచర్లు",
        "f_tabs": ["➕ పంట జోడించు", "📊 డాష్‌బోర్డ్", "🧮 లాభం", "🚚 ట్రక్ పూలింగ్"],
        "feat_tabs": ["🏛️ పథకాలు", "🧪 మందులు", "📖 గైడ్", "🤝 B2B", "🌿 AI", "💬 రైతుల చర్చ"],
        "demand": "🚨 డిమాండ్ అలర్ట్: ఉల్లిపాయల అన్వేషణ 40% పెరిగింది. ఎక్కువ లాభం కోసం ప్లాన్ చేయండి!",
        "voice_search": "🔍 పంటలను వెతకండి (🎤 వాయిస్)", "voice_btn": "🎤 మాట్లాడండి",
        "add_crop": "పంటను జోడించు", "calc": "లెక్కించు", "cart_total": "మొత్తం: ₹",
        "pool_title": "🚚 ట్రక్ పూలింగ్ (రవాణా భాగస్వామ్యం)", "pool_btn": "ట్రక్‌లో చేరండి",
        "qa_title": "రైతుల ప్రశ్నలు-జవాబులు", "qa_input": "సందేహాలు అడగండి (🎤 వాయిస్)...",
        "success": "🎉 ఆర్డర్ విజయవంతమైంది!"
    },
    "हिंदी": {
        "home": "🌾 एग्रीकनेक्ट में आपका स्वागत है", "f_box": "👨‍🌾 किसान", "f_desc": "अपनी फसल यहाँ बेचें।",
        "feat_box": "🛠️ विशेषताएं", "feat_desc": "योजनाएं, AI, Q&A.", "b_box": "🛒 ग्राहक", "b_desc": "ताजा सब्जियां खरीदें।",
        "open": "खोलें", "back": "⬅️ वापस", "buy_now": "अभी खरीदें", "checkout": "चेकआउट",
        "f_title": "👨‍🌾 किसान पोर्टल", "b_title": "🛒 ग्राहक पोर्टल", "feat_title": "🛠️ अन्य विशेषताएं",
        "f_tabs": ["➕ फसल जोड़ें", "📊 डैशबोर्ड", "🧮 लाभ", "🚚 ट्रक पूलिंग"],
        "feat_tabs": ["🏛️ योजनाएं", "🧪 इनपुट", "📖 गाइड", "🤝 B2B", "🌿 AI", "💬 Q&A फोरम"],
        "demand": "🚨 डिमांड अलर्ट: प्याज की खोज 40% बढ़ गई है। अधिक लाभ के लिए योजना बनाएं!",
        "voice_search": "🔍 फसल खोजें (🎤 वॉयस)", "voice_btn": "🎤 बोलें",
        "add_crop": "फसल जोड़ें", "calc": "गणना करें", "cart_total": "कुल: ₹",
        "pool_title": "🚚 ट्रक पूलिंग", "pool_btn": "परिवहन में शामिल हों",
        "qa_title": "समुदाय Q&A", "qa_input": "समुदाय से पूछें (🎤 वॉयस)...",
        "success": "🎉 ऑर्डर सफल रहा!"
    }
}

# --- 2. STATE MANAGEMENT ---
if 'current_page' not in st.session_state: st.session_state.current_page = "Home"
if 'farmer_cart' not in st.session_state: st.session_state.farmer_cart = []
if 'buyer_cart' not in st.session_state: st.session_state.buyer_cart = []
if 'language' not in st.session_state: st.session_state.language = "English"

if 'market_items' not in st.session_state:
    st.session_state.market_items = [
        {"farmer": "Ramesh", "crop": "Tomatoes", "price": 30, "stock": 50, "emoji": "🍅", "sales": 1500, "rating": 4.8, "orders": 120},
        {"farmer": "Suresh", "crop": "Onions", "price": 35, "stock": 200, "emoji": "🧅", "sales": 0, "rating": 4.5, "orders": 85},
    ]

def change_page(page_name): st.session_state.current_page = page_name
def add_to_cart(c_type, name, price): st.session_state[f"{c_type}_cart"].append({"name": name, "price": price})
def checkout(c_type): 
    st.session_state.last_order = st.session_state[f"{c_type}_cart"].copy()
    st.session_state[f"{c_type}_cart"] = []
    st.session_state.current_page = "Success"

# --- 3. SIDEBAR ---
st.sidebar.title("🌐 Language / భాష")
st.session_state.language = st.sidebar.selectbox("Select Language:", ["English", "తెలుగు", "हिंदी"])
lang = st.session_state.language
lang_dict = t[lang]

# --- 4. HOME PAGE ---
if st.session_state.current_page == "Home":
    st.title(lang_dict["home"]); st.write("---") 
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.title(lang_dict["f_box"]); st.write(lang_dict["f_desc"])
            st.button(lang_dict["open"], key="btn_f", on_click=change_page, args=("Farmer",), use_container_width=True, type="primary")
    with col2:
        with st.container(border=True):
            st.title(lang_dict["feat_box"]); st.write(lang_dict["feat_desc"])
            st.button(lang_dict["open"], key="btn_feat", on_click=change_page, args=("Features",), use_container_width=True, type="primary")
    with col3:
        with st.container(border=True):
            st.title(lang_dict["b_box"]); st.write(lang_dict["b_desc"])
            st.button(lang_dict["open"], key="btn_b", on_click=change_page, args=("Buyer",), use_container_width=True, type="primary")

# --- 5. FARMER PORTAL ---
elif st.session_state.current_page == "Farmer":
    st.button(lang_dict["back"], on_click=change_page, args=("Home",))
    st.title(lang_dict["f_title"])
    st.warning(lang_dict["demand"]) # DEMAND ALERT FEATURE
    
    tab1, tab2, tab3, tab4 = st.tabs(lang_dict["f_tabs"])
    
    with tab1:
        with st.form("add_crop"):
            farmer_name = st.text_input("Name")
            crop_name = st.text_input("Crop (🎤 Voice Support)")
            emoji = st.text_input("Emoji", value="🍎")
            price = st.number_input("Price (₹)", min_value=1)
            stock = st.number_input("Stock (kg)", min_value=1)
            if st.form_submit_button(lang_dict["add_crop"]) and farmer_name:
                st.session_state.market_items.append({"farmer": farmer_name, "crop": crop_name, "price": price, "stock": stock, "emoji": emoji, "sales": 0, "rating": "New", "orders": 0})
                st.success("✅ Added!")
                
    with tab2:
        st.subheader("Analytics")
        dashboard_name = st.text_input("Enter your name:", value="Ramesh")
        my_items = [item for item in st.session_state.market_items if item['farmer'].lower() == dashboard_name.lower()]
        if my_items:
            st.metric(label="Earnings", value=f"₹{sum(item.get('sales', 0) for item in my_items)}")
            st.line_chart(pd.DataFrame({"Tomatoes (₹)": [25, 28, 30, 32, 30], "Onions (₹)": [40, 38, 35, 34, 35]}))
            
    with tab3:
        acres = st.number_input("Acres", value=1.0)
        yield_kg = st.number_input("Yield/Acre", value=2000)
        price_est = st.number_input("Price/kg", value=30)
        if st.button(lang_dict["calc"], type="primary"):
            st.success(f"💰 Projected Revenue: **₹{(acres * yield_kg) * price_est:,.2f}**")

    with tab4: # TRUCK POOLING FEATURE
        st.subheader(lang_dict["pool_title"])
        with st.container(border=True):
            st.write("🚚 **Route:** Mallapur ➡️ Secunderabad Market")
            st.progress(60); st.caption("Capacity: 600kg / 1000kg filled | Driver: Kumar")
            st.button(lang_dict["pool_btn"], key="t1")
        with st.container(border=True):
            st.write("🚚 **Route:** Ibrahimpatnam ➡️ LB Nagar")
            st.progress(90); st.caption("Capacity: 900kg / 1000kg filled | Driver: Singh")
            st.button(lang_dict["pool_btn"], key="t2")

# --- 6. FEATURES PORTAL ---
elif st.session_state.current_page == "Features":
    st.button(lang_dict["back"], on_click=change_page, args=("Home",))
    st.title(lang_dict["feat_title"])
    
    t1, t2, t3, t4, t5, t6 = st.tabs(lang_dict["feat_tabs"])
    
    with t1: st.write("✅ PM-KISAN, KCC, AIF Links Here")
    with t2: 
        st.button("Neem Oil - ₹250", on_click=add_to_cart, args=("farmer", "Neem Oil", 250))
        if st.session_state.farmer_cart:
            st.write(f"**{lang_dict['cart_total']} {sum(i['price'] for i in st.session_state.farmer_cart)}**")
            st.button(lang_dict["buy_now"], on_click=checkout, args=("farmer",))
    with t3: st.write("📖 Soil & Water Guides Here")
    with t4: st.write("🏢 Active Taj Hotel Contract: 500kg Onions")
    with t5: st.file_uploader("Upload Leaf Image")
    
    with t6: # Q&A FORUM FEATURE
        st.subheader(lang_dict["qa_title"])
        with st.chat_message("user"): st.write("How do I protect tomatoes from heavy rain?")
        with st.chat_message("assistant"): st.write("Ensure proper field drainage and use raised beds. - *Farmer Suresh*")
        st.chat_input(lang_dict["qa_input"])

# --- 7. BUYER PORTAL ---
elif st.session_state.current_page == "Buyer":
    st.button(lang_dict["back"], on_click=change_page, args=("Home",))
    st.title(lang_dict["b_title"])
    
    c1, c2 = st.columns([3, 1])
    with c1: search = st.text_input(lang_dict["voice_search"]) # VOICE ACCESSIBILITY UI
    with c2: st.button(lang_dict["voice_btn"])
    
    cols = st.columns(3)
    for i, item in enumerate(st.session_state.market_items):
        with cols[i % 3]:
            with st.container(border=True):
                st.write(f"### {item['emoji']} {item['crop']}")
                st.write(f"👨‍🌾 {item['farmer']} | ⭐ {item['rating']}")
                st.button(f"₹{item['price']} - Add", key=f"b_{i}", on_click=add_to_cart, args=("buyer", item['crop'], item['price']))
                
    if st.session_state.buyer_cart:
        st.write(f"**{lang_dict['cart_total']} {sum(i['price'] for i in st.session_state.buyer_cart)}**")
        st.button(lang_dict["checkout"], on_click=checkout, args=("buyer",))

# --- 8. SUCCESS ---
elif st.session_state.current_page == "Success":
    st.balloons(); st.title(lang_dict["success"])
    st.button(lang_dict["back"], on_click=change_page, args=("Home",))