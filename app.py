import streamlit as st
import time
import pandas as pd

# --- 1. PAGE CONFIGURATION & TRANSLATIONS ---
st.set_page_config(page_title="AgriConnect", layout="wide")

text = {
    "English": {
        "title": "🌾 Welcome to AgriConnect",
        "f_box": "👨‍🌾 Farmer", "f_desc": "List your fresh harvest directly to the market.",
        "feat_box": "🛠️ Helpful Features", "feat_desc": "Government schemes, B2B contracts, and AI tools.",
        "b_box": "🛒 Customer", "b_desc": "Browse fresh produce directly from local farms.",
        "open_btn": "Open Portal", "back_btn": "⬅️ Back to Home",
        "f_title": "👨‍🌾 Farmer Portal", "feat_title": "🛠️ Helpful Features", "b_title": "🛒 Buyer Storefront"
    },
    "తెలుగు": {
        "title": "🌾 అగ్రి కనెక్ట్‌కు స్వాగతం",
        "f_box": "👨‍🌾 రైతు", "f_desc": "మీ పంటను నేరుగా మార్కెట్‌లో జాబితా చేయండి.",
        "feat_box": "🛠️ ఫీచర్లు", "feat_desc": "ప్రభుత్వ పథకాలు, B2B కాంట్రాక్ట్‌లు మరియు AI టూల్స్.",
        "b_box": "🛒 కస్టమర్", "b_desc": "స్థానిక రైతుల నుండి నేరుగా కొనుగోలు చేయండి.",
        "open_btn": "తెరువు", "back_btn": "⬅️ వెనుకకు",
        "f_title": "👨‍🌾 రైతు పోర్టల్", "feat_title": "🛠️ ఇతర ఫీచర్లు", "b_title": "🛒 కస్టమర్ పోర్టల్"
    },
    "हिंदी": {
        "title": "🌾 एग्रीकनेक्ट में आपका स्वागत है",
        "f_box": "👨‍🌾 किसान", "f_desc": "अपनी ताजा फसल सीधे बाजार में सूचीबद्ध करें।",
        "feat_box": "🛠️ विशेषताएं", "feat_desc": "सरकारी योजनाएं, B2B अनुबंध और AI टूल।",
        "b_box": "🛒 ग्राहक", "b_desc": "सीधे स्थानीय खेतों से ताजा उपज ब्राउज़ करें।",
        "open_btn": "खोलें", "back_btn": "⬅️ वापस",
        "f_title": "👨‍🌾 किसान पोर्टल", "feat_title": "🛠️ अन्य विशेषताएं", "b_title": "🛒 ग्राहक पोर्टल"
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
    if cart_type == 'farmer': st.session_state.farmer_cart.append({"name": item_name, "price": price})
    elif cart_type == 'buyer': st.session_state.buyer_cart.append({"name": item_name, "price": price})

def checkout(cart_type):
    if cart_type == 'farmer':
        st.session_state.last_order = st.session_state.farmer_cart.copy()
        st.session_state.farmer_cart = []
    elif cart_type == 'buyer':
        st.session_state.last_order = st.session_state.buyer_cart.copy()
        st.session_state.buyer_cart = []
    st.session_state.current_page = "Success"

# --- 3. SIDEBAR ---
st.sidebar.title("🌐 Language / భాష")
st.session_state.language = st.sidebar.selectbox("Select Display Language:", ["English", "తెలుగు", "हिंदी"])
lang = st.session_state.language

# --- 4. HOME PAGE ---
if st.session_state.current_page == "Home":
    st.title(text[lang]["title"])
    st.write("---") 
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.title(text[lang]["f_box"]); st.write(text[lang]["f_desc"]); st.write("") 
            st.button(text[lang]["open_btn"], key="btn_f", on_click=change_page, args=("Farmer",), use_container_width=True, type="primary")
    with col2:
        with st.container(border=True):
            st.title(text[lang]["feat_box"]); st.write(text[lang]["feat_desc"]); st.write("")
            st.button(text[lang]["open_btn"], key="btn_feat", on_click=change_page, args=("Features",), use_container_width=True, type="primary")
    with col3:
        with st.container(border=True):
            st.title(text[lang]["b_box"]); st.write(text[lang]["b_desc"]); st.write("")
            st.button(text[lang]["open_btn"], key="btn_b", on_click=change_page, args=("Buyer",), use_container_width=True, type="primary")

# --- 5. FARMER PORTAL & DASHBOARD ---
elif st.session_state.current_page == "Farmer":
    st.button(text[lang]["back_btn"], on_click=change_page, args=("Home",))
    st.title(text[lang]["f_title"])
    
    tab1, tab2, tab3 = st.tabs(["➕ Add New Crop", "📊 My Dashboard", "🧮 Profit Estimator"])
    
    with tab1:
        if not st.session_state.crop_added:
            with st.form("add_crop"):
                farmer_name = st.text_input("Your Name")
                crop_name = st.text_input("Crop Name (e.g., Apple)")
                emoji = st.text_input("Crop Emoji (e.g., 🍎)", value="🍎")
                price = st.number_input("Price per kg (₹)", min_value=1)
                stock = st.number_input("Available Stock (kg)", min_value=1)
                submit = st.form_submit_button("List Crop")
                if submit and farmer_name and crop_name:
                    st.session_state.market_items.append({"farmer": farmer_name, "crop": crop_name, "price": price, "stock": stock, "emoji": emoji, "sales": 0, "rating": "New", "orders": 0})
                    st.session_state.crop_added = True
                    st.rerun()
        else:
            st.success("✅ Crop successfully listed on the live market!")
            st.button("➕ Add Another Crop", on_click=reset_add_crop, type="primary")
            
    with tab2:
        st.subheader("Farm Analytics")
        dashboard_name = st.text_input("Enter your name to view your dashboard:", value="Ramesh")
        my_items = [item for item in st.session_state.market_items if item['farmer'].lower() == dashboard_name.lower()]
        
        if my_items:
            total_earnings = sum(item.get('sales', 0) for item in my_items)
            st.metric(label="Total Projected Earnings", value=f"₹{total_earnings}")
            
            st.write("### 📈 Live Market Price Trends")
            # Dynamic Analytics Chart
            chart_data = pd.DataFrame({
                "Tomatoes (₹/kg)": [25, 28, 30, 32, 30, 29, 30],
                "Onions (₹/kg)": [40, 38, 35, 34, 35, 36, 35]
            }, index=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
            st.line_chart(chart_data)
            
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
        if st.button("Calculate Expected Revenue", type="primary"):
            st.success(f"🌾 Estimated Harvest: **{acres * yield_per_acre:,.0f} kg**")
            st.info(f"💰 Projected Revenue: **₹{(acres * yield_per_acre) * est_price:,.2f}**")

# --- 6. OTHER HELPFUL FEATURES ---
elif st.session_state.current_page == "Features":
    st.button(text[lang]["back_btn"], on_click=change_page, args=("Home",))
    st.title(text[lang]["feat_title"])
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏛️ Schemes", "🧪 Inputs", "📖 Guide", "🤝 B2B Contracts", "🌿 Crop AI"])
    
    with tab1:
        st.subheader("PM-KISAN & AIF Support")
        st.text_input("Enter Aadhar Number:")
        st.button("Check Status")
                
    with tab2:
        st.subheader("Direct Input Ordering")
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            st.write("### 🌿 Neem Oil (1L)")
            st.button("Add Neem Oil - ₹250", on_click=add_to_cart, args=("farmer", "Neem Oil (1L)", 250))
        with p_col2:
            st.write("### 🛡️ Copper Fungicide")
            st.button("Add Fungicide - ₹320", on_click=add_to_cart, args=("farmer", "Copper Fungicide", 320))
        if st.session_state.farmer_cart:
            st.write(f"**Cart Total: ₹{sum(item['price'] for item in st.session_state.farmer_cart)}**")
            st.button("Buy Now", on_click=checkout, args=("farmer",), type="primary")

    with tab3:
        st.subheader("Farming Best Practices")
        with st.expander("🌱 Soil Preparation"): st.write("- Ensure deep ploughing.\n- Apply well-rotted manure.")
        with st.expander("💧 Efficient Water Management"): st.write("- Adopt drip irrigation to save up to 40% water.")

    with tab4:
        st.subheader("Active Wholesale Contracts")
        st.info("🏢 **Taj Hotels** requires: 500kg of Onions by Dec 1st | Target Price: ₹30/kg")
        if st.button("Accept Taj Contract", type="primary"): st.success("Contract secured! Buyer notified.")
        st.warning("🏭 **Balaji Foods** requires: 1000kg of Potatoes by Nov 15th | Target Price: ₹18/kg")
        if st.button("Accept Balaji Contract", type="primary"): st.success("Contract secured! Buyer notified.")
            
    with tab5:
        st.subheader("AI Crop Health Scanner")
        st.write("Upload a picture of a diseased leaf for instant AI diagnosis.")
        uploaded_file = st.file_uploader("Upload leaf image (JPG/PNG)", type=["jpg", "png"])
        if uploaded_file and st.button("Analyze Image", type="primary"):
            with st.spinner("Scanning for pathogens using AgriConnect AI..."):
                time.sleep(2.5) # Simulated AI loading delay
            st.error("⚠️ **Detected:** Early Blight (Alternaria solani) - 87% Confidence")
            st.success("✅ **Recommended Action:** Apply Copper Fungicide immediately. (Available in Inputs tab)")

# --- 7. BUYER STOREFRONT ---
elif st.session_state.current_page == "Buyer":
    st.button(text[lang]["back_btn"], on_click=change_page, args=("Home",))
    st.title(text[lang]["b_title"])
    
    col_search, col_filter = st.columns([2, 1])
    with col_search: search_query = st.text_input("🔍 Search for a crop (e.g., Tomatoes)")
    with col_filter: max_price = st.slider("Max Price (₹/kg)", min_value=10, max_value=200, value=200)

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
        st.write(f"**Total: ₹{total}**")
        st.button("Checkout & Buy", on_click=checkout, args=("buyer",), type="primary")

# --- 8. SUCCESS SCREEN & INVOICE ---
elif st.session_state.current_page == "Success":
    st.balloons()
    st.title("🎉 Order Placed Successfully!")
    
    if st.session_state.last_order:
        st.write("---")
        st.subheader("🧾 Auto-Generated Digital Invoice")
        total = sum(item['price'] for item in st.session_state.last_order)
        plat_fee = total * 0.02
        savings = total * 0.20 # Simulating 20% savings vs retail
        
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
        
    st.button("⬅️ Return to Home", on_click=change_page, args=("Home",), type="primary")