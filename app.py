import streamlit as st
import ee
import geemap.foliumap as geemap

# Initialize Earth Engine
ee.Initialize()

# Header and layout
st.set_page_config(layout="wide")
st.title("ระบบติดตาม GCVI พื้นที่เกี่ยวข้าว")
st.subheader("กล้า-แกร่ง • จังหวัดนครสวรรค์")

# Function to get GCVI image
@st.cache_data
def get_gcvi():
    province = ee.FeatureCollection("FAO/GAUL/2015/level1").filter(ee.Filter.eq('ADM1_NAME', 'Nakhon Sawan'))
    aoi = province.geometry()
    def add_gcvi(img):
        gcvi = img.expression('NIR / GREEN - 1', {
            'NIR': img.select('B8'),
            'GREEN': img.select('B3')
        }).rename('GCVI')
        return img.addBands(gcvi)

    s2 = ee.ImageCollection('COPERNICUS/S2_HARMONIZED')\
        .filterBounds(aoi)\
        .filterDate('2024-11-01', '2024-12-15')\
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))\
        .map(add_gcvi)

    return s2.select('GCVI').median().clip(aoi), aoi

# Get GCVI and AOI
gcvi_image, aoi = get_gcvi()
harvested = gcvi_image.lt(1.0).selfMask()
pixel_area = ee.Image.pixelArea().updateMask(harvested)

# === Apply bestEffort fix ===
area_stats = pixel_area.reduceRegion(
    reducer=ee.Reducer.sum(),
    geometry=aoi,
    scale=10,
    maxPixels=1e10,
    bestEffort=True
)

# === Calculate outputs ===
area_rai = area_stats.getNumber('area').divide(1600)
tons = area_rai.multiply(0.18)
trips = tons.divide(4)

# Display metrics
st.metric("พื้นที่เกี่ยวแล้ว (ไร่)", f"{area_rai.getInfo():,.0f}")
st.metric("ปริมาณฟางโดยประมาณ (ตัน)", f"{tons.getInfo():,.0f}")
st.metric("รถเกี่ยวที่ต้องใช้ (เที่ยว)", f"{trips.getInfo():,.0f}")

# Map viewer
m = geemap.Map()
m.centerObject(aoi, 8)
m.addLayer(gcvi_image, {"min": 0, "max": 2, "palette": ['yellow', 'green', 'darkgreen']}, "GCVI")
m.addLayer(harvested, {"palette": ['red']}, "เกี่ยวแล้ว")
m.to_streamlit(height=600)
