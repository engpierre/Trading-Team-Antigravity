import os
import yfinance as yf

class FetchAIAgentConnector:
    """
    Dedicated agent for managing decentralized data retrieval.
    Updated to act as a direct quantitative oracle, bypassing network consensus
    to fetch strict live, real-time pricing data directly via yfinance.
    """
    def __init__(self, endpoint_url=None):
        pass
        
    def dispatch_task(self, ticker, task_payload):
        print(f"[*] (Fetch.AI Oracle) Fetching live quantitative pricing for {ticker}...")
        
        try:
            stock = yf.Ticker(ticker.upper())
            ticker_info = stock.info
            
            # Strict safe lookup hierarchy using .get() to prevent KeyError if markets are closed
            live_price = ticker_info.get('currentPrice', ticker_info.get('lastPrice', ticker_info.get('regularMarketPrice')))
            
            if live_price is None:
                # Reality Anchor Fallback: If .info is rate-limited, ping .history for closing price
                hist = stock.history(period="1d")
                if not hist.empty:
                    live_price = hist['Close'].iloc[-1]
                else:
                    return f"FETCH.AI ORACLE ERROR [{ticker.upper()}]: Could not retrieve reliable live price data. Scraper offline."
                    
            return f"""
            --- FETCH.AI DECENTRALIZED ORACLE ---
            TARGET SYMBOL: {ticker.upper()}
            STRICTLY CURRENT PRICE: {float(live_price):.2f}
            """
            
        except Exception as e:
            return f"FETCH.AI ORACLE ERROR: Network exception occurred - {str(e)}"

if __name__ == "__main__":
    agent = FetchAIAgentConnector()
    print(agent.dispatch_task("AAPL", {}))
