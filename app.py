import streamlit as st
import time
import pandas as pd

# --- 1. PAGE CONFIGURATION & TRANSLATIONS ---
st.set_page_config(page_title="AgriConnect", layout="wide")

t = {
    "English": {
        "home": "🌾 Welcome to AgriConnect", "f_box": "👨‍🌾 Farmer", "f_desc": "List your fresh harvest directly to the market.",
        "feat_box": "🛠️ Helpful Features", "feat_desc": "Government schemes, B2B contracts, and AI tools.", "b_box": "🛒 Customer", "b_desc": "Browse fresh produce directly from local farms.",
        "open": "Open Portal", "back": "⬅️ Back to Home", "buy_now": "Buy Now", "checkout": "Checkout & Buy",
        "f_title": "👨‍🌾 Farmer Portal", "b_title": "🛒 Buyer Storefront", "feat_title": "🛠️ Helpful Features",
        "f_tabs": ["➕ Add New Crop", "📊 My Dashboard", "🧮 Profit Estimator", "🚚 Truck Pooling"],
        "feat_tabs": ["🏛️ Schemes", "🧪 Inputs", "📖 Guide", "🤝 B2B Contracts", "🌿 Crop AI", "💬 Q&A Forum"],
        "demand": "🚨 High Demand Alert: Onion searches are up 40% this week. Consider planting for higher margins!",
        "search_ph": "🔍 Search for a crop (🎤 Voice Enabled)", "voice_btn": "🎤 Speak",
        "add_crop": "List Crop", "calc": "Calculate Expected Revenue", "cart_total": "Cart Total: ₹",
        "pool_title": "🚚 Active Truck Pools", "pool_btn": "Join Transport",
        "qa_title": "Community Q&A", "qa_input": "Ask the community (🎤 Voice Enabled)...",
        "success": "🎉 Order Placed Successfully!", "invoice": "🧾 Auto-Generated Digital Invoice", "delivery": "🚚 Active Deliveries",
        "smart_cmd": "🎤 Click to Record Voice Command"
    },
    "తెలుగు": {
        "home": "🌾 అగ్రి కనెక్ట్‌కు స్వాగతం", "f_box": "👨‍🌾 రైతు", "f_desc": "మీ పంటను నేరుగా మార్కెట్‌లో జాబితా చేయండి.",
        "feat_box": "🛠️ ఫీచర్లు", "feat_desc": "ప్రభుత్వ పథకాలు, B2B కాంట్రాక్ట్‌లు మరియు AI టూల్స్.", "b_box": "🛒 కస్టమర్", "b_desc": "స్థానిక రైతుల నుండి నేరుగా కొనుగోలు చేయండి.",
        "open": "తెరువు", "back": "⬅️ వెనుకకు", "buy_now": "కొనుగోలు చేయండి", "checkout": "చెక్అవుట్",
        "f_title": "👨‍🌾 రైతు పోర్టల్", "b_title": "🛒 కస్టమర్ పోర్టల్", "feat_title": "🛠️ ఇతర ఫీచర్లు",
        "f_tabs": ["➕ పంట జోడించు", "📊 డాష్‌బోర్డ్", "🧮 లాభం", "🚚 ట్రక్ పూలింగ్"],
        "feat_tabs": ["🏛️ పథకాలు", "🧪 మందులు", "📖 గైడ్", "🤝 B2B", "🌿 AI", "💬 రైతుల చర్చ"],
        "demand": "🚨 డిమాండ్ అలర్ట్: ఉల్లిపాయల అన్వేషణ 40% పెరిగింది. ఎక్కువ లాభం కోసం ప్లాన్ చేయండి!",
        "search_ph": "🔍 పంటలను వెతకండి (🎤 వాయిస్)", "voice_btn": "🎤 మాట్లాడండి",
        "add_crop": "పంటను జోడించు", "calc": "రెవెన్యూ లెక్కించు", "cart_total": "మొత్తం: ₹",
        "pool_title": "🚚 ట్రక్ పూలింగ్ (రవాణా భాగస్వామ్యం)", "pool_btn": "ట్రక్‌లో చేరండి",
        "qa_title": "రైతుల ప్రశ్నలు-జవాబులు", "qa_input": "సందేహాలు అడగండి (🎤 వాయిస్)...",
        "success": "🎉 ఆర్డర్ విజయవంతమైంది!", "invoice": "🧾 డిజిటల్ రశీదు", "delivery": "🚚 యాక్టివ్ డెలివరీలు",
        "smart_cmd": "🎤 వాయిస్ కమాండ్ రికార్డ్ చేయడానికి క్లిక్ చేయండి"
    },
    "हिंदी": {
        "home": "🌾 एग्रीकनेक्ट में आपका स्वागत है", "f_box": "👨‍🌾 किसान", "f_desc": "अपनी ताजा फसल सीधे बाजार में सूचीबद्ध करें।",
        "feat_box": "🛠️ विशेषताएं", "feat_desc": "सरकारी योजनाएं, B2B अनुबंध और AI टूल।", "b_box": "🛒 ग्राहक", "b_desc": "सीधे स्थानीय खेतों से ताजा उपज ब्राउज़ करें।",
        "open": "खोलें", "back": "⬅️ वापस", "buy_now": "अभी खरीदें", "checkout": "चेकआउट",
        "f_title": "👨‍🌾 किसान पोर्टल", "b_title": "🛒 ग्राहक पोर्टल", "feat_title": "🛠️ अन्य विशेषताएं",
        "f_tabs": ["➕ फसल जोड़ें", "📊 डैशबोर्ड", "🧮 लाभ", "🚚 ट्रक पूलिंग"],
        "feat_tabs": ["🏛️ योजनाएं", "🧪 इनपुट", "📖 गाइड", "🤝 B2B", "🌿 AI", "💬 Q&A फोरम"],
        "demand": "🚨 डिमांड अलर्ट: प्याज की खोज 40% बढ़ गई है। अधिक लाभ के लिए योजना बनाएं!",
        "search_ph": "🔍 फसल खोजें (🎤 वॉयस)", "voice_btn": "🎤 बोलें",
        "add_crop": "फसल जोड़ें", "calc": "राजस्व की गणना करें", "cart_total": "कुल: ₹",
        "pool_title": "🚚 ट्रक पूलिंग", "pool_btn": "परिवहन में शामिल हों",
        "qa_title": "समुदाय Q&A", "qa_input": "समुदाय से पूछें (🎤 वॉयस)...",
        "success": "🎉 ऑर्डर सफल रहा!", "invoice": "🧾 डिजिटल चालान", "delivery": "🚚 सक्रिय डिलीवरी",
        "smart_cmd": "🎤 वॉयस कमांड रिकॉर्ड करने के लिए क्लिक करें"
    }
}

# --- 2. STATE MANAGEMENT & DATABASE ---
if 'current_page' not in st.session_state: st.session_state.current_page = "Home"
if 'crop_added' not in st.session_state: st.session_state.crop_added = False
if 'farmer_cart' not in st.session_state: st.session_state.farmer_cart = []
if 'buyer_cart' not in st.session_state: st.session_state.buyer_cart = []
if 'last_order' not in st.session_state: st.session_state.last_order = []
if 'language' not in st.session_state: st.session_state.language = "English"

if 'market_items' not in st.session_state:
    st.session_state.market_items = [
        {"farmer": "Ramesh", "crop": "Tomatoes", "price": 30, "stock": 50, "emoji": "🍅", "sales": 1500, "rating": 4.8, "orders": 120},
        {"farmer": "Suresh", "crop": "Onions", "price": 35, "stock": 200, "emoji": "🧅", "sales": 0, "rating": 4.5, "orders": 85},
    ]

def change_page(page_name):
    st.session_state.current_page = page_name
    st.session_state.crop_added = False

def reset_add_crop(): st.session_state.crop_added = False

def add_to_cart(cart_type, item_name, price):
    st.session_state[f"{cart_type}_cart"].append({"name": item_name, "price": price})

def checkout(cart_type):
    st.session_state.last_order = st.session_state[f"{cart_type}_cart"].copy()
    st.session_state[f"{cart_type}_cart"] = []
    st.session_state.current_page = "Success"

# --- 3. SIDEBAR (LANGUAGE SELECTOR) ---
st.sidebar.title("🌐 Language / భాష")
st.session_state.language = st.sidebar.selectbox("Select Display Language:", ["English", "తెలుగు", "हिंदी"])
lang = st.session_state.language
lang_dict = t[lang]

# --- 4. HOME PAGE ---
if st.session_state.current_page == "Home":
    st.title(lang_dict["home"])
    st.write("---") 
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.title(lang_dict["f_box"]); st.write(lang_dict["f_desc"]); st.write("") 
            st.button(lang_dict["open"], key="btn_f", on_click=change_page, args=("Farmer",), use_container_width=True, type="primary")
    with col2:
        with st.container(border=True):
            st.title(lang_dict["feat_box"]); st.write(lang_dict["feat_desc"]); st.write("")
            st.button(lang_dict["open"], key="btn_feat", on_click=change_page, args=("Features",), use_container_width=True, type="primary")
    with col3:
        with st.container(border=True):
            st.title(lang_dict["b_box"]); st.write(lang_dict["b_desc"]); st.write("")
            st.button(lang_dict["open"], key="btn_b", on_click=change_page, args=("Buyer",), use_container_width=True, type="primary")

# --- 5. FARMER PORTAL ---
elif st.session_state.current_page == "Farmer":
    st.button(lang_dict["back"], on_click=change_page, args=("Home",))
    st.title(lang_dict["f_title"])
    st.warning(lang_dict["demand"])
    
    tab1, tab2, tab3, tab4 = st.tabs(lang_dict["f_tabs"])
    
    with tab1:
        st.write("### 🗣️ Smart Voice Assistant")
        smart_name = st.text_input("Your Name (For Voice Listing)", value="Ramesh")
        
        # REAL MICROPHONE WIDGET
        audio_value = st.audio_input(lang_dict["smart_cmd"])
        
        if audio_value:
            with st.spinner("🎙️ AI processing voice..."):
                time.sleep(2) # Simulating upload and processing time
                
                # Hackathon Demo Magic: Cycles through your script perfectly
                if 'voice_demo_count' not in st.session_state: st.session_state.voice_demo_count = 0
                
                demo_commands = [
                    ("Tomato", 10, 60, "🍅"),
                    ("Potato", 8, 50, "🥔"),
                    ("Rice", 20, 100, "🌾"),
                    ("Onion", 15, 99, "🧅")
                ]
                
                crop_val, stock_val, price_val, emoji_val = demo_commands[st.session_state.voice_demo_count % len(demo_commands)]
                st.session_state.voice_demo_count += 1
                
                st.session_state.market_items.append({"farmer": smart_name, "crop": crop_val, "price": price_val, "stock": stock_val, "emoji": emoji_val, "sales": 0, "rating": "New", "orders": 0})
                
                st.success(f"✅ **Transcribed Voice:** 'List {stock_val}kg {crop_val} for {price_val} rupees'")
                st.info(f"Successfully listed {stock_val}kg of {crop_val} to the market!")
                
        st.write("---")
        st.write("### ✍️ Manual Entry")
        if not st.session_state.crop_added:
            with st.form("add_crop"):
                farmer_name = st.text_input("Your Name")
                crop_name = st.text_input("Crop Name")
                emoji = st.text_input("Crop Emoji (e.g., 🍎)", value="🍎")
                price = st.number_input("Price per kg (₹)", min_value=1)
                stock = st.number_input("Available Stock (kg)", min_value=1)
                if st.form_submit_button(lang_dict["add_crop"]) and farmer_name and crop_name:
                    st.session_state.market_items.append({"farmer": farmer_name, "crop": crop_name, "price": price, "stock": stock, "emoji": emoji, "sales": 0, "rating": "New", "orders": 0})
                    st.session_state.crop_added = True
                    st.rerun()
        else:
            st.success("✅ Crop successfully listed on the live market!")
            st.button("➕ Add Another Crop", on_click=reset_add_crop)
            
    with tab2:
        st.subheader("Farm Analytics")
        dashboard_name = st.text_input("Enter your name to view your dashboard:", value="Ramesh")
        my_items = [item for item in st.session_state.market_items if item['farmer'].lower() == dashboard_name.lower()]
        if my_items:
            st.metric(label="Total Projected Earnings", value=f"₹{sum(item.get('sales', 0) for item in my_items)}")
            st.write("### 📈 Live Market Price Trends")
            st.line_chart(pd.DataFrame({"Tomatoes (₹/kg)": [25, 28, 30, 32, 30], "Onions (₹/kg)": [40, 38, 35, 34, 35]}, index=["Mon", "Tue", "Wed", "Thu", "Fri"]))
            st.write("### 📦 Your Active Listings")
            for item in my_items:
                with st.container(border=True):
                    st.write(f"**{item['emoji']} {item['crop']}** | Price: ₹{item['price']}/kg | Stock: {item['stock']}kg")
        else:
            st.info("No listings found for this name yet.")
            
    with tab3:
        st.subheader("Yield & Profit Estimator")
        acres = st.number_input("Land Size (Acres)", min_value=0.1, value=1.0)
        yield_per_acre = st.number_input("Expected Yield per Acre (kg)", min_value=50, value=2000)
        est_price = st.number_input("Expected Selling Price (₹/kg)", min_value=1, value=30)
        if st.button(lang_dict["calc"], type="primary"):
            st.success(f"🌾 Estimated Harvest: **{acres * yield_per_acre:,.0f} kg**")
            st.info(f"💰 Projected Revenue: **₹{(acres * yield_per_acre) * est_price:,.2f}**")

    with tab4:
        st.subheader(lang_dict["pool_title"])
        with st.container(border=True):
            st.write("🚚 **Route:** Mallapur ➡️ Secunderabad Market")
            st.progress(60); st.caption("Capacity: 600kg / 1000kg filled | Driver: Kumar")
            st.button(lang_dict["pool_btn"], key="t1")
        with st.container(border=True):
            st.write("🚚 **Route:** Ibrahimpatnam ➡️ LB Nagar")
            st.progress(90); st.caption("Capacity: 900kg / 1000kg filled | Driver: Singh")
            st.button(lang_dict["pool_btn"], key="t2")

# --- 6. OTHER HELPFUL FEATURES ---
elif st.session_state.current_page == "Features":
    st.button(lang_dict["back"], on_click=change_page, args=("Home",))
    st.title(lang_dict["feat_title"])
    
    t1, t2, t3, t4, t5, t6 = st.tabs(lang_dict["feat_tabs"])
    
    with t1:
        st.subheader("Financial Support & Subsidies")
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.write("### PM-KISAN Samman Nidhi")
                st.button("Check PM-KISAN Status")
            with st.container(border=True):
                st.write("### Kisan Credit Card (KCC)")
                st.button("Apply for KCC Loan")
        with col2:
            with st.container(border=True):
                st.write("### Agriculture Infrastructure Fund")
                st.button("Apply for AIF")
            with st.container(border=True):
                st.write("### PM Fasal Bima Yojana")
                st.button("Calculate Insurance Premium")
                
    with t2:
        st.subheader("Direct Input Ordering")
        p_col1, p_col2, p_col3 = st.columns(3)
        with p_col1:
            with st.container(border=True):
                st.write("### 🌿 Neem Oil (1L)")
                st.button("Add - ₹250", key="i1", on_click=add_to_cart, args=("farmer", "Neem Oil (1L)", 250), use_container_width=True)
            with st.container(border=True):
                st.write("### 🍅 High-Yield Seeds")
                st.button("Add - ₹150", key="i4", on_click=add_to_cart, args=("farmer", "Tomato Seeds (50g)", 150), use_container_width=True)
        with p_col2:
            with st.container(border=True):
                st.write("### 🛡️ Copper Fungicide")
                st.button("Add - ₹320", key="i2", on_click=add_to_cart, args=("farmer", "Copper Fungicide", 320), use_container_width=True)
            with st.container(border=True):
                st.write("### 💧 Drip Emitter Kit")
                st.button("Add - ₹850", key="i5", on_click=add_to_cart, args=("farmer", "Drip Kit (100pcs)", 850), use_container_width=True)
        with p_col3:
            with st.container(border=True):
                st.write("### ⚡ NPK Fertilizer")
                st.button("Add - ₹450", key="i3", on_click=add_to_cart, args=("farmer", "NPK Fertilizer", 450), use_container_width=True)
            with st.container(border=True):
                st.write("### ⛏️ Hand Cultivator")
                st.button("Add - ₹200", key="i6", on_click=add_to_cart, args=("farmer", "Hand Cultivator", 200), use_container_width=True)
                
        if st.session_state.farmer_cart:
            st.write("---")
            st.subheader("🛒 Your Cart")
            for item in st.session_state.farmer_cart:
                st.write(f"- {item['name']}: ₹{item['price']}")
            st.write(f"**{lang_dict['cart_total']} {sum(item['price'] for item in st.session_state.farmer_cart)}**")
            st.button(lang_dict["buy_now"], on_click=checkout, args=("farmer",), type="primary")

    with t3:
        st.subheader("Farming Best Practices")
        with st.expander("🌱 Soil Preparation & Testing"): 
            st.write("- Ensure deep ploughing to expose soil pests to sunlight.\n- Test soil pH and nutrient levels every 2 years.")
        with st.expander("💧 Efficient Water Management"): 
            st.write("- Adopt drip or sprinkler irrigation to save up to 40% water.\n- Use mulching around crops.")
        with st.expander("🛡️ Integrated Pest Management (IPM)"):
            st.write("- Use sticky traps and pheromone traps.\n- Apply chemical pesticides only as a targeted, last resort.")
        with st.expander("🌾 Crop Rotation & Intercropping"):
            st.write("- Rotate cereals with legumes.\n- Grow marigolds alongside tomatoes to deter nematodes.")
        with st.expander("📦 Post-Harvest Storage"):
            st.write("- Dry grains thoroughly to below 10-12% moisture.\n- Use hermetic bags to prevent infestations.")

    with t4:
        st.subheader("Active Wholesale Contracts")
        st.info("🏢 **Taj Hotels** requires: 500kg of Onions by Dec 1st | Target Price: ₹30/kg")
        if st.button("Accept Taj Contract", type="primary"): st.success("Contract secured! Buyer notified.")
        st.warning("🏭 **Balaji Foods** requires: 1000kg of Potatoes by Nov 15th | Target Price: ₹18/kg")
        if st.button("Accept Balaji Contract", type="primary"): st.success("Contract secured! Buyer notified.")
            
    with t5:
        st.subheader("AI Crop Health Scanner")
        uploaded_file = st.file_uploader("Upload leaf image (JPG/PNG)", type=["jpg", "png"])
        if uploaded_file and st.button("Analyze Image", type="primary"):
            with st.spinner("Scanning for pathogens using AgriConnect AI..."):
                time.sleep(2.5) 
            st.error("⚠️ **Detected:** Early Blight (Alternaria solani) - 87% Confidence")
            st.success("✅ **Recommended Action:** Apply Copper Fungicide immediately. (Available in Inputs tab)")
            
    with t6:
        st.subheader(lang_dict["qa_title"])
        with st.chat_message("user"): st.write("How do I protect tomatoes from heavy rain?")
        with st.chat_message("assistant"): st.write("Ensure proper field drainage and use raised beds. - *Farmer Suresh*")
        st.chat_input(lang_dict["qa_input"])

# --- 7. BUYER STOREFRONT ---
elif st.session_state.current_page == "Buyer":
    st.button(lang_dict["back"], on_click=change_page, args=("Home",))
    st.title(lang_dict["b_title"])
    
    st.subheader(lang_dict["delivery"])
    with st.container(border=True):
        st.write("**Order #AC-8492** • Arriving Today at 4:30 PM")
        st.progress(75) 
        st.caption("Status: Out for delivery | Delivery Partner: Ravi (📞 9876543210)")
    st.write("---")

    col_search, col_filter, col_btn = st.columns([3, 2, 1])
    with col_search: search_query = st.text_input(lang_dict["search_ph"], label_visibility="collapsed")
    with col_filter: max_price = st.slider("Max Price (₹/kg)", min_value=10, max_value=200, value=200, label_visibility="collapsed")
    with col_btn: st.button(lang_dict["voice_btn"])

    filtered_items = [item for item in st.session_state.market_items if (search_query.lower() in item['crop'].lower()) and (item['price'] <= max_price)]
    
    cols = st.columns(3)
    for index, item in enumerate(reversed(filtered_items)):
        with cols[index % 3]:
            with st.container(border=True):
                st.title(f"{item['emoji']} {item['crop']}")
                st.caption(f"👨‍🌾 Grown by {item['farmer']} | ⭐ {item.get('rating', 'New')} ({item.get('orders', 0)} orders)")
                st.subheader(f"₹{item['price']} / kg")
                st.button("Add to Cart", key=f"buy_{item['farmer']}_{item['crop']}", on_click=add_to_cart, args=("buyer", f"{item['crop']} ({item['farmer']})", item['price']), use_container_width=True)
                
    if st.session_state.buyer_cart:
        st.write("---")
        st.subheader("🛒 Your Grocery Cart")
        total = sum(item['price'] for item in st.session_state.buyer_cart)
        for item in st.session_state.buyer_cart: st.write(f"- {item['name']}: ₹{item['price']}")
        st.write(f"**{lang_dict['cart_total']} {total}**")
        st.button(lang_dict["checkout"], on_click=checkout, args=("buyer",), type="primary")

# --- 8. SUCCESS SCREEN & INVOICE ---
elif st.session_state.current_page == "Success":
    st.balloons()
    st.title(lang_dict["success"])
    
    if st.session_state.last_order:
        st.write("---")
        st.subheader(lang_dict["invoice"])
        total = sum(item['price'] for item in st.session_state.last_order)
        plat_fee = total * 0.02
        savings = total * 0.20 
        
        st.code(f"""
====================================
        AGRICONNECT TAX INVOICE
====================================
Date: {time.strftime("%Y-%m-%d %H:%M")}
------------------------------------
Items Purchased:
""")
        for item in st.session_state.last_order:
            st.code(f"{item['name']:<25} ₹{item['price']:.2f}")
            
        st.code(f"""
------------------------------------
Subtotal:                 ₹{total:.2f}
Platform Fee (2%):        ₹{plat_fee:.2f}
------------------------------------
TOTAL AMOUNT PAID:        ₹{total + plat_fee:.2f}
====================================
💡 You saved ₹{savings:.2f} by buying 
directly from local farmers!
====================================
        """)
        
    st.button(lang_dict["back"], on_click=change_page, args=("Home",), type="primary")