import sqlite3
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='[BACKTEST_VALIDATOR] %(message)s')
DB_PATH = 'antigravity_aar.db'

def initialize_blackbox():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ledger 1: The Mission Logs (The "SITREP" Archive)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mission_logs (
            mission_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            ticker TEXT,
            regime TEXT,
            conviction_delta TEXT,
            override_active INTEGER,
            price_at_entry REAL,
            primary_logic TEXT
        )
    ''')

    # Ledger 2: The Performance Ledger (The "ROI" Tracker)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance_ledger (
            mission_id INTEGER,
            price_current REAL,
            price_t_plus_24h REAL,
            price_t_plus_5d REAL,
            roi_percentage REAL,
            status TEXT,
            FOREIGN KEY(mission_id) REFERENCES mission_logs(mission_id)
        )
    ''')

    # Ledger 3: Agent Attribution (The "Trust" Matrix)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_attribution (
            agent_name TEXT PRIMARY KEY,
            total_verdicts INTEGER,
            successful_verdicts INTEGER,
            trust_coefficient REAL
        )
    ''')

    conn.commit()
    conn.close()
    
def save_verdict_to_blackbox(verdict_json, ticker, current_price):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        override = 1 if verdict_json.get('judicial_override') else 0
        logic = verdict_json.get('verdict', {}).get('final_logic', '')
        delta_str = str(verdict_json.get('conviction_delta', ''))
        regime = verdict_json.get('geopolitical', {}).get('geopolitical_regime', 'STABLE')
        
        # Capture the full 11-node intelligence state natively extracting current pricing
        cursor.execute('''
            INSERT INTO mission_logs 
            (timestamp, ticker, price_entry, regime, conviction_delta, override_active, primary_logic)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            ticker,
            current_price,
            regime,
            delta_str,
            override,
            logic
        ))
        
        mission_id = cursor.lastrowid
        # Initialize the pending performance loop array evaluating actual ROI metrics tomorrow
        cursor.execute('''
            INSERT INTO performance_ledger (mission_id, price_current, roi_percentage, status)
            VALUES (?, ?, ?, ?)
        ''', (mission_id, current_price, 0.0, "PENDING"))

        conn.commit()
        conn.close()
        logging.info(f"Verdict physically archived inside the AAR Blackbox for target: {ticker}")
    except Exception as e:
        logging.error(f"Failed to execute structural AAR DB dump: {e}")

def grade_overrides():
    """ 
    Calculates the Success Rate (S) of the trailing 10 Judicial Overrides natively.
    If S < 0.40, the system must forcefully fire the LOGIC RECALIBRATION REQUIRED array warning.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Target the final 10 Override specific arrays cross-indexing Closed Performance blocks
        cursor.execute('''
            SELECT p.roi_percentage 
            FROM mission_logs m
            JOIN performance_ledger p ON m.mission_id = p.mission_id
            WHERE m.override_active = 1 AND p.status = 'CLOSED'
            ORDER BY m.timestamp DESC
            LIMIT 10
        ''')
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return False, "Insufficient Closed Paper Trades mapped to execute exact structural Override Recalibration math."
            
        wins = sum([1 for r in rows if r[0] > 0])
        win_rate = wins / len(rows)
        
        # Hard limits mapping failure parameters trapping RSI configuration execution drift
        if len(rows) >= 5 and win_rate < 0.40:
            return True, f"Win-Rate {win_rate*100:.1f}% (< 40%)."
        return False, f"Win-Rate {win_rate*100:.1f}%."
    except Exception as e:
        return False, f"Error calculating structural AAR math: {e}"

# Architect structure automatically on launch
initialize_blackbox()
