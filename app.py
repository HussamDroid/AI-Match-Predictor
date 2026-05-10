import streamlit as st
import datetime
from api_client import FootballAPIClient
from model_logic import MatchPredictor

st.set_page_config(page_title="AI Match Predictor", layout="wide", page_icon="⚽")

# --- HIGH-IMPACT SCOREBOARD & STANDINGS CSS ---
st.markdown("""
    <style>
    /* Fixtures Styling */
    .scoreboard-container {
        background-color: #1a1a1a;
        border-radius: 15px;
        padding: 25px;
        border-left: 5px solid #ff4b4b;
    }
    .team-header { font-size: 28px; font-weight: 800; text-align: center; color: white; }
    .score-massive { 
        font-size: 95px !important; 
        font-weight: 900; 
        text-align: center; 
        line-height: 1;
        margin: 10px 0px;
        font-family: 'Courier New', Courier, monospace;
    }
    .win-green { color: #00ff41; text-shadow: 0 0 10px #00ff41; }
    .lose-red { color: #ff3131; text-shadow: 0 0 10px #ff3131; }
    .draw-white { color: #ffffff; }
    
    .match-day-time { 
        text-align: center; 
        color: #ffaa00; 
        font-size: 20px; 
        font-weight: bold;
        background: rgba(255,170,0,0.1);
        padding: 5px;
        border-radius: 5px;
    }
    .match-full-date { text-align: center; color: #888; font-size: 16px; margin-bottom: 15px; }

    /* Standings UI Overhaul */
    .st-table-header {
        background-color: #ff4b4b !important;
        color: white !important;
        font-weight: bold;
    }
    .ucl-spot { border-left: 5px solid #00ff41; padding-left: 10px; }
    .relegation-spot { border-left: 5px solid #ff3131; padding-left: 10px; }
    .pts-bold { font-weight: 900; color: #ff4b4b; font-size: 1.1em; }
    </style>
""", unsafe_allow_html=True)

def main():
    api = FootballAPIClient()
    predictor = MatchPredictor()
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Fixtures", "Standings"])
    leagues = api.get_available_leagues()
    sel_league_name = st.sidebar.selectbox("League", list(leagues.keys()))
    l_code = leagues[sel_league_name]
    standings = api.get_standings(l_code)

    if page == "Fixtures":
        target_date = st.sidebar.date_input("Match Date", datetime.date.today())
        st.header(f"Live Match Center: {sel_league_name}")
        
        matches = api.get_fixtures(l_code, target_date)
        
        if not matches:
            st.warning(f"No matches scheduled for {target_date.strftime('%A, %B %d')}.")
        else:
            for m in matches:
                h_stats = standings.get(m['homeTeam']['name'])
                a_stats = standings.get(m['awayTeam']['name'])
                match_dt = datetime.datetime.strptime(m['utcDate'], "%Y-%m-%dT%H:%M:%SZ")
                
                with st.container(border=True):
                    st.markdown(f"<p class='match-full-date'>{match_dt.strftime('%A, %B %d, %Y')}</p>", unsafe_allow_html=True)
                    
                    col_home, col_score, col_away = st.columns([2, 3, 2])
                    
                    with col_home:
                        st.markdown(f"<p class='team-header'>{m['homeTeam']['shortName']}</p>", unsafe_allow_html=True)
                        st.image(m['homeTeam']['crest'], width=130)
                    
                    with col_score:
                        if m['status'] == "FINISHED":
                            h_score = m['score']['fullTime']['home']
                            a_score = m['score']['fullTime']['away']
                            
                            h_style = "win-green" if h_score > a_score else "lose-red" if h_score < a_score else "draw-white"
                            a_style = "win-green" if a_score > h_score else "lose-red" if a_score < h_score else "draw-white"
                            
                            st.markdown(f"<p class='score-massive'><span class='{h_style}'>{h_score}</span><span class='draw-white'>:</span><span class='{a_style}'>{a_score}</span></p>", unsafe_allow_html=True)
                            st.markdown("<p class='match-day-time'>FINAL RESULT</p>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<p class='score-massive' style='color:white;'>{match_dt.strftime('%H:%M')}</p>", unsafe_allow_html=True)
                            st.markdown(f"<p class='match-day-time'>KICK-OFF (UTC)</p>", unsafe_allow_html=True)
                    
                    with col_away:
                        st.markdown(f"<p class='team-header'>{m['awayTeam']['shortName']}</p>", unsafe_allow_html=True)
                        st.image(m['awayTeam']['crest'], width=130)

                    if m['status'] != "FINISHED" and h_stats and a_stats:
                        res = predictor.calculate_probability(h_stats, a_stats)
                        st.write("---")
                        with st.expander("VIEW AI PREDICTION SUMMARY"):
                            p1, p2, p3 = st.columns(3)
                            p1.metric(f"{m['homeTeam']['shortName']} Win", f"{res['Home']}%")
                            p2.metric("Draw Chance", f"{res['Draw']}%")
                            p3.metric(f"{m['awayTeam']['shortName']} Win", f"{res['Away']}%")
                            st.divider()
                            st.write(f"**Analysis:** Based on league data, **{m['homeTeam']['shortName']}** has an Expected Goals (xG) of **{res['h_xg']}**, while **{m['awayTeam']['shortName']}** is at **{res['a_xg']}**.")
                            st.progress(int(res['Home']))

    else:
        st.header(f"{sel_league_name} Table")
        
        # Enhanced Table Data
        processed_data = []
        for n, d in standings.items():
            # Zone markers
            pos = d['position']
            zone_class = "ucl-spot" if pos <= 4 else "relegation-spot" if pos >= 18 else ""
            
            processed_data.append({
                "Rank": pos,
                "Crest": d['team']['crest'],
                "Team": n,
                "P": d['playedGames'],
                "W": d['won'],
                "D": d['draw'],
                "L": d['lost'],
                "GD": d['goalDifference'],
                "PTS": d['points'],
                "Zone": zone_class
            })

        # Using st.column_config for a professional data table
        st.dataframe(
            processed_data,
            column_config={
                "Rank": st.column_config.NumberColumn("Pos", format="%d"),
                "Crest": st.column_config.ImageColumn(" ", width="small"),
                "Team": st.column_config.TextColumn("Club"),
                "P": st.column_config.NumberColumn("MP"),
                "W": st.column_config.NumberColumn("W"),
                "D": st.column_config.NumberColumn("D"),
                "L": st.column_config.NumberColumn("L"),
                "GD": st.column_config.NumberColumn("GD"),
                "PTS": st.column_config.NumberColumn("PTS", help="Total Points accumulated"),
                "Zone": None # Hide this column, used for logic only
            },
            hide_index=True,
            use_container_width=True
        )
        
        st.info("🟢 Top 4: UCL Qualification | 🔴 Bottom 3: Relegation Zone")

if __name__ == "__main__":
    main()