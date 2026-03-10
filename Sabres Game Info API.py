import requests
import time
import datetime

def get_sabres_game_info():
    # 1. Get scoreboard
    try:
        r = requests.get("https://api-web.nhle.com/v1/scoreboard/BUF/now", timeout=12)
        r.raise_for_status()
        data = r.json()
    except:
        return "ERROR\n   \n   \n     "

    # 2. Pick the right game (today live > today > upcoming > last played)
    today = datetime.date.today()
    games_today = []
    upcoming = []
    past = []

    for date_group in data.get('gamesByDate', []):
        try:
            gdate = datetime.date.fromisoformat(date_group['date'])
        except:
            continue
        for game in date_group.get('games', []):
            if gdate == today:
                games_today.append(game)
            elif gdate > today:
                upcoming.append(game)
            else:
                past.append(game)

    if games_today:
        live = [g for g in games_today if g['gameState'] in ['LIVE', 'CRIT']]
        game = live[0] if live else games_today[0]
    elif upcoming:
        game = min(upcoming, key=lambda x: x.get('gameDate', ''))
    elif past:
        game = max(past, key=lambda x: x.get('gameDate', ''))
    else:
        return "     \n  0 \n  0 \nUPC  "

    game_id = game['id']
    game_state = game['gameState']

    # 3. Get boxscore
    try:
        box = requests.get(f"https://api-web.nhle.com/v1/gamecenter/{game_id}/boxscore", timeout=10).json()
    except:
        return "ERROR\n   \n   \n     "

    # Shots
    home_sog = box.get('homeTeam', {}).get('sog', 0)
    away_sog = box.get('awayTeam', {}).get('sog', 0)

    # Clock & Period logic
    if game_state in ['FINAL', 'OFF']:
        clock_str   = ""          # completely blank line
        period_str  = "FINAL"
    elif game_state not in ['LIVE', 'CRIT']:
        clock_str   = ""
        period_str  = "PRE"
    else:
        clock_data = box.get('clock', {})
        time_rem   = clock_data.get('timeRemaining', '00:00')
        inter      = clock_data.get('inIntermission', False)

        if inter:
            clock_str = "INT"
        else:
            if ':' in time_rem:
                m, s = time_rem.split(':')
                if int(m) < 10:
                    m = str(int(m))      # removes leading zero
                clock_str = f"{m}:{s}"
            else:
                clock_str = time_rem

        # Period label
        pd = box.get('periodDescriptor', {})
        num = pd.get('number', 0)
        typ = pd.get('periodType', 'REG')
        if num == 0:
            period_str = "UNK"
        else:
            ords = {1: '1ST', 2: '2ND', 3: '3RD'}
            period_str = ords.get(num, f"{num}TH")
            if typ != 'REG':
                period_str = typ.upper()

    # ─── FIXED 5-CHAR WIDTH FOR PERFECT STACKED ALIGNMENT ───
    clock_line  = f"{clock_str:<5}"   # 5 spaces when blank → never shifts
    period_line = f"{period_str:<5}"
    home_line   = f"{home_sog:>3}"     # right-aligned shots
    away_line   = f"{away_sog:>3}"

    # Order: Clock → Home shots → Away shots → Period
    return f"{clock_line}\n{home_line}\n{away_line}\n{period_line}"


# ———————————————— RUN LOOP ————————————————
print("Sabres Scorebug → game_info.txt | Running...")
print("Console will show updates every ~15 seconds")
print("Press Ctrl+C to stop\n")

try:
    while True:
        text = get_sabres_game_info()
        
        # Write to file for OBS
        with open("game_info.txt", "w", encoding="utf-8") as f:
            f.write(text)
        
        # Show nice formatted update in console
        now_str = datetime.datetime.now().strftime('%H:%M:%S')
        lines = text.strip().split('\n')
        
        if len(lines) == 4:
            clock, home, away, period = [line.strip() for line in lines]  # clean whitespace
            print(f"[{now_str}]   Clock / Period     Shots (H / A)")
            print(f"          {clock: <5}          {home: >2} / {away: >2}")
            print(f"          {period: <5}")
        else:
            print(f"[{now_str}] {text.strip()}")
        
        print("─" * 50)
        
        time.sleep(15)

except KeyboardInterrupt:
    print("\nStopped by user.")
except Exception as e:
    print(f"Loop crashed: {e}")
