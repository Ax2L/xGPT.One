
import streamlit as st

# * === Menu Content Box ---------------> Datastore

def datastore_box():
    """Renders the datastore box in the header."""
    # Title and Explanation
    st.markdown("## Datastore Tools")
    st.markdown(
        "Here, manage your **local files** and get an overview of "
        "the **Vector Database** using Attu and Milvus. "
        "_Further explanations and guides will be added soon._"
    )
    # Local Files Section
    with st.expander("Local Files"):
        st.markdown("Browse, upload, or manage your local files seamlessly.")
        if st.button("Open Filebrowser"):
            change_page_extended("data_file_manager")
    # Vector Database Section
    with st.expander("Vector Database (Milvus)"):
        st.markdown(
            "Utilize **Attu** to get an overview of Milvus. The default "
            "user credentials are configured in the `docker-compose` file and are as follows:\n"
            "- **Username:** minioadmin\n"
            "- **Password:** minioadmin\n\n"
            "_The configuration file path:_\n"
            "`helper/docker/docker-compose-db.yaml`"
        )
        # Note: Streamlit does not support `on_click` URL redirect via button yet.
        # Using `st.markdown` to create a hyperlink.
        st.markdown(
            "[Open Milvus Dashboard](https://localhost:8181)",
            unsafe_allow_html=True,
        )
    # Postgres
    with st.expander("Postgresql"):
        st.markdown("Modify, upload, or delete your chat-data seamlessly.")

