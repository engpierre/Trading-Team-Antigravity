import streamlit as st
import pandas as pd
import numpy as np
from supervisor_agent import SupervisorAgent

def render_audit_card(ticker, json_data, raw_reports):
    """ Modular helper rendering the adversarial tabs dynamically parsing the strict CIO 8-Node JSON schema. """
    v_action = json_data.get('verdict', {}).get('action', 'NEUTRAL')
    v_confidence = json_data.get('verdict', {}).get('confidence', 'Unknown')
    v_logic = json_data.get('verdict', {}).get('final_logic', json_data.get('verdict', {}).get('logic', 'Fetching Master Logic...'))
    integrity = json_data.get('integrity_check', json_data.get('raw_integrity', 'System Status Pending...'))
    delta_str = json_data.get('conviction_delta', 'N/A')
    
    # 🌟 Integrity Status Banner
    st.info(f"🛡️ **System Health (Integrity Monitor):** {integrity}")
    
    # 🌍 Geopolitical IPB Banner
    ipb_data = json_data.get('geopolitical', {})
    if ipb_data.get('geopolitical_regime') == 'VOLATILE':
        st.error(f"🌍 **GEOPOLITICAL SITREP WARNING (Risk {ipb_data.get('risk_score', 0)}/100):** {ipb_data.get('chokepoint_analysis', 'Friction')} -> {ipb_data.get('strategic_impact', 'Risk detected.')}")

    tab_swarm, tab_critic = st.tabs(["✅ Bullish Swarm", "🚩 Adversarial Critic"])

    with tab_swarm:
        st.metric("Swarm Conviction Score", f"{json_data.get('swarm_score', 0)}/100")
        with st.expander("Underlying Swarm Pillars (Anchored by Oracle Ground Truth)"):
            st.code(raw_reports.get('FetchAI (Oracle)', 'No Oracle Data'), language="json")
            st.info(raw_reports.get('WhaleWatcher', 'No Whale Data'))
            st.info(raw_reports.get('Technical', 'No Tech Data'))
            st.info(raw_reports.get('Fundamental', 'No Fund Data'))

    with tab_critic:
        critic_data = json_data.get('critic', {})
        st.metric("Risk Factor (Critic)", f"{json_data.get('critic_score', 0)}/100", delta="Bearish Vulnerability", delta_color="inverse")
        st.error(f"**CRITIC REBUTTAL:** {critic_data.get('rebuttal', 'No structural weaknesses mathematically uncovered.')}")
        
    st.divider()
    
    v_color = "#3498db"
    if "BUY" in v_action.upper(): v_color = "#2ecc71"
    if "SELL" in v_action.upper() or "CAUTION" in v_action.upper() or "TRAP" in v_action.upper(): v_color = "#e74c3c"
    if "HOLD" in v_action.upper(): v_color = "#FF9800"
    
    # CIO Mathematical Adjudication Layout
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        st.metric("Conviction Delta (Swarm > Risk)", delta_str)
    with c2:
        st.write(f"Confidence Level: **{v_confidence}**")
    
    st.markdown(f"### ⚖️ Master CIO Verdict: <span style='color:{v_color};'>{v_action}</span>", unsafe_allow_html=True)
    
    # --- Judicial Override UI Logic ---
    if json_data.get("judicial_override"):
        st.warning("⚠️ **JUDICIAL OVERRIDE ACTIVE**")
        st.caption("The Master CIO has overridden the Adversarial Critic based on 'Generational Alpha' parameters (Deep Oversold RSI/Divergence).")

    st.write(f"**CIO Strategy:** {v_logic}")

def main():
    st.set_page_config(page_title="Anti-gravity 8-Node Swarm", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")
    
    st.sidebar.title("📡 Command Center")
    mode = st.sidebar.radio("Operating Mode", ["Manual Audit", "Autonomous Recon", "AAR Ledger (Backtest)"])
    st.sidebar.markdown("---")
    st.sidebar.caption("Anti-gravity Quant Desk © 2026")
    
    st.markdown("<h1 style='text-align: center;'>⚖️ Anti-gravity War Room</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    supervisor = SupervisorAgent()

    if mode == "Manual Audit":
        st.markdown("<h4 style='text-align: center; color: gray;'>Reactive Ticker Analysis</h4>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            ticker = st.text_input("Target Node:", "AAPL", label_visibility="collapsed").upper()
            if st.button("Execute Reactive Audit", use_container_width=True, type="primary"):
                with st.spinner(f"Initiating 8-Node Judicial Loop targeting {ticker}..."):
                    j_list, r_list = supervisor.execute(ticker, mode="manual")
                
                if not j_list:
                    st.error("❌ Agent Swarm Failed. Ensure GEMINI_API_KEY is active in terminal profile.")
                else:
                    render_audit_card(ticker, j_list[0], r_list[0])
                    
    elif mode == "Autonomous Recon":
        st.markdown("<h4 style='text-align: center; color: #3498db;'>Proactive Market Discovery</h4>", unsafe_allow_html=True)
        st.info("The Scout Node aggressively scans the highly liquid megacap universe (S&P benchmark) to mathematically isolate the Top 3 Mansfield Outliers, autonomously piping each target natively into the Master CIO Judicial loop.")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Launch Autonomous Recon 🚀", use_container_width=True, type="primary"):
                
                with st.status("Deploying Proactive Hunter... (Approx 45s Multi-Array Generation)", expanded=True) as status:
                    st.write("1️⃣ Scout Agent Calculating MRS & Volume Delta Arrays...")
                    st.write("2️⃣ Triangulating Top 10 Anomalies & Executing Pearson Matrix Locks...")
                    st.write("3️⃣ Dispatching Central Swarms & Extrapolating Insider Interventions...")
                    
                    j_list, r_list = supervisor.execute("SCAN", mode="discovery")
                    status.update(label="Reconnaissance Sweep Complete!", state="complete", expanded=False)
                    
                if not j_list:
                    st.error("❌ Reconnaissance Failed.")
                else:
                    st.success(f"Successfully calculated and adjudicated {len(j_list)} completely diversified algorithmic breakouts.")
                    
                    # Intercept the Covariance Report globally injected into the first array object safely
                    cov_report = r_list[0].get('Covariance (Diversification Matrix)', '')
                    if "TACTICAL ADJUSTMENT" in cov_report:
                        # Split by newline and render each warning separately
                        for warning_msg in cov_report.split("\n\n"):
                            st.warning(warning_msg)
                    elif cov_report:
                        st.success(cov_report)
                        
                    # Generates flexible array architecture independent of volume payload
                    for j, r in zip(j_list, r_list):
                        t_name = j.get("ticker", "UNKNOWN")
                        with st.expander(f"📌 HIGH-CONVICTION SCOUT TARGET LOCKED: {t_name}", expanded=True):
                            render_audit_card(t_name, j, r)

    elif mode == "AAR Ledger (Backtest)":
        st.markdown("<h4 style='text-align: center; color: #8e44ad;'>📈 After-Action DB Overrider</h4>", unsafe_allow_html=True)
        st.info("The Validator physically tracks the paper-trade lifecycle and natively penalizes Hallucinating nodes utilizing Spearman Rank correlation metrics over time.")
        
        try:
            from optimizer_engine import get_global_trust_weights
            weights, trust_avg = get_global_trust_weights()
            
            st.subheader("🧠 Self-Optimization: Trust Matrix")
            df_weights = pd.DataFrame([weights]).T.reset_index()
            df_weights.columns = ['Agent', 'Active Weight']
            
            st.data_editor(
                df_weights,
                column_config={
                    "Active Weight": st.column_config.ProgressColumn(
                        "Current Influence",
                        help="The mathematical weight used in final synthesis",
                        format="%.2f",
                        min_value=0,
                        max_value=1,
                    ),
                },
                hide_index=True,
                use_container_width=True
            )
            
            if trust_avg < 0.40:
                st.error(f"🤖 **SELF-OPTIMIZATION ACTIVE:** Boosting Adversarial Critic weight natively due to trailing volatility-drift (Swarm Trust {trust_avg*100:.1f}%).")
        
            from backtest_validator import grade_overrides
            needs_recalibration, grade_report = grade_overrides()
            if needs_recalibration:
                st.error(f"🚨 **LOGIC RECALIBRATION REQUIRED:** Judicial Override trailing win-rate failing baseline ({grade_report}). Advocate tightening Generational Alpha trigger to RSI-20 to avoid catching 'Falling Knives'.")
            else:
                st.success(f"⚖️ Judicial Overrides maintaining structural precision. {grade_report}")
                
            # Display Mission Logs locally
            import sqlite3
            conn = sqlite3.connect('antigravity_aar.db')
            df_logs = pd.read_sql_query("SELECT mission_id, timestamp, ticker, regime, conviction_delta, override_active, price_entry FROM mission_logs ORDER BY timestamp DESC LIMIT 25", conn)
            st.dataframe(df_logs, use_container_width=True)
            conn.close()
        except Exception as e:
            st.warning("Database currently empty. Execute 8-Node CI array loops to populate the structural persistent ledgers.")

if __name__ == "__main__":
    main()
