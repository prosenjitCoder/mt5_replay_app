import streamlit as st
from core.state import update_index

def create_navigation_controls(symbol: str, screen_bars: int, df) -> None:
    """Create navigation controls with reliable keyboard support"""
    nav1, nav2, _ = st.columns([1, 1, 6])
    
    # Create buttons with distinct keys
    prev_pressed = nav1.button("◀ Prev", key=f"nav_prev_{symbol}")
    next_pressed = nav2.button("Next ▶", key=f"nav_next_{symbol}")
    
    # Handle navigation
    if prev_pressed:
        _handle_navigation(symbol, screen_bars, direction=-1, max_len=len(df))
    if next_pressed:
        _handle_navigation(symbol, screen_bars, direction=1, max_len=len(df))
    
    # Add keyboard navigation
    _add_keyboard_navigation()

def _handle_navigation(symbol: str, screen_bars: int, direction: int, max_len: int) -> None:
    """Handle navigation logic"""
    current_idx = st.session_state.get(f"idx_{symbol}", screen_bars)
    new_idx = current_idx + direction
    new_idx = max(screen_bars, min(new_idx, max_len))
    update_index(symbol, new_idx)
    st.rerun()

def _add_keyboard_navigation():
    """Optimized keyboard navigation that works consistently"""
    st.components.v1.html(
        """
        <script>
        (function() {
            const doc = window.parent.document;
            let prevBtn, nextBtn;
            
            function cacheButtons() {
                const buttons = Array.from(doc.querySelectorAll('button'));
                prevBtn = buttons.find(b => b.textContent.includes('◀ Prev'));
                nextBtn = buttons.find(b => b.textContent.includes('Next ▶'));
            }
            
            function handleKeyPress(e) {
                if (e.key === 'ArrowLeft' && prevBtn) {
                    prevBtn.click();
                    e.preventDefault();
                }
                if (e.key === 'ArrowRight' && nextBtn) {
                    nextBtn.click();
                    e.preventDefault();
                }
            }
            
            // Initial button cache
            cacheButtons();
            
            // Refresh buttons periodically in case of DOM changes
            setInterval(cacheButtons, 1000);
            
            // Add event listener
            doc.addEventListener('keydown', handleKeyPress);
        })();
        </script>
        """,
        height=0,
        width=0
    )