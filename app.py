import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import time
import textwrap
from datetime import datetime, timedelta

# 1. CẤU HÌNH TRANG
st.set_page_config(
    page_title="EOD Stock Dashboard - Pro UI",
    page_icon="📈",
    layout="wide"
)

# 2. CUSTOM CSS - FIX TRIỆT ĐỂ MÀU CHỮ DATE INPUT, CHỚP TRẮNG POPOVER/SELECTBOX, SCROLLBAR & CALENDAR
st.markdown("""
    <style>
    html, body, #root, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background-color: #0F111A !important;
        color: #E2E8F0 !important;
    }
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    /* ========================================================= */
    /* FIX CỰC ĐANH TOÀN BỘ THANH CUỘN (SCROLLBAR & BUTTONS)     */
    /* ========================================================= */

    ::-webkit-scrollbar,
    *::-webkit-scrollbar {
        width: 8px !important;
        height: 8px !important;
        background-color: #0F111A !important;
    }

    ::-webkit-scrollbar-track,
    *::-webkit-scrollbar-track {
        background: #0F111A !important;
        border-radius: 8px !important;
    }

    ::-webkit-scrollbar-thumb,
    *::-webkit-scrollbar-thumb {
        background: #2A2D42 !important;
        border-radius: 8px !important;
        border: 2px solid #0F111A !important;
    }

    ::-webkit-scrollbar-thumb:hover,
    *::-webkit-scrollbar-thumb:hover {
        background: #7C3AED !important;
    }

    ::-webkit-scrollbar-button,
    *::-webkit-scrollbar-button {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
        background-color: transparent !important;
    }

    ::-webkit-scrollbar-corner,
    *::-webkit-scrollbar-corner {
        background-color: #0F111A !important;
    }

    * {
        scrollbar-width: thin !important;
        scrollbar-color: #2A2D42 #0F111A !important;
    }

    /* Nền ứng dụng chính */
    .stApp {
        background-color: #0F111A !important;
        color: #E2E8F0 !important;
    }

    [data-testid="stHeader"] {
        background-color: #0F111A !important;
        color: #E2E8F0 !important;
    }

    /* ========================================================= */
    /* FIX MÀU CHỮ ĐỒNG BỘ CHO DATE INPUT VÀ TOÀN BỘ Ô INPUT     */
    /* ========================================================= */
    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] input,
    [data-testid="stDateInput"] input {
        color: #F1F5F9 !important;
        -webkit-text-fill-color: #F1F5F9 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
    }

    /* ========================================================= */
    /* Khung tổng của Calendar Popup */
    div[data-baseweb="popover"] div[data-baseweb="calendar"],
    div[data-baseweb="calendar"][data-baseweb="calendar"] {
        background-color: #161824 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    /* Ép nền tối cho TẤT CẢ các thẻ bên trong Calendar (đè ô trắng đệm đầu/cuối tháng) */
    div[data-baseweb="calendar"] *,
    div[data-baseweb="calendar"][data-baseweb="calendar"] *,
    div[data-baseweb="calendar"] div,
    div[data-baseweb="calendar"] [role="grid"],
    div[data-baseweb="calendar"] [role="row"],
    div[data-baseweb="calendar"] [role="gridcell"],
    div[data-baseweb="calendar"] [role="gridcell"] > div,
    div[data-baseweb="calendar"] [role="presentation"] {
        background-color: #161824 !important;
        background: #161824 !important;
        background-image: none !important;
        border-color: transparent !important;
        outline: none !important;
    }

    /* Chặn mọi pseudo-element (vòng tròn đỏ/trắng thường được vẽ bằng ::before/::after) */
    div[data-baseweb="calendar"] *::before,
    div[data-baseweb="calendar"] *::after {
        background: transparent !important;
        border-color: transparent !important;
        box-shadow: none !important;
        outline: none !important;
    }

    /* Header Title */
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #A78BFA 0%, #38BDF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        letter-spacing: -0.5px;
    }

    /* --- SIDEBAR STYLING --- */
    [data-testid="stSidebar"] {
        background-color: #161824 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    }

    [data-testid="stSidebar"] *, 
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p {
    color: #94A3B8 !important;
    font-size: 1rem !important;
    font-weight: 500;
}

/* Tiêu đề "⚙️ Bộ lọc" to hơn, nổi bật hơn */
[data-testid="stSidebar"] h3 {
    font-size: 1.3rem !important;
    color: #F1F5F9 !important;
    margin-bottom: 12px !important;
}

/* Label của từng field (Sàn giao dịch:, Danh sách..., v.v.) đậm và rõ hơn */
[data-testid="stSidebar"] label p {
    font-size: 1rem !important;
    color: #CBD5E1 !important;
    font-weight: 600 !important;
}

    /* FIX VIỀN KÉP KHUNG INPUT & SELECT */
    [data-testid="stSidebar"] div[data-baseweb="input"] {
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
        background-color: #1E2030 !important;
        box-shadow: none !important;
        overflow: hidden !important;
    }

    [data-testid="stSidebar"] div[data-baseweb="input"] > div,
    [data-testid="stSidebar"] div[data-baseweb="base-input"] {
        border: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
        outline: none !important;
    }

    [data-testid="stSidebar"] div[data-baseweb="input"] input,
    [data-testid="stSidebar"] div[data-baseweb="select"] > div {
        padding-top: 10px !important;
        padding-bottom: 10px !important;
        font-size: 1rem !important;
    }

    [data-testid="stSidebar"] [data-baseweb="tag"] {
        font-size: 0.95rem !important;
        padding: 4px 8px !important;
    }

    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stMultiSelect,
    [data-testid="stSidebar"] .stDateInput {
        margin-bottom: 6px !important;
    }

    /* --- FILE UPLOADER --- */
    [data-testid="stFileUploader"] {
        background-color: #1E2030 !important;
        border: 1px dashed rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 10px !important;
    }
    [data-testid="stFileUploader"] section {
        background-color: #1E2030 !important;
    }
    [data-testid="stFileUploader"] section > div {
        color: #94A3B8 !important;
    }
    [data-testid="stFileUploader"] button {
        background-color: #2A2D40 !important;
        color: #E2E8F0 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
    }

    /* ========================================================= */
    /* FIX TRIỆT ĐỂ KHOẢNG TRẮNG VÀ VÒNG ĐỎ TRONG CALENDAR       */
    /* (Chọn selector lặp lại để tăng specificity, thắng style   */
    /*  do BaseWeb/styletron chèn động sau CSS này)              */
    /* ========================================================= */

    /* Khung tổng của Calendar Popup */
    div[data-baseweb="popover"] div[data-baseweb="calendar"],
    div[data-baseweb="calendar"][data-baseweb="calendar"] {
        background-color: #161824 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    /* Ép nền tối cho TẤT CẢ các thẻ bên trong Calendar (đè ô trắng đệm đầu/cuối tháng) */
    div[data-baseweb="calendar"] *,
    div[data-baseweb="calendar"][data-baseweb="calendar"] *,
    div[data-baseweb="calendar"] div,
    div[data-baseweb="calendar"] [role="grid"],
    div[data-baseweb="calendar"] [role="row"],
    div[data-baseweb="calendar"] [role="gridcell"],
    div[data-baseweb="calendar"] [role="gridcell"] > div,
    div[data-baseweb="calendar"] [role="presentation"] {
        background-color: #161824 !important;
        background: #161824 !important;
        background-image: none !important;
    }

    /* Header (Tháng, Năm, Nút chuyển tháng) */
    div[data-baseweb="calendar"] header,
    div[data-baseweb="calendar"] header *,
    div[data-baseweb="calendar"] [data-baseweb="typo-label"],
    div[data-baseweb="calendar"] [role="button"] {
        background-color: #161824 !important;
        color: #F8FAFC !important;
        fill: #F8FAFC !important;
    }

    /* Hàng tiêu đề thứ (Su, Mo, Tu,...) */
    div[data-baseweb="calendar"] [role="month"] > div:first-child,
    div[data-baseweb="calendar"] [role="columnheader"],
    div[data-baseweb="calendar"] [role="columnheader"] * {
        background-color: #1E2030 !important;
        color: #94A3B8 !important;
    }

    /* Định dạng nút ngày thường */
    div[data-baseweb="calendar"] [role="gridcell"] button {
        background-color: transparent !important;
        color: #E2E8F0 !important;
        border-radius: 8px !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Hiệu ứng khi rê chuột qua ngày (Hover) */
    div[data-baseweb="calendar"] [role="gridcell"] button:enabled:hover {
        background-color: #2A2D42 !important;
        color: #A78BFA !important;
    }

    /* Đổi ngày được chọn thành màu Tím Neon bo góc nhẹ (Xóa hoàn toàn hình tròn đỏ chói) */
    div[data-baseweb="calendar"] [aria-selected="true"],
    div[data-baseweb="calendar"] [aria-selected="true"][aria-selected="true"],
    div[data-baseweb="calendar"] [aria-selected="true"] *,
    div[data-baseweb="calendar"] [aria-selected="true"] button,
    div[data-baseweb="calendar"] [aria-selected="true"] div {
        background-color: #7C3AED !important;
        background: #7C3AED !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(124, 58, 237, 0.4) !important;
        border: none !important;
    }

    /* Đổi vòng tròn Ngày Hiện Tại (Today) thành viền Tím nhạt tinh tế */
    div[data-baseweb="calendar"] [aria-current="date"],
    div[data-baseweb="calendar"] [aria-current="date"] * {
        border: 1px solid #A78BFA !important;
        color: #A78BFA !important;
        border-radius: 8px !important;
        box-shadow: none !important;
    }

    /* Ngày bị disable (kể cả ô đệm đầu/cuối tháng) */
    div[data-baseweb="calendar"] [aria-disabled="true"],
    div[data-baseweb="calendar"] [aria-disabled="true"] * {
        color: #334155 !important;
        background-color: #161824 !important;
        background: #161824 !important;
        opacity: 0.5 !important;
    }

    /* Xóa viền focus mặc định */
    div[data-baseweb="calendar"] *:focus {
        outline: none !important;
        box-shadow: none !important;
    }

    /* Submit Button - Hiệu ứng 3D (nổi khối, lún xuống khi bấm) */
    [data-testid="stSidebar"] button[kind="secondaryFormSubmit"] {
        background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 0 !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.2px !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.35) !important;
        position: relative !important;
        /* Lớp bóng dưới tạo cạnh khối 3D + bóng đổ nổi trên nền */
        box-shadow:
            0 4px 0 0 #5B21B6,
            0 4px 0 0 #5B21B6,
            0 8px 16px rgba(124, 58, 237, 0.45) !important;
        transform: translateY(0) !important;
        transition: transform 0.08s ease, box-shadow 0.08s ease, filter 0.15s ease !important;
    }

    [data-testid="stSidebar"] button[kind="secondaryFormSubmit"] p,
    [data-testid="stSidebar"] button[kind="secondaryFormSubmit"] div {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.35) !important;
    }

    [data-testid="stSidebar"] button[kind="secondaryFormSubmit"]:hover {
        filter: brightness(1.08) !important;
        box-shadow:
            0 4px 0 0 #5B21B6,
            0 10px 20px rgba(124, 58, 237, 0.55) !important;
    }

    /* Khi giữ chuột / bấm -> nút "lún" xuống như phím vật lý */
    [data-testid="stSidebar"] button[kind="secondaryFormSubmit"]:active {
        transform: translateY(4px) !important;
        box-shadow:
            0 0 0 0 #5B21B6,
            0 2px 6px rgba(124, 58, 237, 0.4) !important;
        filter: brightness(0.95) !important;
    }

    [data-testid="stSidebar"] button[kind="secondaryFormSubmit"]:focus {
        outline: none !important;
    }

    /* Metric Cards */
    [data-testid="stMetric"] {
        background: #161824 !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        padding: 18px 20px !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3) !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #F8FAFC !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #64748B !important;
    }

    /* Tabs Styling */
    button[data-baseweb="tab"] {
        color: #64748B !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    button[aria-selected="true"] {
        color: #A78BFA !important;
        border-bottom: 2px solid #8B5CF6 !important;
    }

    /* CSS BẢNG HTML CUSTOM */
    .custom-dark-table-container {
        background-color: #161824;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        overflow: hidden;
        margin-top: 10px;
        margin-bottom: 25px;
    }
    .custom-dark-table {
        width: 100%;
        border-collapse: collapse;
        font-family: 'Inter', sans-serif;
        color: #E2E8F0;
        font-size: 0.88rem;
    }
    .custom-dark-table th {
        background-color: #1E2030;
        color: #94A3B8;
        font-weight: 600;
        padding: 14px 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .custom-dark-table td {
        padding: 12px 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    }
    .custom-dark-table tr:hover {
        background-color: rgba(255, 255, 255, 0.03);
    }
    .text-left { text-align: left; }
    .text-right { text-align: right; }
    .pos-val { color: #34D399; font-weight: 600; }
    .neg-val { color: #F87171; font-weight: 600; }
    .neu-val { color: #94A3B8; font-weight: 600; }
    /* Border trái phân biệt thẻ Cao Nhất / Thấp Nhất trong khu vực nội dung chính */
    [data-testid="stMain"] [data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="stMetric"] {
        border-left: 3px solid #34D399 !important;
    }
    [data-testid="stMain"] [data-testid="stHorizontalBlock"] > div:nth-child(3) [data-testid="stMetric"] {
        border-left: 3px solid #F87171 !important;
    }
    /* Đồng bộ nền tối cho ô tìm kiếm & number_input ở khu vực nội dung chính (ngoài sidebar) */
    [data-testid="stMain"] [data-testid="stTextInput"] div[data-baseweb="input"],
    [data-testid="stMain"] [data-testid="stNumberInput"] div[data-baseweb="input"],
    [data-testid="stMain"] [data-testid="stTextInput"] div[data-baseweb="base-input"],
    [data-testid="stMain"] [data-testid="stNumberInput"] div[data-baseweb="base-input"] {
        background-color: #1E2030 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
    }

    [data-testid="stMain"] [data-testid="stTextInput"] input,
    [data-testid="stMain"] [data-testid="stNumberInput"] input {
        background-color: transparent !important;
        color: #F1F5F9 !important;
        -webkit-text-fill-color: #F1F5F9 !important;
    }

    /* Nút tăng/giảm (+/-) của number_input */
    [data-testid="stMain"] [data-testid="stNumberInputStepUp"],
    [data-testid="stMain"] [data-testid="stNumberInputStepDown"] {
        background-color: #2A2D40 !important;
        border-color: rgba(255, 255, 255, 0.12) !important;
    }
    [data-testid="stMain"] [data-testid="stNumberInputStepUp"] svg,
    [data-testid="stMain"] [data-testid="stNumberInputStepDown"] svg {
        fill: #E2E8F0 !important;
    }

    /* Placeholder text (chữ mờ "Tìm mã cổ phiếu") */
    [data-testid="stMain"] [data-testid="stTextInput"] input::placeholder {
        color: #64748B !important;
        -webkit-text-fill-color: #64748B !important;
    }
   /* Loading overlay khi bấm RELOAD */
    .dark-loading-overlay {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #161824;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 60px 20px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .dark-loading-spinner {
        width: 42px;
        height: 42px;
        border: 4px solid rgba(124, 58, 237, 0.2);
        border-top: 4px solid #7C3AED;
        border-radius: 50%;
        animation: dark-spin 0.8s linear infinite;
        margin-bottom: 18px;
    }
    @keyframes dark-spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .dark-loading-text {
        color: #A78BFA;
        font-weight: 600;
        font-size: 1.05rem;
        letter-spacing: 0.3px;
    }
    /* Loading toàn màn hình khi bấm RELOAD - thay thế hoàn toàn nội dung chính */
    .dark-loading-fullscreen {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 70vh;
    }
    .dark-loading-spinner {
        width: 48px;
        height: 48px;
        border: 4px solid rgba(124, 58, 237, 0.2);
        border-top: 4px solid #7C3AED;
        border-radius: 50%;
        animation: dark-spin 0.8s linear infinite;
        margin-bottom: 20px;
    }
    @keyframes dark-spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .dark-loading-text {
        color: #A78BFA;
        font-weight: 600;
        font-size: 1.15rem;
        letter-spacing: 0.3px;
    }
    </style>
""", unsafe_allow_html=True)

# 2b. JS "CHỐT CHẶN CUỐI" CHO CALENDAR
# Lý do cần thêm JS: mỗi khi popup calendar mở, BaseWeb (thư viện nền của
# st.date_input) tự sinh ra style mới (qua styletron) và style này được
# chèn vào <head> SAU CSS custom ở trên -> nó đè mất !important của mình.
# Đoạn script dưới dùng MutationObserver để "canh" mỗi lần DOM calendar
# thay đổi (đổi tháng, chọn ngày...) rồi ép lại inline style với
# 'important' ngay trên phần tử -> luôn thắng, không còn ô trắng/vòng đỏ.
components.html(
    """
    <script>
    (function() {
        function toRGB(str) {
            const m = str && str.match(/rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)/);
            return m ? [parseInt(m[1]), parseInt(m[2]), parseInt(m[3])] : null;
        }
        function isWhiteish(rgb) {
            return rgb && rgb[0] > 220 && rgb[1] > 220 && rgb[2] > 220;
        }
        function isReddish(rgb) {
            return rgb && rgb[0] > 170 && rgb[1] < 110 && rgb[2] < 110;
        }

        function applyCalendarFix() {
            const doc = window.parent.document;
            const calendar = doc.querySelector('div[data-baseweb="calendar"]');
            if (!calendar) return;

            const nodes = calendar.querySelectorAll('*');
            nodes.forEach(function(el) {
                const cs = window.getComputedStyle(el);
                const bg = toRGB(cs.backgroundColor);
                const border = toRGB(cs.borderColor);
                const shadow = toRGB(cs.boxShadow);
                const outline = toRGB(cs.outlineColor);

                const selectedLike = isReddish(border) || isReddish(shadow) || isReddish(outline) || isReddish(bg);
                const whiteLike = isWhiteish(bg);

                if (selectedLike) {
                    el.style.setProperty('background-color', '#7C3AED', 'important');
                    el.style.setProperty('background', '#7C3AED', 'important');
                    el.style.setProperty('border-color', '#7C3AED', 'important');
                    el.style.setProperty('outline-color', '#7C3AED', 'important');
                    el.style.setProperty('box-shadow', '0 2px 8px rgba(124, 58, 237, 0.4)', 'important');
                    el.style.setProperty('color', '#FFFFFF', 'important');
                    el.style.setProperty('border-radius', '8px', 'important');
                } else if (whiteLike) {
                    el.style.setProperty('background-color', '#161824', 'important');
                    el.style.setProperty('background', '#161824', 'important');
                    el.style.setProperty('box-shadow', 'none', 'important');
                    if (isWhiteish(border)) {
                        el.style.setProperty('border-color', 'transparent', 'important');
                    }
                }
            });
        }

        // --- Chỉ chạy setInterval khi calendar THỰC SỰ đang mở ---
        // Trước đây setInterval(150ms) chạy vô hạn suốt phiên làm việc dù
        // calendar đóng, gây tốn CPU không cần thiết. Giờ ta dùng
        // MutationObserver để phát hiện lúc nào calendar được thêm/xóa
        // khỏi DOM, và chỉ bật interval trong khoảng thời gian đó.
        let calendarInterval = null;

        function startIntervalIfNeeded() {
            const doc = window.parent.document;
            const calendarOpen = !!doc.querySelector('div[data-baseweb="calendar"]');

            if (calendarOpen && !calendarInterval) {
                applyCalendarFix();
                calendarInterval = setInterval(applyCalendarFix, 150);
            } else if (!calendarOpen && calendarInterval) {
                clearInterval(calendarInterval);
                calendarInterval = null;
            }
        }

        const observer = new MutationObserver(function() {
            startIntervalIfNeeded();
        });
        observer.observe(window.parent.document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['aria-selected', 'aria-current', 'class', 'style']
        });

        // Kiểm tra trạng thái ban đầu (phòng trường hợp calendar đã mở sẵn)
        startIntervalIfNeeded();
    })();
    </script>
    """,
    height=0,
    width=0,
)

# 3. HÀM NẠP VÀ XỬ LÝ DỮ LIỆU
@st.cache_data
def load_data_from_files():
    df_list = []

    files_config = {
        'HNX': 'CafeF.HNX.Upto10.08.2026.csv',
        'HOSE': 'CafeF.HSX.Upto10.08.2026.csv',
        'UPCOM': 'CafeF.UPCOM.Upto10.08.2026.csv'
    }
    for ex_name, f_path in files_config.items():
        if os.path.exists(f_path):
            temp_df = pd.read_csv(f_path)
            temp_df.columns = temp_df.columns.str.replace('<', '').str.replace('>', '').str.strip()
            temp_df = temp_df.dropna(subset=['Ticker'])
            temp_df['Ticker'] = temp_df['Ticker'].astype(str).str.strip()
            temp_df['Exchange'] = ex_name
            df_list.append(temp_df)

    if not df_list:
        return pd.DataFrame()

    combined_df = pd.concat(df_list, ignore_index=True)

    combined_df['DTYYYYMMDD'] = pd.to_datetime(
        combined_df['DTYYYYMMDD'].astype(str),
        format='%Y%m%d',
        errors='coerce'
    )

    n_before = len(combined_df)
    invalid_rows = combined_df[combined_df['DTYYYYMMDD'].isna()]
    if not invalid_rows.empty:
        combined_df = combined_df.dropna(subset=['DTYYYYMMDD'])
        n_dropped = n_before - len(combined_df)
        bad_tickers = sorted(invalid_rows['Ticker'].unique())[:10]
        st.warning(
            f"⚠️ Đã bỏ qua {n_dropped} dòng dữ liệu có ngày không hợp lệ "
            f"(ví dụ mã: {', '.join(bad_tickers)}{'...' if len(invalid_rows['Ticker'].unique()) > 10 else ''}). "
            f"Vui lòng kiểm tra lại file nguồn nếu số dòng bị bỏ qua quá nhiều."
        )

    # Chuẩn hoá giá theo TỪNG MÃ riêng biệt, tránh trường hợp 1 mã có giá nhỏ
    # (dạng nghìn đồng) nằm chung file với mã khác giá lớn khiến điều kiện
    # scale toàn cục bị sai, gây ra giá hiển thị vô lý (vd "7 đ").
    price_cols = ['Open', 'High', 'Low', 'Close']
    if not combined_df.empty:
        max_close_per_ticker = combined_df.groupby('Ticker')['Close'].transform('max')
        scale_mask = max_close_per_ticker < 500
        combined_df.loc[scale_mask, price_cols] = combined_df.loc[scale_mask, price_cols] * 1000

    return combined_df

# Đọc dữ liệu
df = load_data_from_files()

if df.empty:
    st.error("Không tìm thấy dữ liệu! Vui lòng chép các file CafeF CSV (HNX/HOSE/UPCOM) vào cùng thư mục với app.")
    st.stop()

exchanges = ["Tất cả"] + list(df['Exchange'].unique())
all_tickers = sorted([str(t) for t in df['Ticker'].unique()])

min_db_date = df['DTYYYYMMDD'].min().date()
max_db_date = df['DTYYYYMMDD'].max().date()
default_start_date = max(min_db_date, max_db_date - timedelta(days=365))

last_exchange = st.session_state.get('last_selected_exchange', 'Tất cả')
tickers_pool = all_tickers if last_exchange == "Tất cả" else sorted([str(t) for t in df[df['Exchange'] == last_exchange]['Ticker'].unique()])

default_watchlist = [t for t in ['VNM', 'FPT', 'SSI', 'HPG', 'VCB'] if t in tickers_pool]
if not default_watchlist and len(tickers_pool) >= 3:
    default_watchlist = tickers_pool[:5]

# --- SIDEBAR FORM ---
with st.sidebar.form("filter_form"):
    st.markdown("### ⚙️ Bộ lọc")
    
    selected_exchange = st.selectbox("Sàn giao dịch:", options=exchanges)
    
    watchlist = st.multiselect(
        "Danh sách cổ phiếu theo dõi:",
        options=all_tickers,
        default=default_watchlist
    )

    selected_ticker = st.selectbox(
        "Mã cổ phiếu phân tích chi tiết:", 
        options=all_tickers
    )

    col_s, col_e = st.columns(2)
    with col_s:
        start_date = st.date_input("Bắt đầu", value=default_start_date, min_value=min_db_date, max_value=max_db_date)
    with col_e:
        end_date = st.date_input("Kết thúc", value=max_db_date, min_value=min_db_date, max_value=max_db_date)

    selected_indicators = st.multiselect(
        "Chỉ báo kỹ thuật:",
        options=["SMA 20", "SMA 50", "EMA 20", "Bollinger Bands", "RSI (14)", "MACD"],
        default=["SMA 20"]
    )
    
    submit_button = st.form_submit_button("RELOAD", use_container_width=True)

st.session_state['last_selected_exchange'] = selected_exchange


# Lọc dữ liệu
filtered_df = df if selected_exchange == "Tất cả" else df[df['Exchange'] == selected_exchange]

date_filtered_df = filtered_df[
    (filtered_df['DTYYYYMMDD'].dt.date >= start_date) & 
    (filtered_df['DTYYYYMMDD'].dt.date <= end_date)
].copy()

# 4. GIAO DIỆN CHÍNH
main_placeholder = st.empty()

# Nếu vừa bấm RELOAD -> hiện màn hình loading thay thế TOÀN BỘ nội dung cũ
if submit_button:
    with main_placeholder.container():
        st.markdown(
            """
            <div class="dark-loading-fullscreen">
                <div class="dark-loading-spinner"></div>
                <div class="dark-loading-text">Đang tải dữ liệu...</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    time.sleep(0.6)

# Sau khi loading xong (hoặc không phải vừa bấm RELOAD) -> vẽ nội dung thật
# vào ĐÚNG placeholder đó, tự động thay thế màn hình loading
main_content = main_placeholder.container()

with main_content:
    st.markdown('<div class="main-header">Dữ liệu EOD thị trường chứng khoán Việt Nam</div>', unsafe_allow_html=True)

    tab_watchlist, tab_analysis, tab_market = st.tabs([
        "📊 Danh sách theo dõi", 
        "📈 Phân tích chi tiết", 
        "🌐 Toàn bộ thị trường"
    ])

# TAB 1: DANH SÁCH THEO DÕI
with tab_watchlist:
    st.subheader("Bảng theo dõi diễn biến giá các cổ phiếu quan tâm")
    
    if not watchlist:
        st.info("Vui lòng chọn ít nhất 1 cổ phiếu trong danh sách bên trái.")
    else:
        wl_data = []
        for ticker in watchlist:
            sub = date_filtered_df[date_filtered_df['Ticker'] == ticker].sort_values('DTYYYYMMDD')
            if not sub.empty:
                latest = sub.iloc[-1]
                prev = sub.iloc[-2]['Close'] if len(sub) > 1 else latest['Close']
                change = latest['Close'] - prev
                pct_change = (change / prev * 100) if prev != 0 else 0
                
                wl_data.append({
                    'Mã CK': ticker,
                    'Sàn': latest['Exchange'],
                    'Giá Đóng Cửa': latest['Close'],
                    'Thay Đổi': change,
                    '% Thay Đổi': pct_change,
                    'Cao Nhất (Kỳ)': sub['High'].max(),
                    'Thấp Nhất (Kỳ)': sub['Low'].min(),
                    'Tổng KLGD': sub['Volume'].sum(),
                    'Ngày Gần Nhất': latest['DTYYYYMMDD'].strftime('%d/%m/%Y')
                })

        if wl_data:
            rows_html = ""
            for item in wl_data:
                chg = item['Thay Đổi']
                cls = "pos-val" if chg > 0 else ("neg-val" if chg < 0 else "neu-val")
                chg_str = f"+{chg:,.2f}" if chg > 0 else f"{chg:,.2f}"
                pct_str = f"+{item['% Thay Đổi']:.2f}%" if item['% Thay Đổi'] > 0 else f"{item['% Thay Đổi']:.2f}%"

                rows_html += f"""<tr>
<td class="text-left" style="font-weight: 700; color: #F8FAFC;">{item['Mã CK']}</td>
<td class="text-left" style="color: #64748B;">{item['Sàn']}</td>
<td class="text-right">{item['Giá Đóng Cửa']:,.0f}</td>
<td class="text-right {cls}">{chg_str}</td>
<td class="text-right {cls}">{pct_str}</td>
<td class="text-right">{item['Cao Nhất (Kỳ)']:,.0f}</td>
<td class="text-right">{item['Thấp Nhất (Kỳ)']:,.0f}</td>
<td class="text-right">{item['Tổng KLGD']:,}</td>
<td class="text-left" style="color: #64748B;">{item['Ngày Gần Nhất']}</td>
</tr>"""

            raw_html = f"""
            <div class="custom-dark-table-container">
                <table class="custom-dark-table">
                    <thead>
                        <tr>
                            <th class="text-left">Mã CK</th>
                            <th class="text-left">Sàn</th>
                            <th class="text-right">Giá Đóng Cửa</th>
                            <th class="text-right">Thay Đổi</th>
                            <th class="text-right">% Thay Đổi</th>
                            <th class="text-right">Cao Nhất (Kỳ)</th>
                            <th class="text-right">Thấp Nhất (Kỳ)</th>
                            <th class="text-right">Tổng KLGD</th>
                            <th class="text-left">Ngày Gần Nhất</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
            </div>
            """
            
            st.markdown(textwrap.dedent(raw_html), unsafe_allow_html=True)

            st.markdown("<h4>So sánh biến động giá (%) trong kỳ</h4>", unsafe_allow_html=True)
            
            fig_comp = go.Figure()
            for ticker in watchlist:
                sub = date_filtered_df[date_filtered_df['Ticker'] == ticker].sort_values('DTYYYYMMDD')
                if not sub.empty:
                    base_price = sub.iloc[0]['Close']
                    if base_price > 0:
                        pct_series = ((sub['Close'] - base_price) / base_price) * 100
                        fig_comp.add_trace(go.Scatter(
                            x=sub['DTYYYYMMDD'], 
                            y=pct_series, 
                            mode='lines', 
                            name=ticker,
                            line=dict(width=2)
                        ))

            fig_comp.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])], gridcolor='rgba(255, 255, 255, 0.05)', tickformat="%d/%m/%Y")
            fig_comp.update_yaxes(gridcolor='rgba(255, 255, 255, 0.05)')
            fig_comp.update_layout(
                yaxis_title="Biến động (%)",
                height=380,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#94A3B8', family='Inter'),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_comp, use_container_width=True)

# TAB 2: PHÂN TÍCH CHI TIẾT
with tab_analysis:
    data = date_filtered_df[date_filtered_df['Ticker'] == selected_ticker].sort_values('DTYYYYMMDD').copy()

    if not data.empty:
        expected_sessions = max(1, int((end_date - start_date).days * 5 / 7))
        if len(data) < expected_sessions * 0.5:
            st.info(f"⚠️ Chỉ có {len(data)} phiên giao dịch trong khoảng thời gian đã chọn (dự kiến ~{expected_sessions} phiên). Dữ liệu có thể bị thiếu hoặc mã này ít giao dịch.")
        data['SMA20'] = data['Close'].rolling(window=20).mean()
        data['SMA50'] = data['Close'].rolling(window=50).mean()
        data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
        
        std20 = data['Close'].rolling(window=20).std()
        data['BB_Upper'] = data['SMA20'] + (std20 * 2)
        data['BB_Lower'] = data['SMA20'] - (std20 * 2)
        
        # RSI theo chuẩn Wilder (khớp với TradingView và đa số nền tảng khác),
        # dùng smoothing kiểu EMA với alpha = 1/14 thay vì rolling mean thông thường.
        delta = data['Close'].diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)

        avg_gain = gain.ewm(alpha=1/14, min_periods=14, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1/14, min_periods=14, adjust=False).mean()

        rs = avg_gain / avg_loss
        data['RSI'] = 100 - (100 / (1 + rs))

        # Trường hợp avg_loss = 0 (giá chỉ tăng liên tục, không giảm phiên nào)
        # -> rs = inf -> RSI đúng ra phải là 100, không phải NaN
        data.loc[(avg_loss == 0) & (avg_gain > 0), 'RSI'] = 100
        # Trường hợp cả gain và loss đều 0 (giá đứng yên hoàn toàn) -> RSI = 50 (trung tính)
        data.loc[(avg_loss == 0) & (avg_gain == 0), 'RSI'] = 50

        ema12 = data['Close'].ewm(span=12, adjust=False).mean()
        ema26 = data['Close'].ewm(span=26, adjust=False).mean()
        data['MACD'] = ema12 - ema26
        data['MACD_Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()

        latest = data.iloc[-1]
        prev_close = data.iloc[-2]['Close'] if len(data) > 1 else latest['Close']
        change = latest['Close'] - prev_close
        pct_change = (change / prev_close) * 100 if prev_close != 0 else 0

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Giá Đóng Cửa", f"{latest['Close']:,.0f} đ", f"{change:+,.2f} ({pct_change:+.2f}%)")
        k2.metric("Giá Cao Nhất", f"{data['High'].max():,.0f} đ")
        k3.metric("Giá Thấp Nhất", f"{data['Low'].min():,.0f} đ")
        k4.metric("Tổng Khối Lượng GD", f"{data['Volume'].sum():,}")

        st.markdown("<br>", unsafe_allow_html=True)

        if len(data) < 50 and any(ind in selected_indicators for ind in ["SMA 50", "RSI (14)", "MACD"]):
            st.caption("ℹ️ Khoảng thời gian ngắn hơn chu kỳ tính toán của một số chỉ báo (SMA 50, RSI, MACD) — các đường này có thể bị thiếu ở giai đoạn đầu biểu đồ.")

        has_rsi = "RSI (14)" in selected_indicators
        has_macd = "MACD" in selected_indicators
        
        rows_count = 2 + (1 if has_rsi else 0) + (1 if has_macd else 0)
        row_heights = [0.55] + [0.15] * (rows_count - 1)
        
        fig = make_subplots(
            rows=rows_count, cols=1, 
            shared_xaxes=True, 
            vertical_spacing=0.04, 
            row_heights=row_heights
        )

        fig.add_trace(go.Candlestick(
            x=data['DTYYYYMMDD'], open=data['Open'], high=data['High'],
            low=data['Low'], close=data['Close'], name="Giá",
            increasing_line_color='#38BDF8', increasing_fillcolor='#38BDF8',
            decreasing_line_color='#F43F5E', decreasing_fillcolor='#F43F5E'
        ), row=1, col=1)

        if "SMA 20" in selected_indicators:
            fig.add_trace(go.Scatter(x=data['DTYYYYMMDD'], y=data['SMA20'], name="SMA 20", line=dict(color='#FBBF24', width=1.5)), row=1, col=1)
        if "SMA 50" in selected_indicators:
            fig.add_trace(go.Scatter(x=data['DTYYYYMMDD'], y=data['SMA50'], name="SMA 50", line=dict(color='#60A5FA', width=1.5)), row=1, col=1)
        if "EMA 20" in selected_indicators:
            fig.add_trace(go.Scatter(x=data['DTYYYYMMDD'], y=data['EMA20'], name="EMA 20", line=dict(color='#C084FC', width=1.5)), row=1, col=1)
        if "Bollinger Bands" in selected_indicators:
            fig.add_trace(go.Scatter(x=data['DTYYYYMMDD'], y=data['BB_Upper'], name="BB Upper", line=dict(color='#64748B', dash='dot')), row=1, col=1)
            fig.add_trace(go.Scatter(x=data['DTYYYYMMDD'], y=data['BB_Lower'], name="BB Lower", line=dict(color='#64748B', dash='dot')), row=1, col=1)

        colors = ['#38BDF8' if c >= o else '#F43F5E' for c, o in zip(data['Close'], data['Open'])]
        curr_row = 2
        fig.add_trace(go.Bar(x=data['DTYYYYMMDD'], y=data['Volume'], marker_color=colors, name="Volume"), row=curr_row, col=1)

        if has_rsi:
            curr_row += 1
            fig.add_trace(go.Scatter(x=data['DTYYYYMMDD'], y=data['RSI'], name="RSI (14)", line=dict(color='#A78BFA', width=1.5)), row=curr_row, col=1)
            fig.add_hline(y=70, line_dash="dash", line_color="#F43F5E", row=curr_row, col=1,
                          annotation_text="Quá mua (70)", annotation_position="top left",
                          annotation_font_size=10, annotation_font_color="#F43F5E")
            fig.add_hline(y=30, line_dash="dash", line_color="#34D399", row=curr_row, col=1,
                          annotation_text="Quá bán (30)", annotation_position="bottom left",
                          annotation_font_size=10, annotation_font_color="#34D399")

        if has_macd:
            curr_row += 1
            fig.add_trace(go.Scatter(x=data['DTYYYYMMDD'], y=data['MACD'], name="MACD", line=dict(color='#38BDF8', width=1.5)), row=curr_row, col=1)
            fig.add_trace(go.Scatter(x=data['DTYYYYMMDD'], y=data['MACD_Signal'], name="Signal", line=dict(color='#FBBF24', width=1.5)), row=curr_row, col=1)

        fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])], gridcolor='rgba(255, 255, 255, 0.05)', tickformat="%d/%m/%Y")
        fig.update_yaxes(gridcolor='rgba(255, 255, 255, 0.05)')

        fig.update_layout(
            xaxis_rangeslider_visible=False,
            height=650 + (90 * (rows_count - 2)),
            margin=dict(l=10, r=10, t=20, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94A3B8', family='Inter'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"Không có dữ liệu cho mã **{selected_ticker}** trong khoảng thời gian đã chọn. Vui lòng đổi mã hoặc mở rộng khoảng ngày.")
# TAB 3: TOÀN BỘ THỊ TRƯỜNG
@st.cache_data
def compute_market_summary(sub_df):
    """Tính bảng tổng quan thị trường - chỉ chạy lại khi dữ liệu đầu vào thay đổi
    (đổi sàn / đổi khoảng ngày), KHÔNG chạy lại khi gõ tìm kiếm hay đổi top_n."""
    summary_data = []
    for ticker, group in sub_df.groupby('Ticker'):
        group_sorted = group.sort_values('DTYYYYMMDD')
        if len(group_sorted) > 0:
            last_p = group_sorted.iloc[-1]['Close']
            first_p = group_sorted.iloc[0]['Close']
            p_change = last_p - first_p
            pct = (p_change / first_p * 100) if first_p != 0 else 0
            vol_sum = group_sorted['Volume'].sum()
            summary_data.append({
                'Mã CK': ticker,
                'Giá Đóng Cửa': last_p,
                'Thay Đổi': p_change,
                '% Thay Đổi': pct,
                'Tổng Khối Lượng': vol_sum
            })
    return sorted(summary_data, key=lambda x: x['% Thay Đổi'], reverse=True)


with tab_market:
    st.subheader(f"Bảng tổng quan thị trường ({selected_exchange})")

    if not date_filtered_df.empty:
        # Chỉ tính toán nặng (groupby) khi date_filtered_df thay đổi, nhờ cache_data
        full_summary_data = compute_market_summary(date_filtered_df)

        col_search, col_limit = st.columns([2, 1])
        with col_search:
            search_term = st.text_input("🔍 Tìm mã cổ phiếu", "").strip().upper()
        with col_limit:
            top_n = st.number_input(
                "Số dòng hiển thị",
                min_value=10,
                max_value=max(10, len(full_summary_data)),
                value=min(100, len(full_summary_data)),
                step=10
            )

        # Lọc theo search - nhẹ, chỉ duyệt list đã tính sẵn, không groupby lại
        if search_term:
            summary_data = [item for item in full_summary_data if search_term in item['Mã CK']]
        else:
            summary_data = full_summary_data

        total_matches = len(summary_data)
        summary_data = summary_data[:top_n]
        st.caption(f"Hiển thị {len(summary_data)} / {total_matches} mã phù hợp")

        mkt_rows = ""
        for item in summary_data:
            chg = item['Thay Đổi']
            cls = "pos-val" if chg > 0 else ("neg-val" if chg < 0 else "neu-val")
            chg_str = f"+{chg:,.2f}" if chg > 0 else f"{chg:,.2f}"
            pct_str = f"+{item['% Thay Đổi']:.2f}%" if item['% Thay Đổi'] > 0 else f"{item['% Thay Đổi']:.2f}%"

            mkt_rows += f"""<tr>
<td class="text-left" style="font-weight: 700; color: #F8FAFC;">{item['Mã CK']}</td>
<td class="text-right">{item['Giá Đóng Cửa']:,.0f}</td>
<td class="text-right {cls}">{chg_str}</td>
<td class="text-right {cls}">{pct_str}</td>
<td class="text-right">{item['Tổng Khối Lượng']:,}</td>
</tr>"""

        mkt_table_raw = f"""
        <div class="custom-dark-table-container">
            <table class="custom-dark-table">
                <thead>
                    <tr>
                        <th class="text-left">Mã CK</th>
                        <th class="text-right">Giá Đóng Cửa</th>
                        <th class="text-right">Thay Đổi</th>
                        <th class="text-right">% Thay Đổi</th>
                        <th class="text-right">Tổng Khối Lượng</th>
                    </tr>
                </thead>
                <tbody>
                    {mkt_rows}
                </tbody>
            </table>
        </div>
        """
        st.markdown(textwrap.dedent(mkt_table_raw), unsafe_allow_html=True)