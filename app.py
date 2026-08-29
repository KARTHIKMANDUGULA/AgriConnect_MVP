import streamlit as st

# --- 1. PAGE CONFIGURATION & TRANSLATIONS ---
st.set_page_config(page_title="AgriConnect", layout="wide")

text = {
    "English": {
        "title": "🌾 Welcome to AgriConnect",
        "f_box": "👨‍🌾 Farmer",
        "f_desc": "List your fresh harvest directly to the market and set your own prices.",
        "feat_box": "🛠️ Helpful Features",
        "feat_desc": "Check government schemes, order pesticides, and access support.",
        "b_box": "🛒 Customer",
        "b_desc": "Browse fresh produce directly from local farms. Get better prices.",
        "open_btn": "Open Portal"
    },
    "తెలుగు": {
        "title": "🌾 అగ్రి కనెక్ట్‌కు స్వాగతం",
        "f_box": "👨‍🌾 రైతు",
        "f_desc": "మీ పంటను నేరుగా మార్కెట్‌లో జాబితా చేయండి మరియు మీ స్వంత ధరలను నిర్ణయించండి.",
        "feat_box": "🛠️ ఇతర ఫీచర్లు",
        "feat_desc": "ప్రభుత్వ పథకాలను తనిఖీ చేయండి, పురుగుమందులను ఆర్డర్ చేయండి.",
        "b_box": "🛒 కస్టమర్",
        "b_desc": "స్థానిక రైతుల నుండి నేరుగా తాజా కూరగాయలను కొనుగోలు చేయండి.",
        "open_btn": "తెరువు"
    },
    "हिंदी": {
        "title": "🌾 एग्रीकनेक्ट में आपका स्वागत है",
        "f_box": "👨‍🌾 किसान",
        "f_desc": "अपनी ताजा फसल सीधे बाजार में सूचीबद्ध करें और अपनी कीमतें तय करें।",
        "feat_box": "🛠️ अन्य विशेषताएं",
        "feat_desc": "सरकारी योजनाओं की जांच करें, कीटनाशकों का ऑर्डर करें।",
        "b_box": "🛒 ग्राहक",
        "b_desc": "सीधे स्थानीय खेतों से ताजा उपज ब्राउज़ करें।",
        "open_btn": "खोलें"
    }
}

# --- 2. STATE MANAGEMENT & DATABASE ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
if 'crop_added' not in st.session_state:
    st.session_state.crop_added = False
if 'farmer_cart' not in st.session_state:
    st.session_state.farmer_cart = []
if 'buyer_cart' not in st.session_state:
    st.session_state.buyer_cart = []
if 'language' not in st.session_state:
    st.session_state.language = "English"

# Added ratings and order history for the Trust System
if 'market_items' not in st.session_state:
    st.session_state.market_items = [
        {"farmer": "Ramesh", "crop": "Tomatoes", "price": 30, "stock": 50, "emoji": "🍅", "sales": 1500, "rating": 4.8, "orders": 120},
        {"farmer": "Suresh", "crop": "Onions", "price": 35, "stock": 200, "emoji": "🧅", "sales": 0, "rating": 4.5, "orders": 85},
    ]

def change_page(page_name):
    st.session_state.current_page = page_name
    st.session_state.crop_added = False

def reset_add_crop():
    st.session_state.crop_added = False

def add_to_cart(cart_type, item_name, price):
    if cart_type == 'farmer':
        st.session_state.farmer_cart.append({"name": item_name, "price": price})
    elif cart_type == 'buyer':
        st.session_state.buyer_cart.append({"name": item_name, "price": price})

def checkout(cart_type):
    if cart_type == 'farmer':
        st.session_state.farmer_cart = []
    elif cart_type == 'buyer':
        st.session_state.buyer_cart = []
    st.session_state.current_page = "Success"

# --- 3. SIDEBAR (LANGUAGE SELECTOR) ---
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
            st.title(text[lang]["f_box"])
            st.write(text[lang]["f_desc"])
            st.write("") 
            st.button(text[lang]["open_btn"], key="btn_f", on_click=change_page, args=("Farmer",), use_container_width=True, type="primary")
            
    with col2:
        with st.container(border=True):
            st.title(text[lang]["feat_box"])
            st.write(text[lang]["feat_desc"])
            st.write("")
            st.button(text[lang]["open_btn"], key="btn_feat", on_click=change_page, args=("Features",), use_container_width=True, type="primary")

    with col3:
        with st.container(border=True):
            st.title(text[lang]["b_box"])
            st.write(text[lang]["b_desc"])
            st.write("")
            st.button(text[lang]["open_btn"], key="btn_b", on_click=change_page, args=("Buyer",), use_container_width=True, type="primary")

# --- 5. FARMER PORTAL & DASHBOARD ---
elif st.session_state.current_page == "Farmer":
    st.button("⬅️ Back to Home", on_click=change_page, args=("Home",))
    st.title("👨‍🌾 Farmer Portal")
    
    tab1, tab2, tab3 = st.tabs(["➕ Add New Crop", "📊 My Dashboard", "🧮 Profit Estimator"])
    
    with tab1:
        if not st.session_state.crop_added:
            st.write("Add your harvest to the live market.")
            with st.form("add_crop"):
                farmer_name = st.text_input("Your Name")
                crop_name = st.text_input("Crop Name (e.g., Apple)")
                emoji = st.text_input("Crop Emoji (e.g., 🍎)", value="🍎")
                price = st.number_input("Price per kg (₹)", min_value=1)
                stock = st.number_input("Available Stock (kg)", min_value=1)
                submit = st.form_submit_button("List Crop")
                
                if submit and farmer_name and crop_name:
                    st.session_state.market_items.append({
                        "farmer": farmer_name, "crop": crop_name, "price": price, "stock": stock, "emoji": emoji, "sales": 0, "rating": "New", "orders": 0
                    })
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
            st.write("### 📦 Your Active Listings")
            for item in my_items:
                with st.container(border=True):
                    st.write(f"**{item['emoji']} {item['crop']}** | Price: ₹{item['price']}/kg | Stock: {item['stock']}kg")
        else:
            st.info("No listings found for this name yet. Go to 'Add New Crop' to get started!")
            
    with tab3:
        st.subheader("Yield & Profit Estimator")
        st.write("Calculate your potential earnings before you plant.")
        acres = st.number_input("Land Size (Acres)", min_value=0.1, value=1.0)
        yield_per_acre = st.number_input("Expected Yield per Acre (kg)", min_value=50, value=2000)
        est_price = st.number_input("Expected Selling Price (₹/kg)", min_value=1, value=30)
        
        if st.button("Calculate Expected Revenue", type="primary"):
            total_yield = acres * yield_per_acre
            revenue = total_yield * est_price
            st.success(f"🌾 Estimated Harvest: **{total_yield:,.0f} kg**")
            st.info(f"💰 Projected Revenue: **₹{revenue:,.2f}**")

# --- 6. OTHER HELPFUL FEATURES ---
elif st.session_state.current_page == "Features":
    st.button("⬅️ Back to Home", on_click=change_page, args=("Home",))
    st.title("🛠️ Other Helpful Features")
    
    tab1, tab2, tab3 = st.tabs(["🏛️ Government Schemes", "🧪 Order Pesticides & Inputs", "📖 Best Practices Guide"])
    
    with tab1:
        st.subheader("Financial Support & Subsidies")
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.subheader("PM-KISAN Samman Nidhi")
                st.text_input("Enter Aadhar Number:")
                st.button("Check PM-KISAN Status")
        with col2:
            with st.container(border=True):
                st.subheader("Agriculture Infrastructure Fund")
                st.button("Apply for AIF")
                
    with tab2:
        st.subheader("Direct Input Ordering")
        p_col1, p_col2, p_col3 = st.columns(3)
        with p_col1:
            with st.container(border=True):
                st.write("### 🌿 Neem Oil (1L)")
                st.subheader("₹250")
                st.button("Add to Cart", key="neem", on_click=add_to_cart, args=("farmer", "Neem Oil (1L)", 250), use_container_width=True)
        with p_col2:
            with st.container(border=True):
                st.write("### 🛡️ Copper Fungicide")
                st.subheader("₹320")
                st.button("Add to Cart", key="copper", on_click=add_to_cart, args=("farmer", "Copper Fungicide", 320), use_container_width=True)
        with p_col3:
            with st.container(border=True):
                st.write("### ⚡ NPK Fertilizer")
                st.subheader("₹450")
                st.button("Add to Cart", key="npk", on_click=add_to_cart, args=("farmer", "NPK Fertilizer", 450), use_container_width=True)
        
        if st.session_state.farmer_cart:
            st.write("---")
            st.subheader("🛒 Your Cart")
            total = sum(item['price'] for item in st.session_state.farmer_cart)
            for item in st.session_state.farmer_cart:
                st.write(f"- {item['name']}: ₹{item['price']}")
            st.write(f"**Total: ₹{total}**")
            st.button("Buy Now", on_click=checkout, args=("farmer",), type="primary")

    with tab3:
        st.subheader("Farming Best Practices")
        with st.expander("🌱 Soil Preparation for Kharif Crops"):
            st.write("- Ensure deep ploughing to expose soil pests to sunlight.")
            st.write("- Apply well-rotted farmyard manure or compost before sowing.")
            st.write("- Test soil pH and apply lime if acidic.")
        with st.expander("🛡️ Homemade Organic Pest Control (Neem Extract)"):
            st.write("- Crush 5kg of neem leaves and soak in 100L of water overnight.")
            st.write("- Filter the extract and mix with a little soap solution.")
            st.write("- Spray directly on crops to deter aphids and caterpillars.")
        with st.expander("💧 Efficient Water Management"):
            st.write("- Adopt drip irrigation to save up to 40% water.")
            st.write("- Mulch around plant bases to retain soil moisture and prevent weed growth.")

# --- 7. BUYER STOREFRONT ---
elif st.session_state.current_page == "Buyer":
    st.button("⬅️ Back to Home", on_click=change_page, args=("Home",))
    st.title("🛒 Live Buyer Storefront")
    
    # Smart Search & Filters
    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search_query = st.text_input("🔍 Search for a crop (e.g., Tomatoes)")
    with col_filter:
        max_price = st.slider("Max Price (₹/kg)", min_value=10, max_value=200, value=200)

    # Filter logic
    filtered_items = [
        item for item in st.session_state.market_items 
        if (search_query.lower() in item['crop'].lower()) and (item['price'] <= max_price)
    ]
    
    cols = st.columns(3)
    for index, item in enumerate(reversed(filtered_items)):
        with cols[index % 3]:
            with st.container(border=True):
                st.title(f"{item['emoji']} {item['crop']}")
                # Trust & Ratings Display
                st.caption(f"👨‍🌾 Grown by {item['farmer']} | ⭐ {item.get('rating', 'New')} ({item.get('orders', 0)} orders)")
                st.subheader(f"₹{item['price']} / kg")
                st.button("Add to Cart", key=f"buy_{item['farmer']}_{item['crop']}", on_click=add_to_cart, args=("buyer", f"{item['crop']} ({item['farmer']})", item['price']), use_container_width=True)
                
    if not filtered_items:
        st.warning("No crops found matching your search and price criteria.")
                
    if st.session_state.buyer_cart:
        st.write("---")
        st.subheader("🛒 Your Grocery Cart")
        total = sum(item['price'] for item in st.session_state.buyer_cart)
        for item in st.session_state.buyer_cart:
            st.write(f"- {item['name']}: ₹{item['price']}")
        st.write(f"**Total: ₹{total}**")
        st.button("Checkout & Buy", on_click=checkout, args=("buyer",), type="primary")

# --- 8. SUCCESS SCREEN ---
elif st.session_state.current_page == "Success":
    st.balloons()
    st.title("🎉 Order Placed Successfully!")
    st.success("Your order has been confirmed and is being processed.")
    st.button("⬅️ Return to Home", on_click=change_page, args=("Home",), type="primary")