import streamlit as st

def show_data_analysis():
    st.header("📊 Data Analysis Module")
    st.write("This module performs basic statistical analysis and visualization.")
    
    import numpy as np
    import pandas as pd
    import plotly.express as px
    
    # Generate some data
    data = pd.DataFrame({
        'x': np.random.randn(100),
        'y': np.random.randn(100),
        'category': np.random.choice(['A', 'B', 'C'], 100)
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Raw Data")
        st.dataframe(data.head())
        
    with col2:
        st.subheader("Statistics")
        st.write(data.describe())
        
    st.subheader("Interactive Scatter Plot")
    fig = px.scatter(data, x='x', y='y', color='category', 
                     template="plotly_dark",
                     title="Random Data Distribution")
    st.plotly_chart(fig, use_container_width=True)
