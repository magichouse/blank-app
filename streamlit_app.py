import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import qrcode
import io

# Constants for label dimensions and margins
LABEL_WIDTH_MM = 38
LABEL_HEIGHT_MM = 22
MARGIN_MM = 2

# Conversion factors
MM_TO_PIXELS = 3.78  # Assuming 96 DPI

# Dimensions in pixels
LABEL_WIDTH_PX = int(LABEL_WIDTH_MM * MM_TO_PIXELS)
LABEL_HEIGHT_PX = int(LABEL_HEIGHT_MM * MM_TO_PIXELS)
MARGIN_PX = int(MARGIN_MM * MM_TO_PIXELS)

def create_label(product_name, price, url):
    # Create an empty label image
    label = Image.new("RGB", (LABEL_WIDTH_PX, LABEL_HEIGHT_PX), "white")
    draw = ImageDraw.Draw(label)

    # Generate QR code
    qr = qrcode.QRCode(box_size=2, border=0)
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill='black', back_color='white')
    qr_width, qr_height = qr_img.size
    qr_img = qr_img.resize((qr_width, qr_height))

    # Add QR code to label
    label.paste(qr_img, (MARGIN_PX, MARGIN_PX))

    # Load a font
    font_size = 10
    font = ImageFont.truetype("arial.ttf", font_size)

    # Add product name
    text_x = qr_width + 2 * MARGIN_PX
    text_y = MARGIN_PX
    draw.text((text_x, text_y), product_name, font=font, fill="black")

    # Add price
    price_y = text_y + 20  # Adjust as necessary for spacing
    draw.text((text_x, price_y), f"Price: ${price}", font=font, fill="black")

    return label

# Streamlit interface
st.title("Product Label Generator")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write(df)
    
    if st.button("Generate Labels"):
        labels = []
        for index, row in df.iterrows():
            product_name = row["Product Name"]
            price = row["Price"]
            url = row["URL"]
            label_img = create_label(product_name, price, url)
            labels.append(label_img)
            
            # Display label
            st.image(label_img, caption=f"Label for {product_name}")
            
            # Option to download each label
            buffer = io.BytesIO()
            label_img.save(buffer, format="PNG")
            buffer.seek(0)
            st.download_button(f"Download Label for {product_name}", buffer, file_name=f"{product_name}_label.png", mime="image/png")
else:
    st.info("Please upload a CSV file with columns: Product Name, Price, URL.")
