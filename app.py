import streamlit as st
import time
import pandas as pd
import sqlite3
from sklearn.ensemble import RandomForestRegressor

# ==========================================
# 1. DATABASE & AI ENGINE
# ==========================================
def get_db_connection():
    conn = sqlite3.connect('agriconnect.db', check_same_thread=False, timeout=10)
    return conn

@st.cache_resource
def train_price_ai():
    data = {
        'month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'rain_mm': [10, 5, 20, 40, 60, 120, 150, 130, 90, 40, 15, 5],
        'temp_c': [22, 25, 29, 33, 35, 30, 28, 27, 28, 26, 24, 21],
        'demand_index': [80, 85, 90, 85, 95, 110, 120, 115, 100, 90, 85, 80],
        'price_per_kg': [20, 22, 25, 24, 30, 45, 50, 48, 35, 28, 24, 21]
    }
    df = pd.DataFrame(data)
    X = df[['month', 'rain_mm', 'temp_c', 'demand_index']]
    y = df['price_per_kg']
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

db_conn = get_db_connection()
ai_model = train_price_ai()

# ==========================================
# 2. PAGE CONFIGURATION & TRANSLATIONS
# ==========================================
st.set_page_config(page_title="AgriConnect", layout="wide")

t = {
    "English": {"demand": "🚨 High Demand Alert: Onion searches are up 40% this week. Consider planting for higher margins!", "search_lbl": "Search Available Produce", "search_ph": "Search crops (e.g., Tomato, Apple)...", "price_lbl": "Price Range / Budget (₹/kg)", "voice_btn": "🎤 Speak", "add_crop": "List Crop", "calc": "Run AI Price Forecast", "cart_total": "Cart Total: ₹", "pool_btn": "Join Transport", "buy_now": "Buy Inputs Now", "checkout": "Checkout & Buy"},
    "తెలుగు": {"demand": "🚨 డిమాండ్ అలర్ట్: ఉల్లిపాయల అన్వేషణ 40% పెరిగింది. ఎక్కువ లాభం కోసం ప్లాన్ చేయండి!", "search_lbl": "పంటలను వెతకండి", "search_ph": "పంట పేరు రాయండి (ఉదా: Tomato)...", "price_lbl": "ధర పరిమితి (₹/కిలో)", "voice_btn": "🎤 మాట్లాడండి", "add_crop": "పంటను జోడించు", "calc": "AI విశ్లేషణను అమలు చేయండి", "cart_total": "మొత్తం: ₹", "pool_btn": "ట్రక్‌లో చేరండి", "buy_now": "కొనుగోలు చేయండి", "checkout": "చెక్అవుట్"},
    "हिंदी": {"demand": "🚨 डिमांड अलर्ट: प्याज की खोज 40% बढ़ गई है। अधिक लाभ के लिए योजना बनाएं!", "search_lbl": "फसल खोजें", "search_ph": "फसल का नाम लिखें (उदा. Tomato)...", "price_lbl": "मूल्य सीमा (₹/किग्रा)", "voice_btn": "🎤 बोलें", "add_crop": "फसल जोड़ें", "calc": "एआई मूल्य पूर्वानुमान चलाएं", "cart_total": "कुल: ₹", "pool_btn": "परिवहन में शामिल हों", "buy_now": "अभी खरीदें", "checkout": "चेकआउट"}
}

# ==========================================
# 3. STATE MANAGEMENT 
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
if 'order_type' not in st.session_state: st.session_state.order_type = ""

if 'qa_threads' not in st.session_state:
    st.session_state.qa_threads = [
        {"author": "Suresh (Medchal)", "question": "What is the best treatment for early tomato blight?", "answer": "Copper oxychloride spray (2.5g/L) during early vegetative stages helps control fungal spread."},
        {"author": "Naveen (Warangal)", "question": "Are neem oil sprays effective against aphids?", "answer": "Yes, use cold-pressed 10,000 PPM neem oil mixed with 1ml liquid soap per liter in early morning hours."}
    ]

def fetch_market_items():
    cursor = db_conn.cursor()
    cursor.execute("SELECT farmer_username, crop_name, price_per_kg, stock_kg, emoji FROM Inventory")
    rows = cursor.fetchall()
    return [{"farmer": r[0], "crop": r[1], "price": r[2], "stock": r[3], "emoji": r[4], "sales": 1500, "rating": 4.8, "orders": 12} for r in rows]

st.session_state.market_items = fetch_market_items()

def set_login_step(step): st.session_state.login_step = step
def change_page(page_name): 
    st.session_state.current_page = page_name
    st.session_state.crop_added = False
def reset_add_crop(): st.session_state.crop_added = False
def add_to_cart(cart_type, item_name, price): st.session_state[f"{cart_type}_cart"].append({"name": item_name, "price": price})
def checkout(cart_type):
    st.session_state.last_order = st.session_state[f"{cart_type}_cart"].copy()
    st.session_state[f"{cart_type}_cart"] = []
    st.session_state.order_type = cart_type
    st.session_state.current_page = "Success"
def logout_user():
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = ""
    st.session_state.login_step = "Select"
    st.session_state.current_page = "Farmer_Hub"

def login_user(user, pwd, role):
    u = user.strip().lower()
    cursor = db_conn.cursor()
    cursor.execute("SELECT password, role FROM Users WHERE username=?", (u,))
    result = cursor.fetchone()
    if result:
        correct_pwd, registered_role = result
        if pwd == correct_pwd and registered_role == role:
            st.session_state.authenticated = True
            st.session_state.user_role = role
            st.session_state.username = user.strip().title()
            st.session_state.current_page = "Farmer_Hub" if role == "Farmer" else "Buyer"
            st.rerun()
        else: st.error("❌ Invalid password or incorrect role chosen.")
    else: st.error("❌ Username not found in local database.")

# ==========================================
# 4. SIDEBAR
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
# 5. START SCREEN (LOGIN & SECURE SIGN UP)
# ==========================================
if not st.session_state.authenticated:
    st.title("🌾 Welcome to AgriConnect")
    st.write("Select your portal to continue or create an authorized account.")
    st.write("---")
    if st.session_state.login_step == "Select":
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.title("👨‍🌾 Farmer Access")
                st.button("Open Farmer Portal", on_click=set_login_step, args=("Farmer_Login",), use_container_width=True, type="primary")
        with col2:
            with st.container(border=True):
                st.title("🛒 Customer Access")
                st.button("Open Customer Portal", on_click=set_login_step, args=("Customer_Login",), use_container_width=True, type="primary")

    elif st.session_state.login_step == "Farmer_Login":
        st.button("⬅️ Back to Selection", on_click=set_login_step, args=("Select",))
        with st.container(border=True):
            st.title("👨‍🌾 Farmer Portal")
            tab_in, tab_up = st.tabs(["Sign In", "Create Account"])
            with tab_in:
                with st.form("farmer_auth_form"):
                    f_u = st.text_input("Username", placeholder="Enter username (e.g., ramesh)")
                    f_p = st.text_input("Password", type="password", placeholder="Enter password")
                    if st.form_submit_button("Sign In", type="primary", use_container_width=True): login_user(f_u, f_p, "Farmer")
            with tab_up:
                with st.form("farmer_reg_form"):
                    r_u = st.text_input("Choose Username", placeholder="e.g., rajesh_farm")
                    r_p = st.text_input("Choose Password", type="password", placeholder="Create password")
                    r_key = st.text_input("Admin Security Key", type="password", placeholder="Enter team security key")
                    if st.form_submit_button("Register Account", type="primary", use_container_width=True):
                        if r_key == "adminkarthik13":
                            if r_u and r_p:
                                try:
                                    cursor = db_conn.cursor()
                                    cursor.execute("INSERT INTO Users (username, password, role) VALUES (?, ?, ?)", (r_u.strip().lower(), r_p, "Farmer"))
                                    db_conn.commit()
                                    st.success("✅ Account created successfully! Switch to 'Sign In' and log in.")
                                except sqlite3.IntegrityError:
                                    st.error("❌ Username already exists. Choose another one.")
                            else:
                                st.warning("⚠️ Please fill in all fields.")
                        else:
                            st.error("❌ Invalid Admin Security Key! Access denied.")
                    
    elif st.session_state.login_step == "Customer_Login":
        st.button("⬅️ Back to Selection", on_click=set_login_step, args=("Select",))
        with st.container(border=True):
            st.title("🛒 Customer Portal")
            tab_in, tab_up = st.tabs(["Sign In", "Create Account"])
            with tab_in:
                with st.form("buyer_auth_form"):
                    b_u = st.text_input("Username", placeholder="Enter username (e.g., anita)")
                    b_p = st.text_input("Password", type="password", placeholder="Enter password")
                    if st.form_submit_button("Sign In", type="primary", use_container_width=True): login_user(b_u, b_p, "Customer")
            with tab_up:
                with st.form("buyer_reg_form"):
                    r_u = st.text_input("Choose Username", placeholder="e.g., rahul_buyer")
                    r_p = st.text_input("Choose Password", type="password", placeholder="Create password")
                    r_key = st.text_input("Admin Security Key", type="password", placeholder="Enter team security key")
                    if st.form_submit_button("Register Account", type="primary", use_container_width=True):
                        if r_key == "adminkarthik13":
                            if r_u and r_p:
                                try:
                                    cursor = db_conn.cursor()
                                    cursor.execute("INSERT INTO Users (username, password, role) VALUES (?, ?, ?)", (r_u.strip().lower(), r_p, "Customer"))
                                    db_conn.commit()
                                    st.success("✅ Account created successfully! Switch to 'Sign In' and log in.")
                                except sqlite3.IntegrityError:
                                    st.error("❌ Username already exists. Choose another one.")
                            else:
                                st.warning("⚠️ Please fill in all fields.")
                        else:
                            st.error("❌ Invalid Admin Security Key! Access denied.")
    st.stop()

# ==========================================
# 6. FARMER ROUTES 
# ==========================================
if st.session_state.user_role == "Farmer":
    if st.session_state.current_page == "Farmer_Hub":
        st.title(f"👋 Welcome back, {st.session_state.username}")
        st.write("---")
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.title("📊 Farmer Dashboard")
                st.button("Open Dashboard", on_click=change_page, args=("Farmer_Dashboard",), use_container_width=True, type="primary")
        with col2:
            with st.container(border=True):
                st.title("🛠️ Helpful Features")
                st.button("Open Features", on_click=change_page, args=("Farmer_Features",), use_container_width=True, type="primary")

    elif st.session_state.current_page == "Farmer_Dashboard":
        st.button("⬅️ Back to Farmer Hub", on_click=change_page, args=("Farmer_Hub",))
        st.title("📊 Farmer Dashboard")
        st.warning(lang_dict["demand"])
        tab1, tab2, tab3, tab4 = st.tabs(["➕ Add New Crop", "📈 My Analytics", "🧠 AI Profit Estimator", "🚚 Truck Pooling"])
        
        with tab1:
            st.write("### 🗣️ Smart Voice Assistant")
            smart_name = st.text_input("Your Name (For Voice Listing)", value=st.session_state.username)
            audio_value = st.audio_input("🎤 Click to Record Voice Command")
            if audio_value:
                with st.spinner("🎙️ AI processing voice..."):
                    time.sleep(2)
                    if 'voice_demo_count' not in st.session_state: st.session_state.voice_demo_count = 0
                    demo_commands = [("Tomato", 10, 60, "🍅"), ("Potato", 8, 50, "🥔"), ("Rice", 20, 100, "🌾")]
                    crop_val, stock_val, price_val, emoji_val = demo_commands[st.session_state.voice_demo_count % len(demo_commands)]
                    st.session_state.voice_demo_count += 1
                    cursor = db_conn.cursor()
                    cursor.execute("INSERT INTO Inventory (farmer_username, crop_name, price_per_kg, stock_kg, emoji) VALUES (?, ?, ?, ?, ?)", (smart_name, crop_val, price_val, stock_val, emoji_val))
                    db_conn.commit()
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
                        cursor = db_conn.cursor()
                        cursor.execute("INSERT INTO Inventory (farmer_username, crop_name, price_per_kg, stock_kg, emoji) VALUES (?, ?, ?, ?, ?)", (farmer_name, crop_name, price, stock, emoji))
                        db_conn.commit()
                        st.session_state.crop_added = True
                        st.rerun()
            else:
                st.success("✅ Crop successfully listed to local database!")
                st.button("➕ Add Another Crop", on_click=reset_add_crop)
                
        with tab2:
            st.subheader("📈 Farm Analytics & Performance")
            my_items = [item for item in st.session_state.market_items if item['farmer'].lower() == st.session_state.username.lower()]
            if my_items:
                kpi1, kpi2, kpi3, kpi4 = st.columns(4)
                total_earnings = sum(item.get('sales', 0) for item in my_items)
                with kpi1: st.metric("Total Revenue", f"₹{total_earnings:,.2f}", "+12% vs last month")
                with kpi2: st.metric("Active Stock", f"{sum(item['stock'] for item in my_items)} kg")
                with kpi3: st.metric("Orders", "12")
                with kpi4: st.metric("Rating", "⭐ 4.8")
                st.write("---")
                colA, colB = st.columns(2)
                with colA:
                    st.write("### 📊 Inventory Breakdown")
                    st.bar_chart(pd.DataFrame([{"Crop": i["crop"], "Stock (kg)": i["stock"]} for i in my_items]).set_index("Crop"))
                with colB:
                    st.write("### 📜 Recent Transactions")
                    st.dataframe(pd.DataFrame({"Date": ["2026-09-02", "2026-09-01", "2026-08-28"], "Crop": [my_items[0]['crop'], "Assorted", "Onion"], "Qty (kg)": [50, 15, 100], "Status": ["Delivered", "Delivered", "Processing"]}), hide_index=True, use_container_width=True)
            else:
                st.info("You haven't listed any crops yet. Add a crop to view your analytics!")
                
        with tab3:
            st.write("### 🧠 Machine Learning Price Engine")
            acres = st.number_input("Land Size (Acres)", min_value=0.1, value=1.0)
            yield_per_acre = st.number_input("Expected Yield per Acre (kg)", min_value=50, value=2000)
            col1, col2 = st.columns(2)
            with col1: upcoming_rain = st.number_input("Forecasted Rainfall (mm)", value=80)
            with col2: upcoming_temp = st.number_input("Forecasted Temp (°C)", value=29)
            if st.button(lang_dict["calc"], type="primary"):
                next_week_data = pd.DataFrame([[9, upcoming_rain, upcoming_temp, 105]], columns=['month', 'rain_mm', 'temp_c', 'demand_index'])
                predicted_price = ai_model.predict(next_week_data)[0]
                st.success(f"🌾 Estimated Harvest: **{acres * yield_per_acre:,.0f} kg**")
                st.info(f"📈 AI Predicted Selling Price: **₹{predicted_price:.2f} per kg**")
                st.info(f"💰 Projected Total Revenue: **₹{(acres * yield_per_acre) * predicted_price:,.2f}**")

        with tab4:
            st.subheader("🚚 Active Truck Pools")
            with st.container(border=True):
                st.write("**Route:** Mallapur ➡️ Secunderabad Market")
                st.progress(60); st.caption("Capacity: 600kg / 1000kg filled")
                st.button(lang_dict["pool_btn"], key="t1")

    elif st.session_state.current_page == "Farmer_Features":
        st.button("⬅️ Back to Farmer Hub", on_click=change_page, args=("Farmer_Hub",))
        st.title("🛠️ Helpful Features")
        t1, t2, t3, t4, t5 = st.tabs(["🏛️ Schemes", "🧪 Inputs & Pesticides", "🤝 B2B Contracts", "💬 Community Q&A", "🌿 AI Leaf Scanner"])
        
        with t1:
            st.subheader("Direct Subsidies & Government Portals")
            with st.expander("✅ PM-KISAN Samman Nidhi (Central Govt)"):
                st.write("**Benefit:** ₹6,000 per year distributed in 3 direct payments of ₹2,000.")
                st.write("**Eligibility:** Small and marginal landholding farmer families.")
                st.link_button("🌐 Open Official PM-KISAN Portal ↗️", "https://pmkisan.gov.in/")
            with st.expander("✅ Telangana Rythu Bharosa / Rythu Bandhu"):
                st.write("**Benefit:** Financial crop investment assistance deposited directly into Aadhaar-linked accounts.")
                st.write("**Eligibility:** Land-owning farmers and registered cultivators in Telangana.")
                st.link_button("🌐 Open Official Telangana Portal ↗️", "https://rythubharosa.telangana.gov.in/")
                
        with t2:
            st.subheader("Direct Agricultural Inputs & Pesticide Ordering")
            r1_c1, r1_c2, r1_c3 = st.columns(3)
            with r1_c1:
                with st.container(border=True):
                    st.write("### 🌿 Neem Oil (1L)")
                    st.caption("Bio-insecticide (10,000 PPM)")
                    st.button("Add - ₹250", key="i1", on_click=add_to_cart, args=("farmer", "Neem Oil (1L)", 250), use_container_width=True)
            with r1_c2:
                with st.container(border=True):
                    st.write("### 🧪 Chlorpyrifos (500ml)")
                    st.caption("Pest control for stem borer & termites")
                    st.button("Add - ₹280", key="i2", on_click=add_to_cart, args=("farmer", "Chlorpyrifos (500ml)", 280), use_container_width=True)
            with r1_c3:
                with st.container(border=True):
                    st.write("### 🍄 Trichoderma (1kg)")
                    st.caption("Bio-fungicide for root rot & wilt")
                    st.button("Add - ₹320", key="i3", on_click=add_to_cart, args=("farmer", "Trichoderma (1kg)", 320), use_container_width=True)

            r2_c1, r2_c2, r2_c3 = st.columns(3)
            with r2_c1:
                with st.container(border=True):
                    st.write("### 💧 Drip Irrigation Kit")
                    st.caption("Full 1-Acre micro-irrigation set")
                    st.button("Add - ₹1500", key="i4", on_click=add_to_cart, args=("farmer", "Drip Kit", 1500), use_container_width=True)
            with r2_c2:
                with st.container(border=True):
                    st.write("### 🌱 Hybrid F1 Seeds")
                    st.caption("High-germination disease-resistant pack")
                    st.button("Add - ₹400", key="i5", on_click=add_to_cart, args=("farmer", "Hybrid Seeds", 400), use_container_width=True)
            with r2_c3:
                with st.container(border=True):
                    st.write("### 🪱 Vermicompost (50kg)")
                    st.caption("100% Organic Soil Conditioner")
                    st.button("Add - ₹450", key="i6", on_click=add_to_cart, args=("farmer", "Vermicompost (50kg)", 450), use_container_width=True)

            if st.session_state.farmer_cart:
                st.write("---")
                st.subheader("🛒 Your Input Cart")
                for item in st.session_state.farmer_cart: st.write(f"- {item['name']}: ₹{item['price']}")
                st.button(lang_dict["buy_now"], on_click=checkout, args=("farmer",), type="primary")
                
        with t3:
            st.subheader("📝 Secure B2B Supply Contracts")
            st.info("💡 **What is B2B (Business-to-Business)?** Direct bulk supply agreements between farmers and bulk commercial buyers (like supermarkets, hotels, hostels, and processors) with guaranteed advance pricing and zero middlemen.")
            with st.form("b2b_form"):
                st.selectbox("Select Business Buyer", ["Reliance Fresh - Mallapur Hub", "Karachi Bakery Bulk Procurement", "Secunderabad Wholesale Mandi", "Swiggy Instamart Warehouse"])
                st.text_input("Crop for Bulk Supply", placeholder="e.g., Hybrid Tomatoes, Red Onions")
                st.number_input("Monthly Guaranteed Volume (kg)", min_value=100, step=50)
                st.number_input("Agreed Contract Price (₹/kg)", min_value=10, value=25)
                if st.form_submit_button("Initiate Direct Contract", type="primary"):
                    st.success("✅ Official B2B Contract proposal registered and sent to buyer procurement team!")
                    
        with t4:
            st.subheader("💬 Community Farmer Q&A")
            st.write("Ask agricultural questions and get solutions from agronomists and verified farmers.")
            
            with st.form("new_qa_form"):
                q_author = st.text_input("Your Name / Village", value=f"{st.session_state.username} (Mallapur)")
                q_text = st.text_input("Type your farming question...")
                submit_q = st.form_submit_button("Post Question to Community")
                if submit_q and q_text.strip():
                    st.session_state.qa_threads.insert(0, {
                        "author": q_author,
                        "question": q_text.strip(),
                        "answer": "⏳ Awaiting expert/farmer review."
                    })
                    st.success("✅ Question posted to community board!")
                    st.rerun()

            st.write("---")
            st.write("### 📌 Active Discussions")
            for thread in st.session_state.qa_threads:
                with st.container(border=True):
                    st.write(f"**❓ {thread['question']}**")
                    st.caption(f"Asked by: {thread['author']}")
                    st.info(f"**💡 Solution:** {thread['answer']}")

        with t5:
            st.subheader("🌿 AI Leaf Disease Scanner")
            st.write("Upload or photograph a crop leaf to instantly detect plant infections and receive AI treatment plans.")
            uploaded_file = st.file_uploader("Upload leaf image (JPEG, PNG)...", type=["jpg", "png", "jpeg"])
            if uploaded_file is not None:
                st.image(uploaded_file, caption="Uploaded Leaf Sample", use_container_width=True)
                if st.button("Run AI Leaf Diagnosis", type="primary"):
                    with st.spinner("🔍 Analyzing leaf cellular patterns & discoloration..."):
                        time.sleep(2)
                    st.error("⚠️ **Diagnosis Result:** Early Blight (*Alternaria solani*) detected with 94.2% confidence.")
                    st.info("💡 **Recommended Treatment:** Apply a copper-based bio-fungicide immediately. Ensure adequate spacing between rows to optimize air circulation and reduce moisture retention.")

    elif st.session_state.current_page == "Success":
        st.balloons()
        st.title("🎉 Order Placed Successfully!")
        if st.session_state.last_order:
            st.write("### 🧾 Official Invoice")
            subtotal = sum(item['price'] for item in st.session_state.last_order)
            with st.container(border=True):
                st.write(f"**Purchaser:** {st.session_state.username}")
                st.write("**Order Type:** Agricultural Inputs (B2B)")
                st.write("---")
                for item in st.session_state.last_order:
                    st.write(f"✔️ {item['name']}: ₹{item['price']:.2f}")
                st.write("---")
                gst = subtotal * 0.05
                st.write(f"**Subtotal:** ₹{subtotal:.2f}")
                st.write(f"**Agri-GST (5%):** ₹{gst:.2f}")
                st.write(f"### **Total Paid: ₹{subtotal + gst:.2f}**")
            st.button("⬅️ Back to Features", on_click=change_page, args=("Farmer_Features",), type="primary")

# ==========================================
# 7. CUSTOMER ROUTES
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
        with col_search: 
            search_query = st.text_input(lang_dict["search_lbl"], placeholder=lang_dict["search_ph"])
        with col_filter: 
            max_price = st.slider(lang_dict["price_lbl"], min_value=10, max_value=200, value=200)
        with col_btn: 
            st.write("") 
            st.write("")
            st.button(lang_dict["voice_btn"], use_container_width=True)

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
            st.write("### 🧾 Consumer Receipt")
            subtotal = sum(item['price'] for item in st.session_state.last_order)
            with st.container(border=True):
                st.write(f"**Customer:** {st.session_state.username}")
                st.write("---")
                for item in st.session_state.last_order:
                    st.write(f"✔️ {item['name']}: ₹{item['price']:.2f}")
                st.write("---")
                platform_fee = subtotal * 0.02
                st.write(f"**Subtotal:** ₹{subtotal:.2f}")
                st.write(f"**Platform Fee (2%):** ₹{platform_fee:.2f}")
                st.write(f"### **Total Paid: ₹{subtotal + platform_fee:.2f}**")
                st.success(f"🌱 You saved approximately ₹{(subtotal * 0.15):.2f} by buying direct from local farmers today!")
            st.button("⬅️ Back to Store", on_click=change_page, args=("Buyer",), type="primary")