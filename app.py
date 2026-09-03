import streamlit as st
import time
import pandas as pd

# ==========================================
# 1. PAGE CONFIGURATION & TRANSLATIONS
# ==========================================
st.set_page_config(page_title="AgriConnect", layout="wide")

t = {
    "English": {
        "demand": "🚨 High Demand Alert: Onion searches are up 40% this week. Consider planting for higher margins!",
        "search_ph": "🔍 Search for a crop (🎤 Voice Enabled)", "voice_btn": "🎤 Speak",
        "add_crop": "List Crop", "calc": "Calculate Expected Revenue", "cart_total": "Cart Total: ₹",
        "pool_btn": "Join Transport", "qa_input": "Ask the community (🎤 Voice Enabled)...",
        "smart_cmd": "🎤 Click to Record Voice Command", "buy_now": "Buy Inputs Now", "checkout": "Checkout & Buy"
    },
    "తెలుగు": {
        "demand": "🚨 డిమాండ్ అలర్ట్: ఉల్లిపాయల అన్వేషణ 40% పెరిగింది. ఎక్కువ లాభం కోసం ప్లాన్ చేయండి!",
        "search_ph": "🔍 పంటలను వెతకండి (🎤 వాయిస్)", "voice_btn": "🎤 మాట్లాడండి",
        "add_crop": "పంటను జోడించు", "calc": "రెవెన్యూ లెక్కించు", "cart_total": "మొత్తం: ₹",
        "pool_btn": "ట్రక్‌లో చేరండి", "qa_input": "సందేహాలు అడగండి (🎤 వాయిస్)...",
        "smart_cmd": "🎤 వాయిస్ కమాండ్ రికార్డ్ చేయడానికి క్లిక్ చేయండి", "buy_now": "కొనుగోలు చేయండి", "checkout": "చెక్అవుట్"
    },
    "हिंदी": {
        "demand": "🚨 डिमांड अलर्ट: प्याज की खोज 40% बढ़ गई है। अधिक लाभ के लिए योजना बनाएं!",
        "search_ph": "🔍 फसल खोजें (🎤 वॉयस)", "voice_btn": "🎤 बोलें",
        "add_crop": "फसल जोड़ें", "calc": "राजस्व की गणना करें", "cart_total": "कुल: ₹",
        "pool_btn": "परिवहन में शामिल हों", "qa_input": "समुदाय से पूछें (🎤 वॉयस)...",
        "smart_cmd": "🎤 वॉयस कमांड रिकॉर्ड करने के लिए क्लिक करें", "buy_now": "अभी खरीदें", "checkout": "चेकआउट"
    }
}

# ==========================================
# 2. STATE MANAGEMENT 
# ==========================================
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'user_role' not in st.session_state: st.session_state.user_role = None
if 'username' not in st.session_state: st.session_state.username = ""
if 'login_step' not in st.session_state: st.session_state.login_step = "Select" 
if 'current_page' not in st.session_state: st.session_state.current_page = "Farmer_Hub"
if 'language' not in st.session_state: st.session_state.language = "English"
if 'crop_added' not in st.session_state: st.session_state.crop_added = False
if 'farmer_cart' not in st.session_state: st.session_state.farmer_cart = []
if 'buyer_cart' not in st.session_state: st.session_state.buyer_cart = []
if 'last_order' not in st.session_state: st.session_state.last_order = []
if 'market_items' not in st.session_state:
    st.session_state.market_items = [
        {"farmer": "Ramesh", "crop": "Tomatoes", "price": 30, "stock": 500, "emoji": "🍅", "sales": 15000, "rating": 4.8, "orders": 120},
        {"farmer": "Suresh", "crop": "Onions", "price": 35, "stock": 200, "emoji": "🧅", "sales": 7000, "rating": 4.5, "orders": 85},
    ]

USER_DB = {
    "ramesh": ["pass123", "Farmer"],
    "suresh": ["pass123", "Farmer"],
    "anita": ["buyer123", "Customer"],
    "rahul": ["buyer123", "Customer"]
}

def set_login_step(step): st.session_state.login_step = step
def change_page(page_name): 
    st.session_state.current_page = page_name
    st.session_state.crop_added = False
def reset_add_crop(): st.session_state.crop_added = False
def add_to_cart(cart_type, item_name, price): st.session_state[f"{cart_type}_cart"].append({"name": item_name, "price": price})
def checkout(cart_type):
    st.session_state.last_order = st.session_state[f"{cart_type}_cart"].copy()
    st.session_state[f"{cart_type}_cart"] = []
    st.session_state.current_page = "Success"
def logout_user():
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = ""
    st.session_state.login_step = "Select"
    st.session_state.current_page = "Farmer_Hub"

def login_user(user, pwd, role):
    u = user.strip().lower()
    if u in USER_DB:
        if pwd == USER_DB[u][0] and USER_DB[u][1] == role:
            st.session_state.authenticated = True
            st.session_state.user_role = role
            st.session_state.username = user.strip().title()
            st.session_state.current_page = "Farmer_Hub" if role == "Farmer" else "Buyer"
            st.rerun()
        else:
            st.error("❌ Invalid password or incorrect role chosen.")
    else:
        st.error("❌ Username not found.")

# ==========================================
# 3. SIDEBAR
# ==========================================
st.sidebar.title("🌐 Language / భాష")
st.session_state.language = st.sidebar.selectbox("Select Display Language:", ["English", "తెలుగు", "हिंदी"])
lang = st.session_state.language
lang_dict = t[lang]

if st.session_state.authenticated:
    st.sidebar.write("---")
    st.sidebar.write(f"👤 Logged in as: **{st.session_state.username}**")
    st.sidebar.caption(f"Role: {st.session_state.user_role}")
    st.sidebar.button("🚪 Logout", on_click=logout_user, use_container_width=True)

# ==========================================
# 4. START SCREEN (LOGIN)
# ==========================================
if not st.session_state.authenticated:
    st.title("🌾 Welcome to AgriConnect")
    st.write("Select your portal to continue.")
    st.write("---")
    
    if st.session_state.login_step == "Select":
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.title("👨‍🌾 Farmer Access")
                st.write("List your harvest and access farm tools.")
                st.button("Open Farmer Portal", on_click=set_login_step, args=("Farmer_Login",), use_container_width=True, type="primary")
        with col2:
            with st.container(border=True):
                st.title("🛒 Customer Access")
                st.write("Buy fresh produce directly from local farms.")
                st.button("Open Customer Portal", on_click=set_login_step, args=("Customer_Login",), use_container_width=True, type="primary")

    elif st.session_state.login_step == "Farmer_Login":
        st.button("⬅️ Back to Selection", on_click=set_login_step, args=("Select",))
        with st.container(border=True):
            st.title("👨‍🌾 Farmer Login")
            with st.form("farmer_auth_form"):
                f_u = st.text_input("Username", placeholder="Enter username (e.g., ramesh)")
                f_p = st.text_input("Password", type="password", placeholder="Enter password")
                if st.form_submit_button("Sign In", type="primary", use_container_width=True): login_user(f_u, f_p, "Farmer")
                    
    elif st.session_state.login_step == "Customer_Login":
        st.button("⬅️ Back to Selection", on_click=set_login_step, args=("Select",))
        with st.container(border=True):
            st.title("🛒 Customer Login")
            with st.form("buyer_auth_form"):
                b_u = st.text_input("Username", placeholder="Enter username (e.g., anita)")
                b_p = st.text_input("Password", type="password", placeholder="Enter password")
                if st.form_submit_button("Sign In", type="primary", use_container_width=True): login_user(b_u, b_p, "Customer")

    st.stop()

# ==========================================
# 5. FARMER ROUTES 
# ==========================================
if st.session_state.user_role == "Farmer":
    
    if st.session_state.current_page == "Farmer_Hub":
        st.title(f"👋 Welcome back, {st.session_state.username}")
        st.write("---")
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.title("📊 Farmer Dashboard")
                st.write("Manage your crops, track market prices, and arrange truck pooling.")
                st.button("Open Dashboard", on_click=change_page, args=("Farmer_Dashboard",), use_container_width=True, type="primary")
        with col2:
            with st.container(border=True):
                st.title("🛠️ Helpful Features")
                st.write("Access Government Schemes, Input Ordering, AI, and Guides.")
                st.button("Open Features", on_click=change_page, args=("Farmer_Features",), use_container_width=True, type="primary")

    elif st.session_state.current_page == "Farmer_Dashboard":
        st.button("⬅️ Back to Farmer Hub", on_click=change_page, args=("Farmer_Hub",))
        st.title("📊 Farmer Dashboard")
        st.warning(lang_dict["demand"])
        tab1, tab2, tab3, tab4 = st.tabs(["➕ Add New Crop", "📈 My Analytics", "🧮 Profit Estimator", "🚚 Truck Pooling"])
        
        with tab1:
            st.write("### 🗣️ Smart Voice Assistant")
            smart_name = st.text_input("Your Name (For Voice Listing)", value=st.session_state.username)
            audio_value = st.audio_input(lang_dict["smart_cmd"])
            if audio_value:
                with st.spinner("🎙️ AI processing voice..."):
                    time.sleep(2)
                    if 'voice_demo_count' not in st.session_state: st.session_state.voice_demo_count = 0
                    demo_commands = [("Tomato", 10, 60, "🍅"), ("Potato", 8, 50, "🥔"), ("Rice", 20, 100, "🌾"), ("Onion", 15, 99, "🧅")]
                    crop_val, stock_val, price_val, emoji_val = demo_commands[st.session_state.voice_demo_count % len(demo_commands)]
                    st.session_state.voice_demo_count += 1
                    st.session_state.market_items.append({"farmer": smart_name, "crop": crop_val, "price": price_val, "stock": stock_val, "emoji": emoji_val, "sales": 0, "rating": "New", "orders": 0})
                    st.success(f"✅ **Transcribed Voice:** 'List {stock_val}kg {crop_val} for {price_val} rupees'")
            st.write("---")
            if not st.session_state.crop_added:
                with st.form("add_crop"):
                    farmer_name = st.text_input("Your Name", value=st.session_state.username)
                    crop_name = st.text_input("Crop Name")
                    emoji = st.text_input("Crop Emoji (e.g., 🍎)", value="🍎")
                    price = st.number_input("Price per kg (₹)", min_value=1)
                    stock = st.number_input("Available Stock (kg)", min_value=1)
                    if st.form_submit_button(lang_dict["add_crop"]) and crop_name:
                        st.session_state.market_items.append({"farmer": farmer_name, "crop": crop_name, "price": price, "stock": stock, "emoji": emoji, "sales": 0, "rating": "New", "orders": 0})
                        st.session_state.crop_added = True
                        st.rerun()
            else:
                st.success("✅ Crop successfully listed!")
                st.button("➕ Add Another Crop", on_click=reset_add_crop)
                
        with tab2:
            st.subheader("📈 Farm Analytics & Performance")
            my_items = [item for item in st.session_state.market_items if item['farmer'].lower() == st.session_state.username.lower()]
            
            if my_items:
                kpi1, kpi2, kpi3, kpi4 = st.columns(4)
                total_earnings = sum(item.get('sales', 0) for item in my_items)
                total_stock = sum(item['stock'] for item in my_items)
                total_orders = sum(item.get('orders', 0) for item in my_items)
                
                valid_ratings = [float(item['rating']) for item in my_items if item.get('rating') != 'New']
                avg_rating = sum(valid_ratings) / len(valid_ratings) if valid_ratings else 5.0
                
                with kpi1: st.metric("Total Revenue", f"₹{total_earnings:,.2f}", "+12% vs last month")
                with kpi2: st.metric("Total Active Stock", f"{total_stock} kg")
                with kpi3: st.metric("Completed Orders", f"{total_orders}")
                with kpi4: st.metric("Customer Rating", f"⭐ {avg_rating:.1f}")
                
                st.write("---")
                chart_col, data_col = st.columns(2)
                
                with chart_col:
                    st.write("### 📊 Current Inventory Breakdown")
                    inventory_data = pd.DataFrame([{"Crop": item["crop"], "Stock (kg)": item["stock"]} for item in my_items]).set_index("Crop")
                    st.bar_chart(inventory_data)
                
                with data_col:
                    st.write("### 📜 Recent Transactions")
                    st.dataframe(pd.DataFrame({
                        "Date": ["2026-09-02", "2026-09-03", "2026-09-04"],
                        "Crop": [my_items[0]['crop'], "Assorted", my_items[-1]['crop']],
                        "Qty (kg)": [50, 15, 25],
                        "Status": ["Delivered", "Delivered", "In Transit"]
                    }), hide_index=True, use_container_width=True)

                st.write("---")
                st.write("### 📦 Manage Active Listings")
                for item in my_items:
                    with st.container(border=True):
                        col_info, col_act = st.columns([4, 1])
                        with col_info:
                            st.write(f"**{item['emoji']} {item['crop']}** | Listed at: ₹{item['price']}/kg | Available: {item['stock']}kg")
                        with col_act:
                            st.button("Edit Listing", key=f"edit_{item['crop']}")
            else:
                st.info("You haven't listed any crops yet. Add a crop to view your analytics!")
                
        with tab3:
            acres = st.number_input("Land Size (Acres)", min_value=0.1, value=1.0)
            yield_per_acre = st.number_input("Expected Yield per Acre (kg)", min_value=50, value=2000)
            est_price = st.number_input("Expected Selling Price (₹/kg)", min_value=1, value=30)
            if st.button(lang_dict["calc"], type="primary"):
                st.success(f"🌾 Estimated Harvest: **{acres * yield_per_acre:,.0f} kg**")
                st.info(f"💰 Projected Revenue: **₹{(acres * yield_per_acre) * est_price:,.2f}**")

        with tab4:
            st.subheader("🚚 Active Truck Pools")
            with st.container(border=True):
                st.write("**Route:** Mallapur ➡️ Secunderabad Market")
                st.progress(60); st.caption("Capacity: 600kg / 1000kg filled")
                st.button(lang_dict["pool_btn"], key="t1")

    elif st.session_state.current_page == "Farmer_Features":
        st.button("⬅️ Back to Farmer Hub", on_click=change_page, args=("Farmer_Hub",))
        st.title("🛠️ Helpful Features")
        
        t1, t2, t3, t4, t5, t6 = st.tabs(["🏛️ Schemes", "🧪 Inputs", "📖 Guide", "🤝 B2B Contracts", "🌿 AI Scanner", "💬 Q&A"])
        
        with t1:
            st.subheader("National & State Subsidies")
            col1, col2 = st.columns(2)
            with col1:
                with st.container(border=True):
                    st.write("### PM-KISAN Samman Nidhi")
                    st.caption("₹6,000 per year minimum income support.")
                    st.button("Check Eligibility", key="s1")
                with st.container(border=True):
                    st.write("### PM-KUSUM Yojana")
                    st.caption("Up to 60% subsidy on Solar Water Pumps.")
                    st.button("Apply for Solar", key="s2")
            with col2:
                with st.container(border=True):
                    st.write("### e-NAM Registration")
                    st.caption("National Agriculture Market pan-India trading.")
                    st.button("Register on e-NAM", key="s3")
                with st.container(border=True):
                    st.write("### Kisan Credit Card (KCC)")
                    st.caption("Subsidized credit rates for agricultural inputs.")
                    st.button("Apply for KCC", key="s4")
                    
        with t2:
            st.subheader("Direct Input Ordering (Subsidized Rates)")
            p_col1, p_col2, p_col3 = st.columns(3)
            with p_col1:
                with st.container(border=True):
                    st.write("### 🌿 Neem Oil (1L)")
                    st.button("Add - ₹250", key="i1", on_click=add_to_cart, args=("farmer", "Neem Oil (1L)", 250), use_container_width=True)
                with st.container(border=True):
                    st.write("### 🪤 Pheromone Traps")
                    st.button("Add - ₹180", key="i4", on_click=add_to_cart, args=("farmer", "Pheromone Trap (Set of 5)", 180), use_container_width=True)
                with st.container(border=True):
                    st.write("### 🍅 High-Yield Seeds")
                    st.button("Add - ₹150", key="i7", on_click=add_to_cart, args=("farmer", "Tomato Seeds (50g)", 150), use_container_width=True)
            with p_col2:
                with st.container(border=True):
                    st.write("### 🛡️ Trichoderma (Bio)")
                    st.button("Add - ₹300", key="i2", on_click=add_to_cart, args=("farmer", "Trichoderma Viride (1kg)", 300), use_container_width=True)
                with st.container(border=True):
                    st.write("### 🟨 Sticky Traps")
                    st.button("Add - ₹120", key="i5", on_click=add_to_cart, args=("farmer", "Yellow Sticky Traps (10 pcs)", 120), use_container_width=True)
                with st.container(border=True):
                    st.write("### 💧 Drip Emitters")
                    st.button("Add - ₹850", key="i8", on_click=add_to_cart, args=("farmer", "Drip Kit (100pcs)", 850), use_container_width=True)
            with p_col3:
                with st.container(border=True):
                    st.write("### ⚡ NPK Fertilizer")
                    st.button("Add - ₹450", key="i3", on_click=add_to_cart, args=("farmer", "NPK 19:19:19 (1kg)", 450), use_container_width=True)
                with st.container(border=True):
                    st.write("### 🌱 Rhizobium Base")
                    st.button("Add - ₹220", key="i6", on_click=add_to_cart, args=("farmer", "Rhizobium Bio-fertilizer", 220), use_container_width=True)
                with st.container(border=True):
                    st.write("### 🚜 Mini Tractor Rent")
                    st.button("Add - ₹1200", key="i9", on_click=add_to_cart, args=("farmer", "Tractor Rental (Per Day)", 1200), use_container_width=True)
                    
            if st.session_state.farmer_cart:
                st.write("---")
                st.subheader("🛒 Your Input Cart")
                for item in st.session_state.farmer_cart:
                    st.write(f"- {item['name']}: ₹{item['price']}")
                st.write(f"**{lang_dict['cart_total']} {sum(item['price'] for item in st.session_state.farmer_cart)}**")
                st.button(lang_dict["buy_now"], on_click=checkout, args=("farmer",), type="primary")

        with t3:
            st.subheader("Farming Best Practices")
            with st.expander("🌱 Soil Preparation & Testing"): st.write("- Ensure deep ploughing.\n- Test soil pH every 2 years.")
            with st.expander("💧 Efficient Water Management"): st.write("- Adopt drip irrigation to save up to 40% water.")
            with st.expander("🛡️ Integrated Pest Management"): st.write("- Use sticky traps and pheromone traps.")

        with t4:
            st.subheader("Active Wholesale Contracts")
            st.info("🏢 **Taj Hotels** requires: 500kg of Onions | Target Price: ₹30/kg")
            if st.button("Accept Taj Contract", type="primary"): st.success("Contract secured!")
            
        with t5:
            st.subheader("AI Crop Health Scanner")
            uploaded_file = st.file_uploader("Upload leaf image (JPG/PNG)", type=["jpg", "png"])
            if uploaded_file and st.button("Analyze Image", type="primary"):
                with st.spinner("Scanning..."): time.sleep(2) 
                st.error("⚠️ **Detected:** Early Blight (87% Confidence)")
                
        with t6:
            st.subheader("Community Q&A")
            with st.chat_message("user"): st.write("How do I protect tomatoes from heavy rain?")
            with st.chat_message("assistant"): st.write("Ensure proper field drainage and use raised beds. - *Farmer Suresh*")
            st.chat_input(lang_dict["qa_input"])

    elif st.session_state.current_page == "Success":
        st.balloons()
        st.title("🎉 Agricultural Inputs Ordered Successfully!")
        if st.session_state.last_order:
            st.write("---")
            st.subheader("🧾 AgriConnect B2B Digital Invoice")
            total = sum(item['price'] for item in st.session_state.last_order)
            gst = total * 0.05 
            
            st.code(f"""
====================================
        FARMER INPUT TAX INVOICE
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
Agri-GST (5%):            ₹{gst:.2f}
------------------------------------
TOTAL AMOUNT PAID:        ₹{total + gst:.2f}
====================================
🚚 Expected Delivery: Tomorrow by 10 AM
====================================
            """)
        st.button("⬅️ Back to Features", on_click=change_page, args=("Farmer_Features",), type="primary")

# ==========================================
# 6. CUSTOMER ROUTES
# ==========================================
elif st.session_state.user_role == "Customer":
    
    if st.session_state.current_page == "Buyer":
        st.title("🛒 Fresh Produce Market")
        st.subheader("🚚 Active Deliveries")
        with st.container(border=True):
            st.write("**Order #AC-8492** • Arriving Today at 4:30 PM")
            st.progress(75); st.caption("Status: Out for delivery | Partner: Ravi")
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
                    st.caption(f"👨‍🌾 Grown by {item['farmer']} | ⭐ {item.get('rating', 'New')}")
                    st.subheader(f"₹{item['price']} / kg")
                    st.button("Add to Cart", key=f"buy_{item['farmer']}_{item['crop']}", on_click=add_to_cart, args=("buyer", f"{item['crop']}", item['price']), use_container_width=True)
                    
        if st.session_state.buyer_cart:
            st.write("---")
            st.subheader("🛒 Your Grocery Cart")
            total = sum(item['price'] for item in st.session_state.buyer_cart)
            for item in st.session_state.buyer_cart: st.write(f"- {item['name']}: ₹{item['price']}")
            st.write(f"**{lang_dict['cart_total']} {total}**")
            st.button(lang_dict["checkout"], on_click=checkout, args=("buyer",), type="primary")

    elif st.session_state.current_page == "Success":
        st.balloons()
        st.title("🎉 Order Placed Successfully!")
        if st.session_state.last_order:
            st.write("---")
            st.subheader("🧾 Auto-Generated Digital Invoice")
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
        st.button("⬅️ Back to Store", on_click=change_page, args=("Buyer",), type="primary")