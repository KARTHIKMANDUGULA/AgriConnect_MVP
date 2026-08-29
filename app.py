
import streamlit as st

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="AgriConnect", layout="wide")

# --- 2. STATE MANAGEMENT & DATABASE ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
if 'crop_added' not in st.session_state:
    st.session_state.crop_added = False

# Shopping Carts
if 'farmer_cart' not in st.session_state:
    st.session_state.farmer_cart = []
if 'buyer_cart' not in st.session_state:
    st.session_state.buyer_cart = []

if 'market_items' not in st.session_state:
    st.session_state.market_items = [
        {"farmer": "Ramesh", "crop": "Tomatoes", "price": 30, "stock": 50, "emoji": "🍅"},
        {"farmer": "Suresh", "crop": "Onions", "price": 35, "stock": 200, "emoji": "🧅"},
    ]

# Navigation & Cart Functions
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
    # Empty the cart and go to success page
    if cart_type == 'farmer':
        st.session_state.farmer_cart = []
    elif cart_type == 'buyer':
        st.session_state.buyer_cart = []
    st.session_state.current_page = "Success"

# --- 3. HOME PAGE ---
if st.session_state.current_page == "Home":
    st.title("🌾 Welcome to AgriConnect")
    st.subheader("Select your portal to continue:")
    st.write("---") 
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.title("👨‍🌾 Farmer")
            st.write("List your fresh harvest directly to the market and set your own prices.")
            st.write("") 
            st.button("Open Farmer Portal", on_click=change_page, args=("Farmer",), use_container_width=True, type="primary")
            
    with col2:
        with st.container(border=True):
            st.title("🛠️ Other Helpful Features")
            st.write("Check government schemes, order pesticides, and access agricultural support tools.")
            st.write("")
            st.button("Open Features", on_click=change_page, args=("Features",), use_container_width=True, type="primary")

    with col3:
        with st.container(border=True):
            st.title("🛒 Customer")
            st.write("Browse fresh produce directly from local farms. Get better prices and quality.")
            st.write("")
            st.button("Open Customer Portal", on_click=change_page, args=("Buyer",), use_container_width=True, type="primary")


# --- 4. FARMER PORTAL ---
elif st.session_state.current_page == "Farmer":
    st.button("⬅️ Back to Home", on_click=change_page, args=("Home",))
    st.title("👨‍🌾 Farmer Listing Portal")
    
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
                    "farmer": farmer_name, "crop": crop_name, "price": price, "stock": stock, "emoji": emoji
                })
                st.session_state.crop_added = True
                st.rerun()
    else:
        st.success("✅ Crop successfully listed on the live market!")
        st.button("➕ Add Another Crop", on_click=reset_add_crop, type="primary")


# --- 5. OTHER HELPFUL FEATURES ---
elif st.session_state.current_page == "Features":
    st.button("⬅️ Back to Home", on_click=change_page, args=("Home",))
    st.title("🛠️ Other Helpful Features")
    
    tab1, tab2 = st.tabs(["🏛️ Government Schemes", "🧪 Order Pesticides & Inputs"])
    
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
        
        # Display Farmer Cart
        if st.session_state.farmer_cart:
            st.write("---")
            st.subheader("🛒 Your Cart")
            total = 0
            for item in st.session_state.farmer_cart:
                st.write(f"- {item['name']}: ₹{item['price']}")
                total += item['price']
            st.write(f"**Total: ₹{total}**")
            st.button("Buy Now", on_click=checkout, args=("farmer",), type="primary")


# --- 6. BUYER STOREFRONT ---
elif st.session_state.current_page == "Buyer":
    st.button("⬅️ Back to Home", on_click=change_page, args=("Home",))
    st.title("🛒 Live Buyer Storefront")
    
    cols = st.columns(3)
    for index, item in enumerate(reversed(st.session_state.market_items)):
        with cols[index % 3]:
            with st.container(border=True):
                st.title(f"{item['emoji']} {item['crop']}")
                st.caption(f"👨‍🌾 Grown by {item['farmer']}")
                st.subheader(f"₹{item['price']} / kg")
                
                # Pass crop name and price to the cart function
                st.button("Add to Cart", key=f"buy_{item['farmer']}_{item['crop']}", on_click=add_to_cart, args=("buyer", f"{item['crop']} ({item['farmer']})", item['price']), use_container_width=True)
                
    # Display Buyer Cart
    if st.session_state.buyer_cart:
        st.write("---")
        st.subheader("🛒 Your Grocery Cart")
        total = 0
        for item in st.session_state.buyer_cart:
            st.write(f"- {item['name']}: ₹{item['price']}")
            total += item['price']
        st.write(f"**Total: ₹{total}**")
        st.button("Checkout & Buy", on_click=checkout, args=("buyer",), type="primary")


# --- 7. SUCCESS SCREEN ---
elif st.session_state.current_page == "Success":
    st.balloons() # Triggers a balloon animation on screen!
    st.title("🎉 Order Placed Successfully!")
    st.success("Your order has been confirmed and is being processed.")
    st.write("Thank you for using AgriConnect.")
    st.write("")
    st.button("⬅️ Return to Home", on_click=change_page, args=("Home",), type="primary")