import streamlit as st
css = """
<style>
    div[data-testid="stSidebarNav"] {
        display: block;
        height: 40px;
        width: 0px;
    }
    
    /* Fullscreen overlay */
    #loadingOverlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255, 255, 255, 0.8);
        z-index: 9999;
        cursor: progress;
        transition: opacity 0.5s ease-in-out;
    }

    .loader {
        position: absolute;
        top: 50%;
        left: 50%;
        border: 16px solid #f3f3f3;
        border-top: 16px solid #3498db;
        border-radius: 50%;
        width: 80px;
        height: 80px;
        animation: spin 2s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    body.loading {
        overflow: hidden;
        pointer-events: none;
        user-select: none;
        filter: blur(5px);
    }

    #loadingOverlay.fade-out {
        opacity: 0;
        pointer-events: none;
    }
</style>
"""

st.markdown(css, unsafe_allow_html=True)


js = """
<script>
    function checkStreamlitIsLoaded() {
        // Check if any Streamlit element is loaded
        if (document.querySelector('div[data-baseweb="button"]')) {
            document.body.classList.remove('loading');
            var overlay = document.getElementById('loadingOverlay');
            if (overlay) {
                overlay.classList.add('fade-out');
                setTimeout(() => {
                    if (overlay) {
                        overlay.style.display = 'none';
                    }
                }, 500);  // Wait for the fade-out animation to complete before hiding
            }
        } else {
            setTimeout(checkStreamlitIsLoaded, 100);  // Check every 100ms
        }
    }

    // Start checking when document is ready
    document.addEventListener('DOMContentLoaded', checkStreamlitIsLoaded);
</script>
"""

st.markdown(css, unsafe_allow_html=True)
st.markdown(js, unsafe_allow_html=True)


# Display the loading overlay
st.markdown("""
<div id="loadingOverlay">
    <div class="loader"></div>
</div>
""", unsafe_allow_html=True)
