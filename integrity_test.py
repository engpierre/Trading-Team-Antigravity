import sys
import logging
from supervisor_agent import SupervisorAgent

logging.basicConfig(level=logging.INFO, format='[STRESS TEST] %(message)s')

def run_stress_test():
    logging.info("Initiating 11-Node Integrity Protocol...")
    try:
        from optimizer_engine import get_global_trust_weights
        weights, avg = get_global_trust_weights()
        logging.info(f"Optimizer Hook Online. Trust Avg: {avg*100:.1f}%.")
        logging.info(f"Active Weights: {weights}")
    except Exception as e:
        logging.error(f"Failed to calculate optimization weights mathematically: {e}")
        sys.exit(1)
        
    try:
        from backtest_validator import grade_overrides
        needs_recalibration, grade_report = grade_overrides()
        logging.info(f"Validator Hook Online. {grade_report}")
    except Exception as e:
        logging.error(f"Failed to run quantitative AAR validators: {e}")
        sys.exit(1)
        
    logging.info("Pre-flight architecture chemically secure. Deploying full 11-node stack against AAPL (Reactive Audit)...")
    
    sup = SupervisorAgent()
    try:
        j, r = sup.execute_audit("AAPL", is_proactive=False)
        if j:
            logging.info("STRESS TEST SUCCESS: 11-Node logic block completed successfully resolving circular mapping.")
            logging.info(f"Final CIO Synthesis Extract: {j.get('verdict', {}).get('stance')} | Score: {j.get('conviction_delta')}")
        else:
            logging.error("STRESS TEST FAILED: Master CIO synthesis returned null payload array.")
            sys.exit(1)
    except Exception as e:
        logging.error(f"STRESS TEST SYSTEM CRASH: {e}")
        sys.exit(1)
        
if __name__ == "__main__":
    run_stress_test()
